#MenuTitle: Save stroked shapes in .stroke-source layer

font = Glyphs.font  # Get the current font
for glyph in font.glyphs:
	if glyph.selected:
		for layer in glyph.layers:
			if layer.isMasterLayer and len([
				shape.attributes for shape in layer.shapes if shape.attributes.get("strokeHeight", shape.attributes.get("strokeWidth"))
				]):
				copied_layer = layer.copy()
				copied_layer.name = layer.name + ".stroke-source"
				try:
					index = [l.name for l in glyph.layers].index(copied_layer.name)
					del glyph.layers[index]
				except ValueError:
					pass
				glyph.layers.append(copied_layer)


for glyph in font.glyphs:
	if glyph.selected:
		for layer in glyph.layers:
			if layer.name.endswith(".stroke-source"):
				layer_index = [l.name for l in glyph.layers].index(layer.name.split(".stroke-source")[0])
				destination_layer = glyph.layers[layer_index]
				destination_layer.shapes = layer.shapes.copy()
				for s, shape in list(enumerate(destination_layer.shapes[::1]))[::-1]:
					if shape.__class__.__name__ == "GSPath":
						expanded_stroke = shape.expandedStroke()
						if len(expanded_stroke):
							del destination_layer.shapes[s]
							for p, path in list(enumerate(expanded_stroke))[::-1]:
								destination_layer.paths.append(path.copy())
		
		