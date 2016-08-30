import random
import math

from PIL import Image, ImageFilter
from PIL.ImageOps import autocontrast

from .types import Size, Dimensions


# PIL wrappers

def image(filename):
    return Image.open(filename)

def make_grayscale(image):
    return image.convert("L")


def combine(filenames, size=None, number=None, dimensions=None):
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

    # dimensions overrules number
    if dimensions is None:
        dimensions = Dimensions(1, number)
    else:
        number = dimensions.rows * dimensions.columns

    if size is None:
        size = Size(400, 200) 

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

    show_collage(combined, dimensions)


def show_collage(images, dimensions):
    width, height = images[0].size
    rows, columns = dimensions

    padding = 10

    collage_size = (
        width * columns + padding * (columns-1),
        height * rows + padding * (rows-1)
    )
    collage = Image.new('L', collage_size)
    
    for row in range(rows):
        top = row * (height + padding)
        for col in range(columns):
            left = col * (width + padding)
            idx  = row*columns + col
            collage.paste(images[idx], ((left, top)))

    collage.show()

def crop_square(image, size):
    """
    crop a square from a random location in image
    """
    width, height = image.size
    top = random.randint(0, max(0, height-size))
    left = random.randint(0, max(0, width-size))
    bottom = min(top + size, height)
    right = min(left + size, width)

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

