#MenuTitle: Set Y position for .case glyphs custom parameters (caseShift)

font = Glyphs.font

for glyph in font.glyphs:
	if ".case" in glyph.name:
		for layer in glyph.layers:
			if layer.isMasterLayer:
				value = layer.master.numbers["caseShift"]
				for component in layer.components:
					component.automaticAlignment = False
					if ".case" in component.name:
						component.y = layer.master.capHeight
					elif component.name.startswith("question") or component.name.startswith("exclam"):
						component.y = component.bounds.size.height
					else:
						component.y = value

# class Dialog:
# 	def __init__(self):
# 		self.window = vanilla.FloatingWindow(
# 			(200, 110),
# 			"Set Selected Glyphs Components Y", 
# 		)
# 		self.window.label = vanilla.TextBox((15, 15, -15, 20), "y position", sizeStyle='small')
# 		self.window.input_field = vanilla.EditText((15, 40, -15, 20), sizeStyle='small', callback=None)
# 		self.window.button = vanilla.Button((15, 75, -15, 20), "Apply", sizeStyle='small', callback=self.setYPosition)
# 		self.window.open()

# 	def setYPosition(self, sender):
# 		value = self.window.input_field.get()
# 		if not value:
# 			value = 0
# 		value = float(value)
# 		try:
# 			for glyph in font.glyphs:
# 				if ".case" in glyph.name:
# 					for layer in glyph.layers:
# 						for component in layer.components:
# 							component.automaticAlignment = False
# 							component.y = 0
# 							if component.name.startswith("question") or component.name.startswith("exclam"):
# 								component.y = component.bounds.size.height
# 							else:
# 								component.y = value
# 		except ValueError as e:
# 			print(e)

# Dialog()

