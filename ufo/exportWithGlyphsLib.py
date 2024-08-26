#MenuTitle: Export to UFO with GlyphsLib

__doc__="""

Bakes smart stuff and exports the current font to UFO using glyphsLib

"""

import subprocess
import vanilla
from vanilla import dialogs

from GlyphsApp import GSScriptingHandler
from time import sleep

try:
	import glyphsLib
except ModuleNotFoundError as e:
	python_path = GSScriptingHandler.sharedHandler().currentPythonPath()
	python_executable = python_path + "/bin/python3"
	subprocess.Popen(
		[python_executable, "-m", "pip", "install", "glyphsLib"],
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		encoding="utf-8",
		text=True,
		bufsize=1
	)
	sleep(3)

from glyphsLib import build_masters
from tempfile import NamedTemporaryFile
	
	
class Dialog:
	def __init__(self):
		self.window = vanilla.FloatingWindow(
			(300, 80),
			"Export to UFO with GlyphsLib", 
		)
		self.component_elements = []
		self.window.get_folder = vanilla.Button((15, 15, -15, 20), "Select Export Folder", sizeStyle="small", callback=self.get_folder)
		self.window.export_button = vanilla.Button((15, 45, -15, 20), "Export", sizeStyle="small", callback=self.export)
		self.window.export_button.enable(False)
		self.window.open()
		self.export_folder = None
		
	def get_folder(self, sender):
		export_folder = dialogs.getFolder()
		self.export_folder = export_folder[0]
		sender._nsObject.setTitle_(f"{export_folder}")
		self.window.export_button.enable(True)


	def export(self, sender):
		font = Glyphs.font.copy()

		for glyph in font.glyphs:
			for layer in glyph.layers:
				layer.decomposeCorners()

		with NamedTemporaryFile(suffix='.glyphs', delete=True) as temp_file:
			font.save(temp_file.name)
			build_masters(temp_file.name, self.export_folder, minimal=True)

Dialog()

