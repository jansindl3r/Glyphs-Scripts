# MenuTitle: Tab with glyphs having this glyph in bg

__doc__ = """

Finds glyphs in the font that have the current glyph in their background.

"""

font = Glyphs.font
current_layer = font.selectedLayers[0]
glyphs_to_open_in_tab = []

for glyph in font.glyphs:
	glyph_layer = glyph.layers[current_layer.layerId]
	component_names = [str(component.name) for component in glyph_layer.background.components]
	if str(current_layer.parent.name) in component_names:
		glyphs_to_open_in_tab.append(glyph_layer)

if glyphs_to_open_in_tab:
	Glyphs.font.newTab(glyphs_to_open_in_tab)
else:
	Message(
		"No glyphs found with the current glyph in their background.",
		"Tab with glyphs having this glyph in bg",
		OKButton="OK",
	)