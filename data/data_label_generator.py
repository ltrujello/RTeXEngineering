from pathlib import Path
import re
import csv

base_dir = ""
letter_file_re = re.compile("^letter_")

csv_file = "labels.csv"
csv_field_names = ["image", "label"]


path = Path(base_dir)
writer = csv.DictWriter(csv_file, csv_field_names)
for p in path.rglob("*"):
    if not p.is_file():
        continue

    is_letter_img = letter_file_re.match(p.name) is None
    if not match_filename:
        continue

    image = p.name
    label_file = p.parent / "label.txt"
    if not label_file.exists():
        print(f"{image=} with parent {p.parent} is missing label.txt")
    label = label_file.read_text()

    writer.write_row({"image": image, "label": label})

