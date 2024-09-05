import vanilla
# MenuTitle: Insert Preliminary Carets

selected_glyphs = [layer.parent for layer in Glyphs.font.selectedLayers]
for glyph in selected_glyphs:
	number_of_carets = glyph.name.count("_")
	if number_of_carets == 0:
		if glyph.name in ["fl", "fi"]:
			number_of_carets = 1
		elif glyph.name in ["ellipsis"]:
			number_of_carets = 2
		else:
			number_of_carets = int(AskString(f"Number of carets for \"{glyph.name}\"", value=None, title='Glyphs', OKButton=None, placeholder=None))
	for layer in glyph.layers:
		if layer.isMasterLayer or layer.isSpecialLayer:
			layer.anchors = [
				anchor
				for anchor in layer.anchors
				if not anchor.name.startswith("caret")
			]
		step = layer.width / number_of_carets
		for i in range(number_of_carets):
			layer.anchors.append(GSAnchor(f"caret_{i + 1}", (step / 2 + step * i, 0)))
