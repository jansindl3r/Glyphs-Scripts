# MenuTitle: Copy Data from Master

import GlyphsApp
from vanilla import FloatingWindow, PopUpButton, Button, TextBox, CheckBox, EditText
from Foundation import NSAffineTransform





class Dialog:
	def __init__(self):
		self.layerNames = [layer.name for layer in Glyphs.font.masters]
		self.w = FloatingWindow(
			(300, 180), "Copy Data", minSize=(300, 180), maxSize=(500, 280)
		)

		self.w.layer_from_label = TextBox("auto", "Source Layer", sizeStyle="small")
		self.w.layer_from = PopUpButton("auto", self.layerNames, sizeStyle="small")
		self.w.layer_to_label = TextBox("auto", "Destination Layer", sizeStyle="small")
		self.w.layer_to = PopUpButton("auto", self.layerNames, sizeStyle="small")
		self.w.x_offset_label = TextBox("auto", "X Offset", sizeStyle="small")
		self.w.x_offset = EditText("auto", "0", sizeStyle="small")
		self.w.copy_shapes = CheckBox("auto", "Copy Shapes", sizeStyle="small")

		self.w.copyButton = Button(
			"auto", "Copy Data", callback=self.copyAnchors, sizeStyle="small"
		)

		rules = [
			"V:|-[layer_from_label][layer_from]-[layer_to_label][layer_to]-[x_offset_label][x_offset]-[copy_shapes]-20-[copyButton]-|",
			"H:|-[layer_from_label]-|",
			"H:|-[layer_from]-|",
			"H:|-[layer_to_label]-|",
			"H:|-[layer_to]-|",
			"H:|-[x_offset_label]-|",
			"H:|-[x_offset]-|",
			"H:|-[copy_shapes]-|",
			"H:|-[copyButton]-|",
		]
		metrics = {}
		self.w.addAutoPosSizeRules(rules, metrics)
		# Open the dialog window
		self.w.open()

	def copyAnchors(self, sender):
		# Get the selected layers (A and B)
		index_from = self.w.layer_from.get()
		index_to = self.w.layer_to.get()

		source_layer = Glyphs.font.masters[index_from]
		dest_layer = Glyphs.font.masters[index_to]

		# Copy anchors
		for glyph_layer in Glyphs.font.selectedLayers:
			source_glyph_layer = glyph_layer.parent.layers[source_layer.id]
			dest_glyph_layer = glyph_layer.parent.layers[dest_layer.id]
			
			dest_glyph_layer.clear()
			dest_glyph_layer.LSB = source_glyph_layer.LSB
			dest_glyph_layer.width = source_glyph_layer.width
			# If the checkbox is checked, copy shapes too
			if self.w.copy_shapes.get():
				dest_glyph_layer.background.clear()
				dest_glyph_layer.guides.clear()
				for shape in source_glyph_layer.shapes:
					shape = shape.copy()
					if shape.__class__.__name__ == "GSComponent":
						setattr(shape, "automaticAlignment", False)
					dest_glyph_layer.shapes.append(shape)
				for anchor in source_glyph_layer.anchors:
					dest_glyph_layer.anchors.append(anchor.copy())
				translate_x = float(self.w.x_offset.get())
				if translate_x:
					transform = NSAffineTransform.transform()
					transform.translateXBy_yBy_(translate_x, 0)
					for path in dest_glyph_layer.paths:
						path.applyTransform(transform.transformStruct())


# Run the dialog
Dialog()
