#MenuTitle: Set Y position of components in selected glyphs

__doc__="""

Sets component's Y position in selected glyphs

"""

import vanilla 



def process_glyph(glyph, value, process_all_layers, selected_layers):

	if process_all_layers:
		layers = glyph.layers
	else:
		layers = [layer for layer in glyph.layers if layer.layerId in selected_layers]

	for layer in layers:
		if layer.isMasterLayer or layer.isSpecialLayer:
			for component in layer.components:
				component.automaticAlignment = False
				component.y = value

class Dialog:
	def __init__(self):
		self.window = vanilla.FloatingWindow(
			(200, 140),
			"Set Selected Glyphs Components Y", 
		)
		self.window.label = vanilla.TextBox((15, 15, -15, 20), "Y position", sizeStyle='small')
		self.window.input_field = vanilla.EditText((15, 40, -15, 20), sizeStyle='small', callback=self.on_input)
		self.window.process_all_layers = vanilla.CheckBox((15, 70, -15, 20), "Process all master layers", value=True, sizeStyle='small')
		self.window.button = vanilla.Button((15, 100, -15, 20), "Apply", sizeStyle='small', callback=self.setYPosition)
		self.window.button.enable(False)
		self.window.open()

	def setYPosition(self, sender):
		font = Glyphs.font
		selected_layers = [layer.layerId for layer in font.selectedLayers]

		value = self.window.input_field.get()
		if value:
			value = float(value)
			for glyph in font.glyphs:
				if glyph.selected:
					process_glyph(glyph, value, self.window.process_all_layers.get(), selected_layers)

	def on_input(self, sender):
		value = sender.get()
		if value:
			try:
				length = len(str(float(value)))
				if length > 0:
					self.window.button.enable(True)
				else:
					self.window.button.enable(False)
			except ValueError:
				sender.set(value[:-1])

Dialog()

