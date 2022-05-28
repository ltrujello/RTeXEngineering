from word_extraction.transforms import CustomPad
from word_extraction.datasets import LetterDataset
from torchvision.transforms import RandomCrop, Compose

import hashlib

letter_data_base = "/data/letter_dataset/"

letters = [ 
"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
]

# Build the directory skeleton if not already there
for letter in letters:
    letter_dir = letter_data_base / letter
    letter_dir.mkdir(exists_ok=True)

trans = transforms.Compose([
    CustomPad((100, 100)), 
    RandomCrop((80, 80)),
]
letter_dataset = LetterDataset("data/letters/labels.csv", "asda", trans)

# Generate 20 randomly cropped copies of our current dataset
for i in range(20):
    for idx in range(len(letter_dataset)):
        letter_img = letter_dataset[idx]["image"]
        label = letter_dataset[idx]["label"]
        letter_hash = hashlib.md5(letter_img).hexdigest()
        letter_path = letter_data_base / label / f"{label}_{letter_hash}.png"

        if letter_path.exists():
            continue

        letter_img = Image.fromarray(letter_img)
        letter_img.save(letter_path)
        

