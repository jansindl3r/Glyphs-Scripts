# MenuTitle: Check Glyphs Width Against a Glyph

__doc__ = """

Usecase: Check if all tabular numbers (`*.\.tf.*`) have the same width as zero.tf.

"""

import re
from vanilla import Window, Group, PopUpButton, Button, TextBox, EditText


class Dialog:
    def __init__(self):
        self.w = Window((260, 180), "Check Glyph Widths Against a Glyph")
        self.w.group = Group("auto")
        self.w.group.glyph_selector_label = TextBox("auto", "Select reference glyph:")
        self.w.group.glyph_selector = PopUpButton("auto", self.get_options())
        self.w.group.runButton = Button(
            "auto", "Check Widths", callback=self.check_widths
        )
        self.w.group.regex_pattern_label = TextBox("auto", "Glyph Name Regex Pattern")
        self.w.group.regex_pattern = EditText("auto")

        rules = [
            "H:|-[glyph_selector_label]-|",
            "H:|-[glyph_selector]-|",
            "H:|-[regex_pattern_label]-|",
            "H:|-[regex_pattern]-|",
            "H:|-[runButton]-|",
            "V:|-[glyph_selector_label]-[glyph_selector]-[regex_pattern_label]-[regex_pattern]-20-[runButton]-|",
        ]
        metrics = {}
        self.w.group.addAutoPosSizeRules(rules, metrics)
        self.w.open()

    def get_options(self):
        return [glyph.name for glyph in Glyphs.font.glyphs]

    def check_widths(self, sender):

        check_against = {}
        reference_glyph = Glyphs.font.glyphs[self.w.group.glyph_selector.get()]

        for layer in reference_glyph.layers:
            if layer.isMasterLayer:
                check_against[layer.layerId] = layer.width

        try:
            pattern = re.compile(self.w.group.regex_pattern.get())
            layers_to_open = []
            for glyph in Glyphs.font.glyphs:
                if re.match(pattern, glyph.name):
                    for layer in glyph.layers:
                        if layer.isMasterLayer or layer.isSpecialLayer:
                            source_width = check_against[
                                layer.layerId
                                if layer.isMasterLayer
                                else layer.associatedMasterId
                            ]
                            if source_width != layer.width:
                                layers_to_open.append(layer)

            Glyphs.font.newTab(layers_to_open)
        except re.error:
            Message("Error", "Invalid regex pattern", OKButton="OK")


Dialog()
