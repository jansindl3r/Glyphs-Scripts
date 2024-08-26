#MenuTitle: Check If Contours Can Interpolate Nicely
from math import hypot, atan2, degrees

Glyphs.clearLog()
font = Glyphs.font
for glyph in font.glyphs:
    paths_across_layers = zip(*[layer.paths for layer in glyph.layers if layer.isMasterLayer or layer.isSpecialLayer])
    for path_across_layer in paths_across_layers:
        angles = []
        for path in path_across_layer:
            angles.append([])
            nodes = path.nodes
            for n in range(len(nodes)):
                prev_node = nodes[n-1]
                node = nodes[n]
                next_node = nodes[(n+1) % len(nodes)]

                if node.type == "offcurve" and prev_node.type == "curve":
                    angle = atan2(prev_node.y - node.y, prev_node.x - node.x)
                    angles[-1].append(degrees(angle))
            
                elif node.type == "curve" and prev_node.type == "offcurve" and next_node.type == "curve":
                    angle = atan2(node.y - prev_node.y, node.x - prev_node.x)
                    angles[-1].append(degrees(angle))

                elif node.type == "curve" and prev_node.type == "offcurve":
                    guess_smooth = hypot(prev_node.x - node.x, prev_node.y - node.y), hypot(node.x - next_node.x, node.y - next_node.y)
                    print("guess", guess_smooth)
                    # angle = atan2(next_node.y - prev_node.y, next_node.x - prev_node.x)
                    # angles[-1].append(degrees(angle))

        all_equal = all(lst == angles[0] for lst in angles)
        print(angles)
        print(glyph.name, all_equal)
                #print(node.type)

                
            
            
