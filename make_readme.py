from pathlib import Path
import re

base = Path(__file__).parent

with open(base / 'README.md', 'w') as readme_file:
    readme_file.write('| Folder | Script | Description |\n')
    readme_file.write('| --- | --- | --- |\n')
    for folder in sorted(base.iterdir(), key=lambda x: x.name):
        if folder.is_dir() and not folder.name.startswith('.'):
            readme_file.write(f'| __{folder.stem.capitalize()}__ |\n')
            for script_path in sorted(folder.glob("*.py"), key=lambda x: x.name):
                if script_path.stem.startswith("__"):
                    continue
                title = re.match(r"#\ ?MenuTitle: (.*)", script_path.read_text()) 
                doc_pattern = r'__doc__\s*=\s*"""(.*?)"""'
                doc = re.search(doc_pattern, script_path.read_text(), re.DOTALL)
                readme_file.write(f'| | {title.group(1)} | {doc.group(1).strip().replace("\n", " ") if doc else ""} |\n')
            