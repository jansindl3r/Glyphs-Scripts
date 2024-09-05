# MenuTitle: Remove empty paths from selected glyphs

__doc__ = """

Sometimes paths have 0 nodes

"""

font = Glyphs.font

for glyph in font.glyphs:
    if glyph.selected:
        for layer in glyph.layers:
            shapes = layer.shapes
            shapes_length = len(shapes)
            for s in range(shapes_length):
                shape = shapes[shapes_length - 1 - s]
                if len(shape) < 2:
                    del shapes[shapes_length - 1 - s]
