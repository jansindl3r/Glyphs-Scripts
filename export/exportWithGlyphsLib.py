#MenuTitle: Export with GlyphsLib

__doc__="""

Bakes smart stuff and exports the current font to UFO, OTF and TTF using glyphsLib

"""

import subprocess
import vanilla
from vanilla import dialogs

from GlyphsApp import GSScriptingHandler
from time import sleep

try:
	import glyphsLib
	import ufo2ft
	import fontmake
 
except ModuleNotFoundError as e:
	python_path = GSScriptingHandler.sharedHandler().currentPythonPath()
	python_executable = python_path + "/bin/python3"
	subprocess.Popen(
		[python_executable, "-m", "pip", "install", "glyphsLib", "ufo2ft", "fontmake"],
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		encoding="utf-8",
		text=True,
		bufsize=1
	)
	sleep(3)

from glyphsLib import build_masters
from ufo2ft import compileOTF, compileTTF, compileVariableTTFs
from tempfile import NamedTemporaryFile
from fontmake.instantiator import Instantiator
from fontTools.designspaceLib import DesignSpaceDocument
from pathlib import Path


	
class Dialog:
	def __init__(self):
		self.window = vanilla.FloatingWindow(
			(300, 175),
			"Export to UFO with GlyphsLib", 
		)
		self.component_elements = []
		self.window.get_folder = vanilla.Button((15, 15, -15, 20), "Select Export Folder", sizeStyle="small", callback=self.get_folder)
		self.window.export_otf = vanilla.CheckBox((15, 45, -15, 20), "Export OTF", sizeStyle="small", value=True, callback=self.toggle_export)
		self.window.export_ttf = vanilla.CheckBox((15, 75, -15, 20), "Export TTF", sizeStyle="small", value=True, callback=self.toggle_export)
		self.window.export_variable = vanilla.CheckBox((15, 105, -15, 20), "Export Variable", sizeStyle="small", value=True, callback=self.toggle_export)
		self.window.export_button = vanilla.Button((15, 135, -15, 20), "Export", sizeStyle="small", callback=self.export)
		self.window.export_button.enable(False)
		self.window.open()
		self.export_folder = None

	def toggle_export(self, sender):
		if any([getattr(self.window, checkbox_name).get() for checkbox_name in ["export_otf", "export_ttf", "export_variable"]]):
			self.window.export_button.enable(True)
		else:
			self.window.export_button.enable(False)

		
	def get_folder(self, sender):
		export_folder = dialogs.getFolder()
		self.export_folder = Path(export_folder[0])
		sender._nsObject.setTitle_(f"{export_folder}")
		self.window.export_button.enable(True)


	def export(self, sender):
		font = Glyphs.font.copy()

		for glyph in font.glyphs:
			for layer in glyph.layers:
				if not (layer.isMasterLayer or layer.isSpecialLayer):
					continue
				layer.decomposeCorners()
				for s, shape in list(enumerate(layer.shapes[::1]))[::-1]:
					if shape.__class__.__name__ == "GSPath":
						expanded_stroke = shape.expandedStroke()
						if len(expanded_stroke):
							del layer.shapes[s]
							for path in expanded_stroke[::-1]:
								layer.paths.append(path.copy())

		export_paths = []
		if self.window.export_ttf.get():
			export_paths.append(self.export_folder/"ttf")
		if self.window.export_otf.get():
			export_paths.append(self.export_folder/"otf")
		if self.window.export_variable.get():
			export_paths.append(self.export_folder/"variable_ttf")
			
		for path in export_paths:
			if not path.exists():
				path.mkdir(parents=True)

		with NamedTemporaryFile(suffix='.glyphs', delete=True) as temp_file:
			font.save(temp_file.name)
			_, designspace_path = build_masters(temp_file.name, self.export_folder/"ufo", minimal=True)
			designspace = DesignSpaceDocument.fromfile(designspace_path)
			instantiator = Instantiator.from_designspace(designspace)
			for instance in designspace.instances:
				ufo = instantiator.generate_instance(instance)
				filename = Path(instance.filename).stem
				if self.window.export_ttf.get():
					compileTTF(ufo).save(self.export_folder/"ttf"/f"{filename}.ttf")
				if self.window.export_otf.get():
					compileOTF(ufo).save(self.export_folder/"otf"/f"{filename}.otf")

			if self.window.export_variable.get():
				for key, font in compileVariableTTFs(designspace, optimizeGvar=True).items():
					font.save(self.export_folder/"variable_ttf"/f"{key}.ttf")

Dialog()

