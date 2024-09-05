# MenuTitle: Check Italics Have Same Width

__doc__ = """

Checks if glyphs on Italic, Slant or actually any other has the same width as their parent layer.

"""

import vanilla


def sanitize_component_name(name):
    return f"c_{hash(name)}"


def get_duplicate_index(components, component):
    same_glyph_components = [
        same_component
        for same_component in components
        if same_component.name == component.name
    ]
    if component in same_glyph_components:
        return same_glyph_components.index(component)
    else:
        return None


class Dialog:
    def __init__(self):
        self.window = vanilla.FloatingWindow(
            (300, 20),
            "Set Selected Glyphs Components Y",
        )
        self.component_elements = []
        self.font = Glyphs.font
        options = [axis.name for axis in self.font.axes]
        self.window.base_axis_index_label = vanilla.TextBox(
            "auto", "Select Base Non-Italic Axis", sizeStyle="small"
        )
        self.window.base_axis_index = vanilla.RadioGroup(
            "auto", options, sizeStyle="small", callback=self.on_input
        )
        self.window.check = vanilla.Button(
            "auto", "Check", sizeStyle="small", callback=self.check
        )
        self.window.check.enable(False)

        rules = [
            # Horizontal
            "H:|-[base_axis_index_label]-|",
            "H:|-[base_axis_index]-|",
            "H:|-[check]-|",
            "V:|-[base_axis_index_label]-[base_axis_index]-[check]-|",
        ]
        metrics = {}
        self.window.addAutoPosSizeRules(rules, metrics)
        self.window.open()

    def on_input(self, sender):
        if sender.get() is not None:
            self.window.check.enable(True)
        else:
            self.window.check.enable(False)

    def check(self, sender):
        groupped_masters = {}
        base_axis_index = self.window.base_axis_index.get()
        for master in self.font.masters:
            groupped_masters.setdefault(master.axes[base_axis_index], []).append(
                master.id
            )

        groupped_masters_values = list(groupped_masters.values())

        new_tab_content = []
        for glyph in self.font.glyphs:
            if not glyph.export:
                continue
            widths = {}
            for layer in glyph.layers:
                if layer.isMasterLayer:
                    for g, group in enumerate(groupped_masters_values):
                        if layer.layerId in group:
                            widths.setdefault(g, []).append(layer.width)

            for group_index, width_values in widths.items():
                if len(set(width_values)) != 1:
                    unsynced_layers = groupped_masters_values[group_index][1:]
                    for unsynced_layer in unsynced_layers:
                        new_tab_content.append(glyph.layers[unsynced_layer])

        self.font.newTab(new_tab_content)


Dialog()
