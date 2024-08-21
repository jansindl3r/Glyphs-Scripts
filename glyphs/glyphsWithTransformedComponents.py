#MenuTitle: glyphs with transformed components

font = Glyphs.font

glyphs_with_transformed_glyphs = set()
for glyph in font.glyphs:
	for layer in glyph.layers:
		if layer.isMasterLayer:
			for component in layer.components:
				if component.rotation != 0 or component.scale.x != 1 or component.scale.y != 1:
#					print(glyph.name, component.rotation, component.scale.x, component.scale.y, component.rotation)
					if len(layer.paths) or True:
						glyphs_with_transformed_glyphs.add(glyph.name)
						break

if glyphs_with_transformed_glyphs:
    font.newTab("/".join(["\n"]+list(glyphs_with_transformed_glyphs)))
else:
	Message("No glyphs with transformed components", "No glyphs with transformed components", OKButton="OK")