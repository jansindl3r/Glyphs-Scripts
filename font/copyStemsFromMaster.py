# MenuTitle: Copy Stems from Master

__doc__ = """

Copies stems from one master to another.

"""

import GlyphsApp
from vanilla import FloatingWindow, PopUpButton, Button, TextBox
from math import ceil


class Dialog:
    def __init__(self):
        self.layerNames = [layer.name for layer in Glyphs.font.masters]
        self.w = FloatingWindow(
            (300, 150), "Copy Stems", minSize=(300, 150), maxSize=(500, 250)
        )

        self.w.master_from_label = TextBox("auto", "Source Layer", sizeStyle="small")
        self.w.master_from = PopUpButton("auto", self.layerNames, sizeStyle="small")
        self.w.master_to_label = TextBox("auto", "Destination Layer", sizeStyle="small")
        self.w.master_to = PopUpButton("auto", self.layerNames, sizeStyle="small")
        self.w.master_to.set(ceil(len(self.layerNames)) / 2)

        self.w.copy_button = Button(
            "auto", "Copy Stems", callback=self.copyAnchors, sizeStyle="small"
        )

        rules = [
            "V:|-[master_from_label][master_from]-[master_to_label][master_to]-20-[copy_button]-|",
            "H:|-[master_from_label]-|",
            "H:|-[master_from]-|",
            "H:|-[master_to_label]-|",
            "H:|-[master_to]-|",
            "H:|-[copy_button]-|",
        ]
        metrics = {}
        self.w.addAutoPosSizeRules(rules, metrics)
        # Open the dialog window
        self.w.open()

    def copyAnchors(self, sender):
        # Get the selected layers (A and B)
        index_from = self.w.master_from.get()
        index_to = self.w.master_to.get()

        master_from = Glyphs.font.masters[index_from]
        master_to = Glyphs.font.masters[index_to]

        master_to.stems = master_from.stems


# Run the dialog
Dialog()
