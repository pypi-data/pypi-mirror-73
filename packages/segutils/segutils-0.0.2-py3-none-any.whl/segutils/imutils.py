import colorsys as __colorsys
import random as __random
from math import ceil as __ceil

import mahotas as __mh
import numpy as __np


def label_mask(mask):
    """
    labels a single binary mask.
    :param mask: a 2D numpy array of 1's (objects) and 0's (background).
    :return: a numpy array of the same shape as `mask` where all connected components in the mask have each been labeled
             with a unique integer, where 0 represents the background.
    """
    labeled_msk, _ = __mh.label(mask)
    return labeled_msk


def label_mask_stack(stack):
    """
    label a stack of binary masks.
    :param stack: a stack of 2D numpy arrays of 1's (objects) and 0's (background).
    :return: a numpy array of the same shape as `stack` where all connected components in each mask have each been
             labeled with a unique integer, where 0 represents the background.
    """
    labeled_masks = []
    for mask in stack:
        labeled_masks.append(label_mask(mask))

    return __np.stack(labeled_masks)


def get_mask_labels(labeled_mask, background_idx=0):
    """
    returns the integer labels of the objects in a labeled mask.
    :param labeled_mask: a 2D numpy array of type `int` consisting of labeled segmented objects.
    :param background_idx: the index of the image background as it appears in `labeled_mask` (default 0). if None is
                           given, it is considered that there is no background and all labels will be returned.
    :return: a numpy array consisting of the sorted object label values.
    """
    labels = __np.unique(labeled_mask)

    if background_idx is None:
        return labels

    if background_idx in labels:
        labels = __np.delete(labels, background_idx)

    return labels


def get_bbox_for_object(labeled_mask, object_idx=1, padding=0):
    """
    get the rectangular border of a specific object in a labeled mask.
    :param labeled_mask: a 2D numpy array of type `int` consisting of labeled segmented objects.
    :param object_idx: the label of the object to extract from the mask (default 1).
    :param padding: the amount of padding to add to each side of the box (default 0).
    :return: a tuple (min_x, min_y, max_x, max_y) representing the top left and bottom right corners of the bounding
             box.
    """
    # extract desired object from mask
    obj_msk = (labeled_mask == object_idx).astype(int)

    # find bbox
    min_y, max_y, min_x, max_x = __mh.bbox(obj_msk)

    # add padding
    min_y, max_y, min_x, max_x = min_y - padding, max_y + padding, min_x - padding, max_x + padding

    # assert that the box boundaries are within the mask's boundaries
    rows, cols = labeled_mask.shape
    min_y, max_y = __np.max((0, min_y)), __np.min((rows, max_y))
    min_x, max_x = __np.max((0, min_x)), __np.min((cols, max_x))

    return min_x, min_y, max_x, max_y


def get_bbox_for_all_objects(labeled_mask, padding=0, background_idx=0):
    """
    get the rectangular border of all objects in a labeled mask. 0 is considered to be the background
    :param labeled_mask: a 2D numpy array of type `int` consisting of labeled segmented objects.
    :param padding: the amount of padding to add to each side of the boxes (default 0).
    :param background_idx: the index of the image background as it appears in `labeled_mask` (default 0). if None is
                           given, it is considered that there is no background and all labels will be returned.
    :return: a dictionary of the form label --> bbox where "label" is the integer value of the object in the given
             `labeled_mask` and "bbox" is a tuple (min_x, min_y, max_x, max_y) representing the top left and bottom
             right corners of the bounding box.
    """
    boxes = {}
    obj_indices = get_mask_labels(labeled_mask, background_idx)
    for i in obj_indices:
        boxes[i] = get_bbox_for_object(labeled_mask, i, padding)

    return boxes


def get_bbox_for_all_objects_in_stack(labeled_mask_stack, padding=0, background_idx=0):
    """
    get the rectangular border of all objects in a labeled mask. 0 is considered to be the background
    :param labeled_mask_stack: a stack of 2D numpy array of type `int` consisting of labeled segmented objects.
    :param padding: the amount of padding to add to each side of the boxes (default 0).
    :param background_idx: the index of the image background as it appears in `labeled_mask` (default 0). if None is
                           given, it is considered that there is no background and all labels will be returned.
    :return: a dictionary of the form label --> bbox where "label" is the integer value of the object in the given
             `labeled_mask` and "bbox" is a tuple (min_x, min_y, max_x, max_y) representing the top left and bottom
             right corners of the bounding box.
    """
    boxes_stack = []
    for msk in labeled_mask_stack:
        boxes_stack.append(get_bbox_for_all_objects(msk, padding, background_idx))

    return boxes_stack


