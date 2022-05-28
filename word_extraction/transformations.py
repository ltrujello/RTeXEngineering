import torch
from skyimage import transform
import math
from torchvision.transforms import Pad, CenterCrop

class CustomPad:
    def __init__(self, output_size: tuple[float, float]):
        self.output_size = output_size
        

    def __call__(self, sample):
        print("CustomPad")
        image = sample['image']

        h, w = image.shape[:2]
        print('original shape', h, w)
        new_h, new_w = self.output_size

        left_pad = 0
        top_pad = 0
        right_pad = 0
        bottom_pad = 0

        if (horiz_pad := new_w - w) > 0:
            print("padding horizontally")
            left_pad = math.ceil(horiz_pad / 2) 
            right_pad = math.floor(horiz_pad / 2) 
            
        if (vertical_pad := new_h - h) > 0:
            print("padding horizontally")
            top_pad = math.ceil(vertical_pad / 2) 
            bottom_pad = math.floor(vertical_pad / 2) 
            
        padding = Pad((left_pad, top_pad, right_pad, bottom_pad), fill=255)
        if isinstance(image, np.ndarray):
            image = torch.from_numpy(image)
        image = padding(image)
        
        print(type(image), (left_pad, top_pad, right_pad, bottom_pad))
        return {'image': image, 'letter': sample["letter"]}
        
class CustomCenterCrop:
    def __init__(self, output_size: tuple[float, float]):
        self.output_size = output_size
        self.torch_center_crop = CenterCrop(output_size)

    def __call__(self, sample):
        print("CustomCenterCrop")
        image = sample["image"]
        if isinstance(image, np.ndarray):
            image = torch.from_numpy(image)
        
        image = self.torch_center_crop(image)
        return {'image': image, 'letter': sample["letter"]}
        

class Rescale(object):
    """Rescale the image in a sample to a given size.

    Args:
        output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image = sample['image']

        h, w = image.shape[:2]
        if isinstance(self.output_size, int):
            if h > w:
                new_h, new_w = self.output_size * h / w, self.output_size
            else:
                new_h, new_w = self.output_size, self.output_size * w / h
        else:
            new_h, new_w = self.output_size

        new_h, new_w = int(new_h), int(new_w)

        img = transform.resize(image, (new_h, new_w))

        return {'image': img, 'letter': sample["letter"]}


class RandomCrop(object):
    """Crop randomly the image in a sample.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        if isinstance(output_size, int):
            self.output_size = (output_size, output_size)
        else:
            assert len(output_size) == 2
            self.output_size = output_size

    def __call__(self, sample):
        image = sample['image']

        h, w = image.shape[:2]
        new_h, new_w = self.output_size

        top = np.random.randint(0, h - new_h)
        left = np.random.randint(0, w - new_w)

        image = image[top: top + new_h,
                      left: left + new_w]

        return {'image': image, 'letter': sample["letter"]}

