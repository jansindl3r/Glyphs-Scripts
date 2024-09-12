# MenuTitle: Tab with Glyphs that have an Overlap

from vanilla import Window, Group, PopUpButton, Button, TextBox


__doc__ = """

Finds glyphs glyphs in given layer that have an overlap.

"""


import re
from vanilla import Window, Group, PopUpButton, Button, TextBox, EditText


class Dialog:
	def __init__(self):
		
		self.w = Window((210, 120), "Check Glyph Widths Against a Glyph")
		self.w.group = Group("auto")
		self.w.group.glyph_selector_label = TextBox("auto", "Select Layer:")
		self.w.group.glyph_selector = PopUpButton("auto", self.get_options())
		self.w.group.run_button = Button(
			"auto", "Find Glyphs with Overlap", callback=self.check_widths
		)
		rules = [
			"H:|-[glyph_selector_label]-|",
			"H:|-[glyph_selector]-|",
			"H:|-[run_button]-|",
			"V:|-[glyph_selector_label]-[glyph_selector]-20-[run_button]-|",
		]
		metrics = {}
		self.w.group.addAutoPosSizeRules(rules, metrics)
		self.w.open()

	def get_options(self):
		return [master.name for master in Glyphs.font.masters]

	def check_widths(self, sender):
		options = self.get_options()
		layers_to_open = []
		for glyph in Glyphs.font.glyphs:
			layer = glyph.layers[options[self.w.group.glyph_selector.get()]]
			if not layer:
				continue
			output_layer = GSLayer()
			output_layer.paths.extend([path.copy() for path in layer.paths])
			output_layer.removeOverlap()
			layer_number_of_nodes = sum([len(path.segments) for path in layer.paths])
			output_number_of_nodes = sum([len(path.segments) for path in output_layer.paths])
			if layer_number_of_nodes != output_number_of_nodes:
				layers_to_open.append(layer)
		Glyphs.font.newTab(layers_to_open)

Dialog()