def crop_out_object(labeled_mask, object_idx=1, image_to_crop=None, padding=0):
    """
    crops out a specific object from a labeled mask.
    :param labeled_mask: a 2D numpy array of type `int` consisting of labeled segmented objects.
    :param object_idx: the label of the object to extract from the mask (default 1).
    :param image_to_crop: a numpy array representing a single, "channels last" format image. if provided, the returned
                          crop is taken from this image. otherwise, the crop is taken from the labeled mask.
    :param padding: the amount of padding to add to each side of the box (default 0).
    :return: a numpy array that is the cropped out object from the desired image (`image_to_crop` if provided, else
             `labeled_mask`).
    """
    assert image_to_crop is None or labeled_mask.shape == image_to_crop.shape

    # get bounding box for object
    min_x, min_y, max_x, max_y = get_bbox_for_object(labeled_mask, object_idx, padding)

    # crop labeled mask or image to crop
    if image_to_crop is None:
        return labeled_mask[min_y:max_y, min_x:max_x]
    else:
        return image_to_crop[min_y:max_y, min_x:max_x]


def mask_out(image, mask):
    """
    pushes an image through a mask, making everything 0 except the masked area.
    :param image: the image to mask.
    :param mask: a 2D numpy array of 1's (keep) and 0's (throw).
    :return: a numpy array of the same shape as `image` such that at points where `mask` is 0 the output is also 0 and
             at points where `mask` is 1 the output is the same as `image` in the same points.
             example:
                      |1 2 3|  |0 1 0|    |0 2 0|
             mask_out(|4 5 6|, |0 0 1|) = |0 0 6|
                      |7 8 9|  |1 0 1|    |7 0 9|
    """
    assert image.shape[:2] == mask.shape, "image and mask must have the same dimensions"

    # copy image so as not to
    out = image.copy()
    out[~mask] = 0
    return out


def generate_rgb_colors(num_colors_to_generate, bright=True, shuffle=False):
    """
    generates a list of RGB colors that are as different as possible.
    in order to not assume the number of bits used, the returned RGB values are between 0 and 1, and can be converted
    to 8bit (for example) by multiplying each value by 255
    :param num_colors_to_generate: the number of colors to generate.
    :param bright: determines if to use bright or dark colors.
    :param shuffle: if True, shuffles the colors randomly before outputting.
    :return: a list of tuples (r, g, b) representing the RGB value of each color. values are between 0 and 1.
    """
    # choose brightness
    brightness = 1.0 if bright else 0.7

    # create HSV triplets (easier to generate with big difference between colors)
    hsv = [(i / num_colors_to_generate, 1, brightness) for i in range(num_colors_to_generate)]

    # convert to rgb
    colors = list(map(lambda c: __colorsys.hsv_to_rgb(*c), hsv))

    # shuffle if necessary
    if shuffle:
        __random.shuffle(colors)

    return colors


def apply_mask(image, mask, color=None, alpha=0.5):
    """
    apply a mask to a given image
    :param image: an RGB image in "channels last" format to apply the mask to.
    :param mask: a binary mask: a 2D numpy array of 1's (objects) and 0's (background).
    :param color: a tuple (r, g, b) representing a color in RGB format. if not provided, a random color is generated.
    :param alpha: the opacity of the overlain mask.
    :return: the same as the input image, but with an overlay of the given mask and color.
    """
    if color is None:
        color = generate_rgb_colors(1)[0]

    image = convert_16_bit_to_8_bit(image.copy())  # assert image is 8bit
    if image.ndim == 2:
        image = __np.stack([image, image, image], axis=-1)
    elif image.ndim != 3:
        raise ValueError('input must be an image')
    elif image.shape[-1] == 1:
        image = __np.dstack([image, image, image])
    elif image.shape[-1] != 3:
        raise ValueError('only support grayscale and RGB images')

    for c in range(3):
        image[:, :, c] = __np.where(mask != 0,
                                    image[:, :, c] * (1 - alpha) + alpha * color[c] * 255,
                                    image[:, :, c])
    return image


