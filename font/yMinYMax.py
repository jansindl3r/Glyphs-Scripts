#MenuTitle: yMin & yMax

font = Glyphs.font

y_max = 0
y_min = 0
for glyph in font.glyphs:
	for layer in glyph.layers:
		if layer.isMasterLayer:
			value = layer.bounds.origin.y + layer.bounds.size.height
			if value > y_max:
				y_max = value
			if value < y_min:
				y_min = value

Message(f"yMax: {y_max}\nyMin: {y_min}", title="Horaaay!")