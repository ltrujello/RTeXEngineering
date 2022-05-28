from word_extraction import PDF_Document
from pathlib import Path
import subprocess

data_dir = Path("data/letters")
tex_dir = Path("tex/letters")
pdf_dir = Path("pdf/letters")
tex_dir.resolve().mkdir(exist_ok=True)
pdf_dir.resolve().mkdir(exist_ok=True)
tex_template ="""\\documentclass[12pt,letterpaper]{{article}}
\\usepackage[margin=0.9in]{{geometry}}
\\thispagestyle{{empty}}

\\begin{{document}}
{}
\\end{{document}}\n
"""

letters = [
"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
]

# Generate the pdfs
for letter in letters:
    print(f"Starting for {letter=}")
    tex_contents = tex_template.format(letter)
    letter_dir = tex_dir / f"{letter}"
    letter_dir.resolve().mkdir(exist_ok=True)

    print(f"Making tex dir for {letter=}")
    tex_file = letter_dir / f"{letter}.tex"
    # if tex_file.exists(): 
    #     print(f"Skipping since tex file for {letter=} exists")
    #     continue
    print(f"Writing to tex file for {letter=}")
    with open(tex_file, "w") as f:
        f.write(tex_contents)

    pdf_file = tex_file.parent / f"{letter}.pdf"
    # if pdf_file.exists():
    #     print(f"Skipping since tex file for {letter=} was compiled")
    #     continue

    print(f"Running shell to compile tex file for {letter=}")
    subprocess.run(f"pdflatex -output-directory {tex_file.resolve().parent} {tex_file.resolve()}", shell=True)
    pdf_file.rename(f"{pdf_dir}/{letter}.pdf")

# Generate the letter images and labels for each pdf
for letter in letters:
    pdf_file = pdf_dir / f"{letter}.pdf"
    print(f"Starting word extraction for {letter=}")
    word_extractor = PDF_Document(str(pdf_file), str(data_dir))
    word_extractor.generate_word_data()

    label_file = data_dir / f"{letter}/page_0/sentence_0_0/words/letters/label.txt"
    with open(label_file, "w") as f:
        f.write(f"{letter}")
    


