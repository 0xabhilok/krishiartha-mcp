import os
import re

html_path = os.path.join("docs", "PITCH_DECK.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Check img sources
img_srcs = re.findall(r'src=["\'](assets/[^"\']+)["\']', content)
print(f"Found {len(img_srcs)} image assets referenced:")
all_exist = True
for src in img_srcs:
    disk_path = os.path.join("docs", src.replace("/", os.sep))
    exists = os.path.exists(disk_path)
    print(f"  {src} -> {disk_path}: exists={exists}")
    if not exists:
        all_exist = False

slides = re.findall(r'<section class=["\']slide', content)
print(f"Total slides found: {len(slides)}")
assert len(slides) == 9, f"Expected 9 slides, found {len(slides)}"
assert all_exist, "All image assets must exist on disk"
print("HTML verification PASSED!")
