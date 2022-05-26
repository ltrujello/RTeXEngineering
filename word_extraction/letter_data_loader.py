from torch.utils.data import Dataset, DataLoader
from skimage import io, transform

from pathlib import Path
import pandas as pd

letters = [
"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
]

def get_letter_ind(letter):
    for idx, symbol in enumerate(letters):
        if symbol == letter:
            return idx
    print("Could not find index of {letter=}")
    return None


class LetterDataset(Dataset):
    """Letter dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        """ 
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.letters_frame = pd.read_csv(csv_file)
        self.root_dir = Path(root_dir)
        self.transform = transform

    def __len__(self):
        return len(self.letters_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = self.letters_frame.iloc[idx, 0]
        image = io.imread(img_name)
        letter = self.letters_frame.iloc[idx, 1] 
        letter_ind = get_letter_ind(letter)
        letter_vec = np.zeros(len(letters))
        letter_vec[letter_ind] = 1 
        sample = {"image": image, "letter": letter_vec}
            
        if self.transform:
            sample = self.transform(sample)

        return sample

#        img_name = os.path.join(self.root_dir,
#                                self.landmarks_frame.iloc[idx, 0])
#        image = io.imread(img_name)
#        landmarks = self.landmarks_frame.iloc[idx, 1:]
#        landmarks = np.array([landmarks])
#        landmarks = landmarks.astype('float').reshape(-1, 2)
#        sample = {'image': image, 'landmarks': landmarks}
#
