# MenuTitle: Spread Master Parameters

__doc__ = """

Copies custom parameters from one master to all other masters.

"""

import GlyphsApp
from vanilla import FloatingWindow, PopUpButton, Button, TextBox, CheckBox
from math import ceil


class Dialog:
    def __init__(self):
        self.layerNames = [layer.name for layer in Glyphs.font.masters]
        self.w = FloatingWindow(
            (300, 150), "Copy Stems", minSize=(300, 150), maxSize=(500, 250)
        )

        self.w.master_from_label = TextBox("auto", "Source Layer", sizeStyle="small")
        self.w.master_from = PopUpButton(
            "auto",
            self.layerNames,
            sizeStyle="small",
            callback=self.on_master_from_change,
        )
        self.parameter_names = []

        self.w.copy_button = Button(
            "auto", "Spread Master Parameters", callback=self.spread, sizeStyle="small"
        )

        self.set_checkboxes()
        self.w.open()

    def set_checkboxes(self):
        parameters_rules_horizontal = []
        parameters_rules_vertical = ""
        for custom_parameter in Glyphs.font.masters[
            self.w.master_from.get()
        ].customParameters:
            name = f"parameter_{custom_parameter.name}"
            self.parameter_names.append(name)
            parameters_rules_horizontal.append(f"H:|-[{name}]-|")
            parameters_rules_vertical += f"[{name}]"
            setattr(
                self.w,
                name,
                CheckBox(
                    "auto",
                    f"{custom_parameter.value}\t\t{custom_parameter.name}",
                    value=True,
                    sizeStyle="small",
                ),
            )

        rules = [
            f"V:|-[master_from_label][master_from]-20-{parameters_rules_vertical}-20-[copy_button]-|",
            "H:|-[master_from_label]-|",
            "H:|-[master_from]-|",
            *parameters_rules_horizontal,
            "H:|-[copy_button]-|",
        ]
        metrics = {}
        self.w.addAutoPosSizeRules(rules, metrics)

    def spread(self, sender):
        index_from = self.w.master_from.get()
        master_from = Glyphs.font.masters[self.w.master_from.get()]
        for i, master_to in enumerate(Glyphs.font.masters):
            if i == index_from:
                continue
            for parameter_name in self.parameter_names:
                if getattr(self.w, parameter_name).get():
                    parameter_key = parameter_name.replace("parameter_", "")
                    parameter = master_from.customParameters[parameter_key]
                    master_to.customParameters[parameter_key] = parameter

    def on_master_from_change(self, _):
        for parameter_name in self.parameter_names:
            delattr(self.w, parameter_name)
        self.parameter_names = []
        self.set_checkboxes()


# Run the dialog
Dialog()
