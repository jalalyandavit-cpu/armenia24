"""Build the tracked static GitHub Pages site, served from main / (root)."""
from pathlib import Path
import os, runpy, shutil
ROOT=Path(__file__).resolve().parents[1]
os.environ['BASE_PATH']='/armenia24'
runpy.run_path(str(ROOT/'scripts/build.py'))
# Only generated names are replaced. Source folders are never removed.
for source in (ROOT/'dist').iterdir():
    target=ROOT/source.name
    if source.is_dir():
        if target.exists(): shutil.rmtree(target)
        shutil.copytree(source,target)
    else: shutil.copy2(source,target)
print('Exported static GitHub Pages files to repository root: /armenia24/')
