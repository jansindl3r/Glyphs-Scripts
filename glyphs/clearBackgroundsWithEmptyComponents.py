# MenuTitle: Clear Backgrounds with Empty Components

font = Glyphs.font
glyphs = font.glyphs
glyph_names = [glyph.name for glyph in glyphs]
for glyph in glyphs:
	for layer in glyph.layers:
		components = layer.background.components
		for component in components:			
			if not component.component:
				layer.background.clear()