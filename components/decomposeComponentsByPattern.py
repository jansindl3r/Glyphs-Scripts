#MenuTitle: Decompose components in selected glyphs by pattern

__doc__="""

Removes components from selected glyphs that match a regex pattern.

"""

import vanilla
import re

pattern_default = "com.jansindl3r.decomposeComponentsPattern.pattern"
Glyphs.registerDefault(pattern_default, r".*\.numr")

def sanitize_component_name(name):
	return f"c_{hash(name)}"
	
def get_duplicate_index(components, component):
	same_glyph_components = [same_component for same_component in components if same_component.name == component.name]
	if component in same_glyph_components:
		return same_glyph_components.index(component)
	else:
		return None

class Dialog:
	def __init__(self):
		self.window = vanilla.FloatingWindow(
			(300, 105),
			"Set Selected Glyphs Components Y", 
		)
		self.component_elements = []
		self.window.pattern_label = vanilla.TextBox((15, 15, -15, 20), "Select Glyph as Input", sizeStyle="small")
		self.window.pattern = vanilla.EditText((15, 35, -15, 20), Glyphs.defaults[pattern_default], sizeStyle="small")
		self.window.process = vanilla.Button((15, 65, -15, 20), "Decompose", sizeStyle="small", callback=self.decompose)
		self.window.open()
		
		self.selected_layer = None


	def decompose(self, sender):
		font = Glyphs.font
		pattern = self.window.pattern.get()
		try:
			for selectedLayer in font.selectedLayers:
				glyph = selectedLayer.parent
				for layer in glyph.layers:
					for component in layer.components:
						if re.match(pattern, str(component.component.name)):
							component.decompose()
		except re.error as e:
			Message("Invalid Regex Pattern")
		Glyphs.defaults[pattern_default] = pattern
		Glyphs.redraw()

Dialog()


