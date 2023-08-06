import unicodedata
import pkgutil
import io

import moderngl
import numpy as np
import pygame.font

from ..allocators.vertlists import VAO
from ..loaders import fonts
from ..atlas import Atlas
from .sprites import QUAD
from .base import Bounds, Transformable, Colorable


FONT_LOAD_SIZE = 48
default_font = None


def get_default_font():
    """Get the default font."""
    global default_font
    if not default_font:
        ttf_data = pkgutil.get_data('wasabi2d', 'data/roboto_regular.ttf')
        default_font = pygame.font.Font(io.BytesIO(ttf_data), FONT_LOAD_SIZE)
    return default_font


class TextureVAO(VAO):
    """A VAO with an associated texture."""

    def render(self, camera):
        self.prog['tex'].value = 0
        self.tex.use(0)
        super().render(camera)


def text_vao(
        ctx: moderngl.Context,
        shadermgr: 'wasabi2d.layers.ShaderManager') -> VAO:
    """Build a BAO for rendering plain colored objects."""
    return TextureVAO(
        mode=moderngl.TRIANGLES,
        ctx=ctx,
        prog=shadermgr.load('texquads', 'text'),
        dtype=np.dtype([
            ('in_vert', '2f4'),
            ('in_color', '4f4'),
            ('in_uv', '2u2'),
        ])
    )


class FontAtlas(Atlas):
    """The combination of a font and the texture atlas it uses."""
    def __init__(self, ctx, font_name):
        super().__init__(ctx)
        if font_name is None:
            self.font = get_default_font()
        else:
            self.font = fonts.load(font_name, fontsize=FONT_LOAD_SIZE)

    def _load(self, name):
        """Load the image for the given name."""
        return self.font.render(name, True, (255, 255, 255))


# Text alignments as a fraction of text layout width
ALIGNMENTS = {
    'left': 0,
    'center': 0.5,
    'right': 1,
}


class Label(Colorable, Transformable):
    """A single-line text block with no additional layout/wrapping."""

    def __init__(
            self,
            text: str,
            font_atlas: FontAtlas,
            layer,
            *,
            align='left',
            fontsize=20,
            pos=(0, 0),
            color=(1, 1, 1, 1)):
        assert align in ALIGNMENTS, f"{align!r} is not a valid text alignment."
        super().__init__()
        self.layer = layer
        self.lst = None
        self._verts = None
        self.align = align
        self.layer = layer
        self.fontsize = fontsize
        self.font_atlas = font_atlas
        self.pos = pos
        self.color = color
        self.vao = None
        self.text = text  # trigger layout

    def _set_dirty(self):
        self.layer._dirty.add(self)

    @property
    def align(self):
        """Get the alignment of the text relative to pos."""
        return self._align

    @align.setter
    def align(self, align):
        if align not in ALIGNMENTS:
            raise ValueError(f"{align!r} is not a valid text alignment.")
        self._align = align
        if self._verts is not None:
            self._layout()

    @property
    def text(self) -> str:
        """Get the text of this label."""
        return self._text

    @text.setter
    def text(self, text: str):
        """Set the text of this label.

        The string is currently normalised to composed form because this
        is simpler to lay out than a string with combining characters, and
        we may not be very sophisticated at this point.

        """
        self._str = unicodedata.normalize('NFC', str(text))
        self._text = text
        self._layout()

        self._set_dirty()

    def _layout(self):
        """Generate indices, uvs and verts for the text."""
        font = self.font_atlas.font

        descent = font.get_descent()
        n_chars = len(self._str) - self._str.count('\n')
        verts = np.ones((4 * n_chars, 3), dtype='f4')
        uvs = np.zeros((4 * n_chars, 2), dtype='f4')
        indices = np.zeros(n_chars * 6, dtype='u4')

        lines = self._str.split('\n')

        # We lay out based on 48px tex so line size is scaled later
        line_height = 48 * 1.3

        curchar = 0
        tex_ids = set()
        tex = None

        for lineno, line in enumerate(lines):
            if not line:
                continue
            # (min_x, max_x, min_y, max_y, horizontal_advance_x)
            metrics = np.array(font.metrics(line), dtype='f4')
            cx = np.cumsum(metrics[:, 4]).reshape(-1, 1)
            xpos = metrics[:, 0:2] + cx

            layout_width = cx[-1] + metrics[-1, 1]
            align_offset = ALIGNMENTS[self._align] * layout_width
            yoff = lineno * line_height
            for idx, char in enumerate(line):
                texregion = self.font_atlas.get(char)
                # TODO: this could break if tex is reallocated (eg. because it
                # grows)
                tex = texregion.tex.tex
                glyph_uvs = texregion.texcoords
                glyph_verts = texregion.get_verts(texregion.width, texregion.height)
                tex_ids.add(tex.glo)

                # The kerning seems pretty bad on Pygame fonts...
    #            glyph_width = glyph_verts[1, 0] - glyph_verts[0, 0]
    #            metrics_width = xpos[idx, 1] - xpos[idx, 0]
    #            print(repr(char), glyph_width, metrics_width, metrics[idx, 4])

                x = xpos[idx, 0]

                quadnum = idx + curchar
                start = quadnum * 4
                glyph_slice = slice(start, start + 4)
                verts[glyph_slice] = glyph_verts + (x - align_offset, yoff - descent, 0)
                uvs[glyph_slice] = glyph_uvs
                indices[6 * quadnum:6 * quadnum + 6] = QUAD + 4 * quadnum

            curchar += len(line)

        # Scale coordinates
        resize = np.identity(3, dtype='f4')
        scale = self.fontsize / 48
        resize[0, 0] = scale
        resize[1, 1] = scale

        # TODO: handle use of multiple textures. We will be able to handle
        # this eventually by selecting texture unit within the shader, or by
        # making multiple draw calls
        assert len(tex_ids) < 2, "Label got allocated over multiple textures"
        self.tex = tex
        self._verts = verts @ resize
        self._uvs = uvs
        self._indices = indices

        # TODO: update self.lst, set dirty OR reallocate self.lst for new size
        if self.tex is None:
            if self.lst:
                self.lst.free()
                self.lst = None
                self.vao = None
        elif self.lst:
            self.lst.realloc(len(self._verts), len(indices))
            self.lst.indexbuf[:] = indices
            self.lst.indexbuf += self.lst.vertoff.start
            self.lst.vertbuf['in_uv'] = uvs
            self._update()
        elif self.tex and not self.vao:
            self._migrate(self.layer._text_vao(self.font_atlas))

    bounds = Bounds('self._verts[:, :2]')

    def delete(self):
        self.layer.objects.remove(self)
        self.lst.free()
        self.layer = None
        self.vao = None

    def _update(self):
        if not self.lst:
            return
        xform = self._xform()

        np.matmul(
            self._verts,
            xform[:, :2],
            self.lst.vertbuf['in_vert']
        )
        self.lst.vertbuf['in_color'] = self._color
        self.lst.dirty = True

    def _migrate(self, vao: TextureVAO):
        """Migrate the fill into the given VAO."""
        # TODO: dealloc from an existing VAO
        if self.lst:
            self.lst.free()
            self.lst = None
        idxs = self._indices
        self.vao = vao
        self.vao.tex = self.tex
        self.lst = vao.alloc(len(self._verts), len(idxs))
        self.lst.indexbuf[:] = idxs
        self.lst.indexbuf += self.lst.vertoff.start
        self.lst.vertbuf['in_uv'] = self._uvs
        self._update()
