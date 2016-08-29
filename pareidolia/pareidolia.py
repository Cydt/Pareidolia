import random
import math

from PIL import Image, ImageFilter
from PIL.ImageOps import autocontrast


# PIL wrappers

def image(filename):
    return Image.open(filename)

def make_grayscale(image):
    return image.convert("L")


def randomize(filenames, size=None, number=None):
    """
    Create a random image from the passed files
    images: list
    size: (x, y)
    """
    # some guards
    if filenames is None or len(filenames) == 0:
        print('Not enough files provided')
        return

    if number is None:
        number = 1

    if size is None:
        size = (400, 200) 

    # copy and shuffle
    shuffled = filenames[:]
    random.shuffle(shuffled)
    
    # pick one base image to fill the canvas
    base = shuffled[0]
    rest = shuffled[1:]

    # create grayscale versions
    images = map(image, shuffled)
    grayscales = list(map(make_grayscale, images))

    # create a new image and paste the grayscales
    combined = list()
    for _ in range(number):
        combined.append(combine_images(grayscales, size=size))

    show_collage(combined)


def show_collage(images):
    width, height = images[0].size
    padding = 10
    collage_size = (width * len(images) + padding * (len(images)-1), height)
    collage = Image.new('L', collage_size)
    
    left = 0
    for img in images:
        collage.paste(img, ((left, 0)))
        left = left + width + padding

    collage.show()

def crop_square(image, size):
    """
    crop a square from a random location in image
    """
    width, height = image.size
    top = random.randint(0, height-size)
    left = random.randint(0, width-size)
    bottom = top + size
    right = left + size

    return image.crop((left, top, right, bottom))

def pythagoras(width, height):
    return math.ceil(math.sqrt(math.pow(width,2) + math.pow(height,2)))

def combine_images(images, size=None):

    width, height = size

    # size for the crop
    radius = pythagoras(*size)
    
    # locations for the paste
    left = int((width - radius) / 2)
    top = int((height - radius) / 2)

    # reusable mask (because opacity is fixed)
    opacity = 100 # out of 255
    mask = Image.new('L', (radius, radius), opacity)

    combined = Image.new('L', size, 'gray')
    for img in images:
        rotation = random.randint(0, 359)

        cropped = crop_square(img, radius)
        rotated = cropped.rotate(rotation, resample=Image.BICUBIC)
        rotated_mask = mask.rotate(rotation)

        combined.paste(rotated, (left, top), rotated_mask)

    combined = autocontrast(combined)

    return combined

