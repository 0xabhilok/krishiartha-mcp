import os
from PIL import Image

assets_dir = "docs/assets"
for f in sorted(os.listdir(assets_dir)):
    p = os.path.join(assets_dir, f)
    if os.path.isfile(p):
        try:
            im = Image.open(p)
            print(f"{f}: format={im.format}, size={im.size}, bytes={os.path.getsize(p)}")
        except Exception as e:
            print(f"{f}: {e}")