def convert_16_bit_to_8_bit(image):
    """
    downgrade image from 16 bit to 8 bit quality while preserving maximum information.
    :param image: a numpy array of dtype uint16 or uint8.
    :return: `image` downgraded to (or kept the same at) uint8.
    """
    if image.dtype == __np.uint16:
        return (image / 256).astype(__np.uint8)
    elif image.dtype == __np.uint8:
        return __np.copy(image)
    else:
        raise ValueError('input must be of type uint16 or uint8')


def make_image_binary(image):
    """
    turn a stack of 2 valued images into a binary 0,1 valued image.
    :param image: a numpy array consisting of 2 or less unique values.
    :return: an image like the given `image` containing only the values 0 and 1. if there are 2 values in the image
             then the minimum will be transformed to 0's and the maximum to 1's. if only 1 value is available then if
             it is 0 return all 0's, otherwise return all 1's
    """
    # find image values
    img_vals = __np.unique(image)
    assert img_vals.size <= 2, f'image is not a binary image'

    if img_vals.size == 1 and img_vals[0] > 0:
        # image has only 1 value greater than 0. use full image mask
        out_img = __np.ones_like(image)
    else:
        # make low value idx 0 and high value idx 1
        low_val_mask = image == min(img_vals)

        out_img = __np.empty_like(image)
        out_img[low_val_mask] = 0
        out_img[~low_val_mask] = 1

    return out_img.astype(__np.uint8)


def make_stack_binary(stack):
    """
    turn a stack of 2 valued images into a binary 0,1 valued image
    :param stack: a numpy array object of shape (stack_size, rows_dim, cols_dim, ...)
    :return: a numpy array of shape (stack_size, rows_dim, cols_dim, ...) conatining only the values 0 and 1
    """
    output = []
    for i, img in enumerate(stack):
        try:
            out_img = make_image_binary(img)
        except AssertionError:
            raise AssertionError(f'image {i} is not a binary image')
        output.append(out_img)

    return __np.stack(output).astype(__np.uint8)


def factor_pad_stack(stack, factor=5):
    """
    Many segmentation models require that the images down-sampled a certain number of times. In these cases the image
    dimensions must divide by 2 by at least as many times as it is to be downsized.
    This function pads the image stack's dimensions in order make the images divisible by 2 enough times.
    :param stack: a numpy array of shape (stack_size, rows_dim, cols_dim, ...).
    :param factor: the number of times the image is expected to be down-sampled.
    :return: the stack, minimally padded with zeros to the bottom and right such that the dimensions of the output are
             divisible by 2 `factor` times.
    """
    # get num of images and image dimensions
    n, image_height, image_width = stack.shape[:3]

    # calculate the number that we should be able to divide by
    divisor = 2 ** factor

    # find closest multiple of the divisor to the image dimensions
    min_image_height = int(divisor * __ceil(image_height / divisor))
    min_image_width = int(divisor * __ceil(image_width / divisor))

    # create zeros matrix with the new minimum dimensions
    out = __np.zeros((n, min_image_height, min_image_width, *stack.shape[3:]), dtype=stack.dtype)

    # give the top left of the zeros matrix the values of the original image
    out[:, :image_height, :image_width] = stack

    return out


def make_3d_grayscale(img):
    """
    convert grayscale image to RGB by using the image in every channel.
    :param img: an image or stack of images
    :return: the image(s) converted to RGB format. if img.shape[-1] is 3, the image is returned as is
    """
    if img.shape[-1] == 3:  # already 3 channels
        return img.copy()

    if img.shape[-1] == 1:  # remove channel dim for grayscale image
        img = img[..., 0]

    return __np.stack([img, img, img], axis=-1).astype(img.dtype)


def is_rgb_image(image):
    """
    determines whether a given image is in RGB "channels last" format
    :param image:
    :return:
    """
    return image.ndim == 3 and image.shape[-1] == 3


def normalize_zero_center(x):
    """
    normalize vector / matrix to mean 0 and std 1: (x - mean(x)) / std(x).
    if the standard deviation of `x` is 0, an ZeroDivisionError will be raised.
    :param x: a numpy array.
    :return: x normalized to mean 0 and std 1
    """
    x = x - x.mean()
    x = x / x.std()
    return x


def normalize_min_max(x, min_val=None, max_val=None):
    """
    normalize vector / matrix to [0, 1].
    :param x: a numpy array.
    :param min_val: the minimum value in normalization. if not provided, takes x.min()
    :param max_val: the maximum value in normalization. if not provided, takes x.max()
    :return:
    """
    if min_val is None:
        min_val = x.min()
    if max_val is None:
        max_val = x.max()

    return (x - min_val) / (max_val - min_val)
