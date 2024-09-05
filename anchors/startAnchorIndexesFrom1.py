# MenuTitle: Start Anchor Indexes From 1
import re


def get_int_in_anchor_name(anchor_name):
    return int(re.match(r".*(\d+).*", anchor_name).group(1))


selected_glyphs = [layer.parent for layer in Glyphs.font.selectedLayers]
for glyph in selected_glyphs:
    for layer in glyph.layers:
        anchors_with_int = filter(lambda x: re.search(r"\d+", x.name), layer.anchors)
        anchors = sorted(
            anchors_with_int, key=lambda x: get_int_in_anchor_name(x.name), reverse=True
        )
        anchors_grouped = {}
        for anchor in anchors:
            key = re.sub(r"\d+", "", anchor.name)
            if key != anchor.name:
                anchors_grouped.setdefault(key, []).append(anchor)
        for anchor_group in anchors_grouped.values():
            min_index = get_int_in_anchor_name(anchor_group[-1].name)
            difference = 1 - min_index
            for anchor in anchor_group:
                match = re.search("\d+", anchor.name)
                left, right = match.span()
                new_anchor_name = (
                    anchor.name[:left]
                    + str(int(match.group()) + difference)
                    + anchor.name[right:]
                )
                anchor.name = new_anchor_name
