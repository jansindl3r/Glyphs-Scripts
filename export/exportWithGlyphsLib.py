#MenuTitle: Export with GlyphsLib

__doc__="""

Bakes smart stuff and exports the current font to UFO, OTF and TTF using glyphsLib

"""

import subprocess
import vanilla
import re
import traceback
from vanilla import dialogs

from GlyphsApp import GSScriptingHandler
from time import sleep


try:
	import glyphsLib
	import ufo2ft
	import fontmake
	import ufoLib2
 
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
from ufoLib2 import Font


def rename_bracket(glyph_name, appendix):
    match = re.match(r"(?P<glyph_name>.*)\.BRACKET\.varAlt(?P<var_alt>\d+)", glyph_name)
    if match:
        group_dict = match.groupdict()
        new_name = f"{group_dict['glyph_name']}.{appendix}.{group_dict['var_alt']}"
        return new_name

def rename_doc(doc, appendix):
    for rule in doc.rules:
        for s, (from_sub, to_sub) in enumerate(rule.subs):
            new_to_sub = rename_bracket(to_sub, appendix)
            if new_to_sub:
                rule.subs[s] = (from_sub, new_to_sub)

    doc.write(doc.path)

def rename_font(font, appendix):

	glyphs_to_rename = []
	for glyph in font:
		new_glyph_name = rename_bracket(glyph.name, appendix)
		if new_glyph_name:
			glyphs_to_rename.append((glyph.name, new_glyph_name))
		for component in glyph.components:
			new_component_name = rename_bracket(component.baseGlyph, appendix)
			if new_component_name:
				component.baseGlyph = new_component_name

	for old_name, new_name in glyphs_to_rename:
		font.renameGlyph(old_name, new_name)
	font.save()

	
class Dialog:
	def __init__(self):
		self.window = vanilla.FloatingWindow(
			(300, 205),
			"Export to UFO with GlyphsLib", 
		)
		self.component_elements = []
		self.window.get_folder = vanilla.Button((15, 15, -15, 20), "Select Export Folder", sizeStyle="small", callback=self.get_folder)
		self.window.export_otf = vanilla.CheckBox((15, 45, -15, 20), "Export OTF", sizeStyle="small", value=True, callback=self.toggle_export)
		self.window.export_ttf = vanilla.CheckBox((15, 75, -15, 20), "Export TTF", sizeStyle="small", value=True, callback=self.toggle_export)
		self.window.export_variable = vanilla.CheckBox((15, 105, -15, 20), "Export Variable", sizeStyle="small", value=True, callback=self.toggle_export)
		self.window.bracket_layer_glyph_appendix_label = vanilla.TextBox((15, 138, -15, 20), "Bracket Layer Appendix", sizeStyle="small")
		self.window.bracket_layer_glyph_appendix = vanilla.EditText((150, 135, -15, 20), text="rvrn", sizeStyle="small")
		self.window.export_button = vanilla.Button((15, 165, -15, 20), "Export", sizeStyle="small", callback=self.export)
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
		self.window.export_button.enable(False)
		self.window.export_button._nsObject.setTitle_("Exporting...")

		try:
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
			
			for glyph in font.glyphs:
				for layer in glyph.layers:
					if not (layer.isMasterLayer or layer.isSpecialLayer):
						continue
					for component in layer.components:
						if component.attributes.get("reversePaths", False):
							component.decompose()
						if component.component and not component.component.export:
							component.decompose()

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
				ufo_paths, designspace_path = build_masters(temp_file.name, self.export_folder/"ufo", minimal=True)
				designspace = DesignSpaceDocument.fromfile(designspace_path)
				bracket_layer_appendix = self.window.bracket_layer_glyph_appendix.get()
				rename_doc(designspace, bracket_layer_appendix)
				for ufo_path in ufo_paths:
					ufo = Font.open(self.export_folder/"ufo"/ufo_path)
					rename_font(ufo, bracket_layer_appendix)
					ufo.save()

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
		except Exception as e:
			Message("Error", f"Something went wrong: {e}", OKButton=None)
			print('\n'.join(traceback.format_tb(e.__traceback__)))
		
		self.window.export_button.enable(True)
		self.window.export_button._nsObject.setTitle_("Export")
	

Dialog()

