from pathlib import Path
import re

base = Path(__file__).parent

readme = ""
for folder in sorted(base.iterdir(), key=lambda x: x.name):
    if folder.is_dir() and not folder.name.startswith("."):
        readme += f"\n # {folder.stem.capitalize()} \n"
        for script_path in sorted(folder.glob("*.py"), key=lambda x: x.name):
            if script_path.stem.startswith("__"):
                continue
            title = re.match(r"#\ ?MenuTitle: (.*)", script_path.read_text())
            doc_pattern = r'__doc__\s*=\s*"""(.*?)"""'
            doc = re.search(doc_pattern, script_path.read_text(), re.DOTALL)
            doc_replaced = doc.group(1).strip().replace("\n", " ") if doc else ""
            readme += f'- *{title.group(1)}{":" if doc_replaced else ""}* {doc_replaced}\n'
            
with open(base / "README.md", "w+") as readme_file:
    readme_file.write(readme)

with open(base / "GLYPHS_README.md", "w+") as glyphs_readme_file:
    lines = list(filter(lambda x:len(x), readme.splitlines()))
    for l, line in enumerate(lines):
        match = re.match(r".*#\ ?(.*)", line)
        if match:
            lines[l] = f"\\n**{match.group(1).strip()}**\\n"
    glyphs_readme_file.write("Scripts by Jan Šindler\\n" + "\\n".join(lines))
