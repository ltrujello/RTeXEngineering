import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path

class PDF_Document:
    def __init__(self, pdf_file: str, data_path: str) -> None:
        """ A class to process the PDF of a tex_document and to implement its letter extraction
        """
        self.pdf_file = Path(pdf_file)  # Path to the pdf file
        self.data_dir = Path(data_path)  # Path to data directory

        self.pdf_file_str = str(self.pdf_file.resolve())
        self.data_dir_str = str(self.data_dir.resolve())

    def generate_word_data(self) -> None:
        """
            If the pdf file has filename "tex_filename" and has n many pages, then this method will
            build a directory structure as below with the png data representing words.

                    |--- ...             |-- page_0/ |-- sentences_0_0/ |-- word_0_0_0/ |-- letters/ (also contains word_0_0_0.png)
                    |                    |   ...         ...                            ...
            data/ --|--- tex_filename/--- |-- page_i/ |-- sentences_i_0/ |-- word_i_0_0 |-- letters/ 
                    |                    |   ...         ...                            ...
                    |--- ...             |-- page_n/ |-- sentences_n_0/ |-- word_n_0_0 |-- letters/
        """
        pdf_fp = str(self.pdf_file.resolve())
        page_pngs = convert_from_path(pdf_fp, 500)  # Create the png of the pdf (500 = resolution argument)
        for i, png in enumerate(page_pngs):
            page_dir = self.data_dir / self.pdf_file.stem / f"page_{i}/"
            page_dir.resolve().mkdir(parents=True, exist_ok=True)  # Create the page directory
            page_img = self.data_dir / self.pdf_file.stem / f"page_{i}.png"
            png.save(str(page_img.resolve()), 'PNG')  # Save the pdf PNG in the directory

            # Find the sentences in the page
            sentences = sentences_in_page(img_to_array(str(page_img.resolve())))
            for j, sentence in enumerate(sentences):
                sentence_dir = page_dir / f"sentence_{i}_{j}/"
                sentence_dir.resolve().mkdir(exist_ok=True)  # Create the sentence directory
                sentence_img = Image.fromarray(sentence).convert('L')
                sentence_img.save(str(sentence_dir / f"sentence_{i}_{j}.png"))  # Save the sentence image

                # Find the words in the sentence
                words = words_in_sentence(sentence)
                for k, word in enumerate(words):
                    word_dir = sentence_dir / "words/"
                    word_dir.resolve().mkdir(exist_ok=True)  # Create the words directory
                    word_img = Image.fromarray(word).convert('L')
                    word_img.save(str(word_dir / f"word_{i}_{j}_{k}.png")) # Save the word image

                    letters = letters_in_word(word)
                    for l, letter in enumerate(letters):
                        letter_dir = word_dir / "letters/"
                        letter_dir.resolve().mkdir(exist_ok=True)  # Create the letters directory
                        letter_img = Image.fromarray(letter).convert('L')
                        letter_img.save(str(letter_dir / f"letter_{i}_{j}_{k}_{l}.png")) # Save the letter image


def img_to_array(img_file: str) -> np.array:
    """ Load image in as np.array.
    """
    image = Image.open(img_file).convert('L')
    w, h = image.size
    data = np.array(list(image.getdata()), dtype=np.uint8).reshape(h, w) # store values to numpy array
    return data


def sentences_in_page(page: np.array) -> list[np.array]:
    # Given a pixel array representing an image of a single page, we return a list of pixel arrays,
    # obtained from the image of the page, which represent the sentences in the page.
    row_ind = 0
    sentences = []
    while row_ind < len(page) - 1:
        sentence = []
        row = page[row_ind].reshape(1, len(page[row_ind]))  # reshape for vstack
        sentence.append(row)
        j = row_ind
        while j < len(page) - 1:  # -1 since we grab two rows at a time
            row1 = page[j].reshape(1, len(page[j]))
            row2 = page[j + 1].reshape(1, len(page[j + 1]))

            # We now examine what pixels in the rows are nonwhite
            row1_nonwhite = (row1 < 230).astype("int")  # Cast bool values to 1s and 0s
            row2_nonwhite = (row2 < 230).astype("int")
            # Take their dot product and check if it's zero; it's nonzero if we're scanning a set of letters.
            if np.inner(row1_nonwhite, row2_nonwhite) != 0:
                sentence.append(row2)
                j += 1
            else:
                break
        row_ind += len(sentence)
        if len(sentence) > 2:
            sentences.append(sentence)

    sentence_arrays = []
    # We now stack our rows of pixel data to create sentences, and return the list of sentences.
    for sentence in sentences:
        array = sentence[0]
        for row_ind in range(1, len(sentence)):
            array = np.vstack((array, sentence[row_ind]))
        sentence_arrays.append(array.astype('uint8'))
    return sentence_arrays


def words_in_sentence(sentence: np.array) -> list[np.array]:
    """ Given a pixel array representing an image single sentence, we look for and extract the columns
    of pixels which represent words in the sentence.
    """
    sentence = sentence.T
    sentence_h = sentence.shape[1]
    i = 0
    words = []
    while i < len(sentence) - 1:
        word = []
        word.append(sentence[i].reshape(sentence_h, 1))  # Reshape for hstack later
        j = i
        while j < len(sentence) - 1:
            col1 = sentence[j]
            col2 = sentence[j + 1]

            col1_nonwhite = (col1 < 230).astype('int')
            col2_nonwhite = (col2 < 230).astype('int')
            """
            The second condition after the or is basically saying: Is there any 
            nonwhite space in the next 15 consecutive pixels at all
            """
            if int(np.inner(col1_nonwhite, col2_nonwhite)) != 0 or np.sum(sentence[j:j + 15] < 230 * 1) != 0:
                j += 1
                word.append(col2.reshape(sentence_h, 1))  # Reshape for hstack later
            else:
                break
        i += len(word)
        if len(word) > 2:  # Too small to be of any relevant detail to the eye
            words.append(word)

    word_arrays = []
    for word in words:
        array = word[0]
        for i in range(1, len(word)):
            array = np.hstack((array, word[i]))
        word_arrays.append(array.astype('uint8'))
    return word_arrays

def letters_in_word(word: np.array) -> list[np.array]:
    """ Given a pixel array representing an image of a single word, we look for and extract the columns
    of pixels which represent letters in the word.
    """
    word = word.T
    word_h = word.shape[1]
    i = 0
    letters = []
    while i < len(word) - 1:
        letter = []
        letter.append(word[i].reshape(word_h, 1))  # Reshape for hstack later
        j = i
        while j < len(word) - 1:
            col1 = word[j]
            col2 = word[j + 1]

            col1_nonwhite = (col1 < 230).astype('int')
            col2_nonwhite = (col2 < 230).astype('int')

            if int(np.inner(col1_nonwhite, col2_nonwhite)) != 0:
                j += 1
                letter.append(col2.reshape(word_h, 1))  # Reshape for hstack later
            else:
                break
        i += len(letter)
        if len(letter) > 2:  # Too small to be of any relevant detail to the eye
            letters.append(letter)

    letter_arrays = []
    for letter in letters:
        array = letter[0]
        for i in range(1, len(letter)):
            array = np.hstack((array, letter[i]))
        letter_arrays.append(array.astype('uint8'))
    return letter_arrays


