#MenuTitle: Set Selected Glyphs Components Y

import vanilla

font = Glyphs.font

class Dialog:
	def __init__(self):
		self.window = vanilla.FloatingWindow(
			(200, 110),
			"Set Selected Glyphs Components Y", 
		)
		self.window.label = vanilla.TextBox((15, 15, -15, 20), "y position", sizeStyle='small')
		self.window.input_field = vanilla.EditText((15, 40, -15, 20), sizeStyle='small', callback=None)
		self.window.button = vanilla.Button((15, 75, -15, 20), "Apply", sizeStyle='small', callback=self.setYPosition)
		self.window.open()

	def setYPosition(self, sender):
		value = self.window.input_field.get()
		try:
			value = float(value)
			for glyph in font.glyphs:
				if glyph.selected:
					for layer in glyph.layers:
						for component in layer.components:
							component.y = value
		except ValueError as e:
			print(e)

Dialog()
