# MenuTitle: Baseline Glyph

__doc__ = """

Creates a glyph that shows the vertical metrics.

"""

font = Glyphs.font
try:
    font.glyphs.append(GSGlyph("baseline"))
except NameError:
    pass
glyph = font.glyphs["baseline"]
for layer in glyph.layers:
    layer.clear()
    heights = {
        getattr(layer.master, key)
        for key in ["xHeight", "descender", "ascender", "capHeight"]
    }
    heights.add(0)
    pen = layer.getPen()
    upm = font.upm
    for height in heights:
        pen.moveTo((0, height - 1))
        pen.lineTo((upm, height - 1))
        pen.lineTo((upm, height + 1))
        pen.lineTo((0, height + 1))
        pen.closePath()
        pen.endPath()
    layer.width = upm
glyph.unicode = "F8FF"
