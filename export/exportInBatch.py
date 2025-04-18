#MenuTitle: Export in batch all relevant formats in separate folders

from AppKit import NSOpenPanel, NSOKButton
from pathlib import Path

font = Glyphs.font  # the current open font

def chooseFolder():
	panel = NSOpenPanel.openPanel()
	panel.setCanChooseFiles_(False)
	panel.setCanChooseDirectories_(True)
	panel.setAllowsMultipleSelection_(False)

	if panel.runModal() == NSOKButton:
		return panel.URLs()[0].path()
	else:
		return None
		
export_path = chooseFolder()
if not export_path:
	raise Exception()
export_path = Path(export_path)

formats = [
	("OTF", {"destination": "otf", "container": "plain"}),
	("TTF", {"destination": "ttf", "container": "plain"}),
	("TTF", {"destination": "woff", "container": "WOFF"}),
	("TTF", {"destination": "woff2", "container": "WOFF2"}),
]

variable_formats = [
	("TTF", {"destination": "variable_ttf", "container": "plain"}),
	("TTF", {"destination": "variable_woff", "container": "WOFF"}),
	("TTF", {"destination": "variable_woff2", "container": "WOFF2"}),
]

for format, data in formats:
	destination_folder = export_path/data["destination"]
	destination_folder.mkdir(parents=True, exist_ok=True)
	for instance in font.instances:
		if instance.active and instance.type == INSTANCETYPESINGLE:
			instance.generate(
				Format=format,
				Containers=[data["container"]],
				FontPath=str(export_path/destination_folder),
				AutoHint=True,
				RemoveOverlap=True
			)
				
for format, data in variable_formats:
	destination_folder = export_path/data["destination"]
	destination_folder.mkdir(parents=True, exist_ok=True)
	for instance in font.instances:
		if instance.active and instance.type == INSTANCETYPEVARIABLE:
			instance.generate(
				Format=format,
				Containers=[data["container"]],
				FontPath=str(export_path/destination_folder),
				AutoHint=True,
				RemoveOverlap=True
			)
			