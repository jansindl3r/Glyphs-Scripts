#MenuTitle: Tab with open corner glyphs

font = Glyphs.font
from fontTools.misc.bezierTools import segmentSegmentIntersections
from fontTools.misc.bezierTools import segmentSegmentIntersections


class OpenCornerPen:
	def __init__(self):
		self.contour = []
		self.open_corners = []
		
	def moveTo(self, point):
		self.contour = [[point]]
		
	def lineTo(self, point):
		self.contour.append([point])
		
	def curveTo(self, point_1, point_2, point_3):
		self.contour.append([point_1, point_2, point_3])
		
	def closePath(self):
		num_segments = len(self.contour)
		if num_segments < 4:
			return  # No possibility of self-intersection with less than 2 segments

		for i in range(num_segments):
			for j in range(i + 2, num_segments + (i > 0)):
				segment_1 = (self.contour[i-1][-1], *self.contour[i])
				segment_2 = (self.contour[j-1][-1], *self.contour[j % num_segments])
				try:
					intersections = segmentSegmentIntersections(segment_1, segment_2)
				except ZeroDivisionError as e:
					pass
				for intersection in intersections:
					if 0 < intersection.t1 < 1 and 0 < intersection.t2 < 1:
						self.open_corners.append(intersection.pt)
		
		self.contour = []
	
	def addComponent(self, *args):
		pass
		
	def endPath(self):
		self.closePath()

open_corner_glyphs = set()

for glyph in font.glyphs:
	for layer in glyph.layers:
		if layer.isMasterLayer:
			open_corner_pen = OpenCornerPen()
			layer.draw(open_corner_pen)
			
			# Print out any detected open corners
			if open_corner_pen.open_corners:
				open_corner_glyphs.add(glyph.name)
				break

if open_corner_glyphs:
	font.newTab("/".join(["\n"]+list(open_corner_glyphs)))
else:
	Message("No open corners", title='Alert', OKButton=None)