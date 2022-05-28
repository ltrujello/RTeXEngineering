from pathlib import Path
import re
import csv

base_dir = Path("data/letters")
letter_file_re = re.compile("^letter_")

csv_file = base_dir / "labels.csv"
csv_field_names = ["image", "label"]
csv_rows = []

for path in base_dir.rglob("*"):
    if not path.is_file():
        continue

    is_letter_img = letter_file_re.match(path.name) is not None
    if not is_letter_img:
        continue

    print(f"Found letter image {path=}")
    label_file = path.parent / "label.txt"
    if not label_file.exists():
        print(f"{image=} with parent {path.parent} is missing label.txt")
        continue
    image = path.resolve()
    label = label_file.read_text()
    row = {"image": image, "label": label}
    csv_rows.append(row)

print("Creating the csv label file")
with open(csv_file, "w") as f:
    writer = csv.DictWriter(f, csv_field_names)
    writer.writeheader()
    for row in csv_rows:
        writer.writerow(row)


