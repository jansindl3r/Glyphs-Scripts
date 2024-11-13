# MenuTitle: Tab with Not Matching Width Masters

from vanilla import Window, List, CheckBoxListCell, Button

class Dialog:

	def __init__(self):
		self.w = Window((200, 500))
		self.w.layers = List(
			"auto",
			[{"Title": master.name, "Checked": False} for master in Glyphs.font.masters],
			columnDescriptions=[{"title": "Title"}, {"title": "Checked", "cell": CheckBoxListCell()}],
			)
		self.w.button = Button(
			"auto", "Check Widths", callback=self.editCallback, sizeStyle="small"
		)
		rules = [
			"V:|-[layers]-[button]-|",
			"H:|-[layers]-|",
			"H:|-[button]-|",
		]
		metrics = {}
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()

	def editCallback(self, sender):
		layers_to_check = []
		layers_to_open_in_tab = []
		for layer, master in zip(self.w.layers, Glyphs.font.masters):
			if layer["Checked"]:
				layers_to_check.append(master)
				
		for glyph_layer in Glyphs.font.glyphs:
			widths = set()
			for layer in layers_to_check:
				widths.add(glyph_layer.layers[layer.id].width)
			if len(widths) != 1:
				for layer in layers_to_check:
					layers_to_open_in_tab.append(glyph_layer.layers[layer.id])
		Glyphs.font.newTab(layers_to_open_in_tab)

Dialog()
