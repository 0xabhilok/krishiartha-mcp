import pptx
from pptx.util import Inches, Pt

prs = pptx.Presentation("docs/KrishiArtha_MCP_Pitch_Deck.pptx")
print(f"Presentation has {len(prs.slides)} slides. Dimensions: {prs.slide_width.inches:.2f} x {prs.slide_height.inches:.2f} in\n")

for i, slide in enumerate(prs.slides):
    print(f"==================================================")
    print(f"SLIDE {i+1}")
    print(f"==================================================")
    for j, shape in enumerate(slide.shapes):
        pos = f"pos=({shape.left.inches:.2f}, {shape.top.inches:.2f}, {shape.width.inches:.2f}, {shape.height.inches:.2f})"
        if shape.has_text_frame:
            text = "\n".join([p.text for p in shape.text_frame.paragraphs if p.text.strip()])
            if text:
                print(f"  Shape {j+1} [TEXT] {pos}:")
                for line in text.split("\n"):
                    print(f"    | {line}")
        elif shape.has_table:
            tbl = shape.table
            print(f"  Shape {j+1} [TABLE] {pos}: {len(tbl.rows)} rows x {len(tbl.columns)} cols")
            for r_idx, row in enumerate(tbl.rows):
                row_str = " | ".join([c.text.strip().replace("\n", " ") for c in row.cells])
                print(f"    R{r_idx}: {row_str}")
        else:
            print(f"  Shape {j+1} [{shape.name} / {shape.shape_type}] {pos}")
    print()
