# MenuTitle: Copy Anchors from Layer

import GlyphsApp
from vanilla import FloatingWindow, PopUpButton, Button, TextBox
from math import radians, tan


def correct_italic_offset(angle, x_height):
    angle_rads = radians(angle)
    return x_height * tan(angle_rads)


class CopyAnchorsDialog:
    def __init__(self):
        self.layerNames = [layer.name for layer in Glyphs.font.masters]
        self.w = FloatingWindow(
            (300, 150), "Copy Anchors", minSize=(300, 150), maxSize=(500, 250)
        )

        self.w.layer_from_label = TextBox("auto", "Source Layer", sizeStyle="small")
        self.w.layer_from = PopUpButton("auto", self.layerNames, sizeStyle="small")
        self.w.layer_to_label = TextBox("auto", "Destination Layer", sizeStyle="small")
        self.w.layer_to = PopUpButton("auto", self.layerNames, sizeStyle="small")

        self.w.copyButton = Button(
            "auto", "Copy Anchors", callback=self.copyAnchors, sizeStyle="small"
        )

        rules = [
            "V:|-[layer_from_label][layer_from]-[layer_to_label][layer_to]-20-[copyButton]-|",
            "H:|-[layer_from_label]-|",
            "H:|-[layer_from]-|",
            "H:|-[layer_to_label]-|",
            "H:|-[layer_to]-|",
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

        layer_from = Glyphs.font.masters[index_from]
        layer_to = Glyphs.font.masters[index_to]

        for glyph_layer in Glyphs.font.selectedLayers:
            glyph_layer_a = glyph_layer.parent.layers[layer_from.id]

            glyph_layer_b = glyph_layer.parent.layers[layer_to.id]

            glyph_layer_b.anchors = []

            for anchor in glyph_layer_a.anchors:
                offset_value_from = correct_italic_offset(
                    layer_from.italicAngle, layer_from.xHeight / 2
                )  # italic correction
                offset_value_to = correct_italic_offset(
                    layer_to.italicAngle, layer_to.xHeight / 2
                )  # italic correction

                x, y = anchor.position

                offset_value_from -= correct_italic_offset(layer_from.italicAngle, y)
                offset_value_to -= correct_italic_offset(layer_to.italicAngle, y)

                glyph_layer_b.anchors.append(
                    GSAnchor(
                        anchor.name,
                        (round(x + (offset_value_from - offset_value_to)), y),
                    )
                )

        Glyphs.showNotification(
            "Anchor Copier", "Anchors copied from Layer A to Layer B successfully!"
        )


# Run the dialog
CopyAnchorsDialog()
