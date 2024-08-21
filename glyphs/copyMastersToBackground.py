#MenuTitle: Copy masters to background

font = Glyphs.font
selected_glyphs = [l.parent for l in font.selectedLayers]
for selected_glyph in selected_glyphs:
	for layer in selected_glyph.layers:
		if layer.isMasterLayer or layer.isSpecialLayer:
			layer.background.clear()
			layer.background = layer.copy()