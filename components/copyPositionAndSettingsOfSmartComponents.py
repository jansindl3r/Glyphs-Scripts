#MenuTitle: Copy Position & Settings of Smart Components

__doc__="""

Copies the position and settings of smart components from a selected glyph to other selected glyphs. You select input glyph and then select either one or more glyphs to paste the components to.

"""

import vanilla

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
			(300, 60),
			"Set Selected Glyphs Components Y", 
		)
		self.component_elements = []
		self.window.select_glyph = vanilla.Button((15, 15, -15, 20), "Select Glyph as Input", sizeStyle="small", callback=self.selected_glyph_as_input)
		self.window.open()
		
		self.selected_layer = None


	def selected_glyph_as_input(self, sender):
		font = Glyphs.font
		selected_layer = font.selectedLayers[0]
		selected_glyph = selected_layer.parent
		self.selected_layer = selected_layer

		
		if not getattr(self.window, "position_label", None):
			y = 35
			self.window.position_label = vanilla.TextBox((-145, y, -80, 20), "Position", alignment="center")
			self.window.settings_label = vanilla.TextBox((-80, y, -15, 20), "Settings", alignment="center")
		y = 55
		button_center_offset = 25
		
		for component in self.component_elements:
			for suffix in ["label", "position", "settings"]:
				delattr(self.window, component + "_" + suffix)
		
		self.component_elements = []
		for c, component in enumerate(selected_layer.components):
			sanitized = sanitize_component_name(component.name)

			duplicate_index = get_duplicate_index(selected_layer.components, component)
			if duplicate_index is not None:
				sanitized += f"_i_{duplicate_index}"
				setattr(self.window, f"component_{sanitized}_label", vanilla.TextBox((15, y, -15, 20), component.name + f" ({duplicate_index + 1})"))
			else:	
				setattr(self.window, f"component_{sanitized}_label", vanilla.TextBox((15, y, -15, 20), component.name))
			setattr(self.window, f"component_{sanitized}_position", vanilla.CheckBox((-145 + button_center_offset, y, -80, 20), "", value=True))
			setattr(self.window, f"component_{sanitized}_settings", vanilla.CheckBox((-80 + button_center_offset, y, -15, 20), "", value=True))
			self.component_elements.append(f"component_{sanitized}")
			y += 20
		
		self.window.select_glyph._nsObject.setTitle_(f"Selected Glyph: \"{selected_glyph.name}\"")
		
		# y += 20
		# if getattr(self.window, "paste_all_layers", None):

		# 	pos_size = list(self.window.paste_all_layers.getPosSize())
		# 	pos_size[1] = y
		# 	self.window.paste_all_layers.setPosSize(pos_size)
		# else:
		# 	self.window.paste_all_layers = vanilla.CheckBox((15, y, -15, 20), "Paste All Layers", sizeStyle="small", value=False)

		y += 20
		if getattr(self.window, "paste_selected", None):
			pos_size = list(self.window.paste_selected.getPosSize())
			pos_size[1] = y
			self.window.paste_selected.setPosSize(pos_size)
		else:
			self.window.paste_selected = vanilla.Button((15, y, -15, 20), "Paste Selected", sizeStyle="small", callback=self.paste_selected)
		
		pos_size = list(self.window.getPosSize())
		pos_size[-1] = y + 40
		self.window.setPosSize(pos_size)

	def paste_selected(self, sender):
		font = Glyphs.font
		
		selected_layer_components_map = {}
		for component in self.selected_layer.components:
			selected_layer_components_map.setdefault(component.name, []).append(component)
		

		for layer in font.selectedLayers:
			for component in layer.components:
				sanitized = sanitize_component_name(component.name)
				duplicate_index = get_duplicate_index(layer.components, component)
				if duplicate_index is not None:
					sanitized += f"_i_{duplicate_index}"
				else:
					duplicate_index = 0

				if component.name in selected_layer_components_map:
					if getattr(self.window, f"component_{sanitized}_position").get():
						component.automaticAlignment = False
						component.position = selected_layer_components_map[component.name][duplicate_index].position

					if getattr(self.window, f"component_{sanitized}_settings").get():
						for key, value in selected_layer_components_map[component.name][duplicate_index].smartComponentValues.items():
							component.smartComponentValues[key] = value
							print(key, value)
		Glyphs.redraw()
		

Dialog()

