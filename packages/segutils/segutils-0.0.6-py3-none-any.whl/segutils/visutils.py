import colorsys as __colorsys
import random as __random

import matplotlib.pyplot as __plt
import numpy as __np

from .imutils import (make_image_binary as __bin_img,
                      is_rgb_image as __is_rgb,
                      convert_16_bit_to_8_bit as __to_8bit,
                      get_mask_labels as __get_labels)


def generate_rgb_colors(num_colors_to_generate, bright=True, shuffle=True):
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
    :param mask: a binary or labeled mask: a 2D numpy array of positive integers (objects) and 0's (background).
    :param color: a tuple (r, g, b) representing a color in RGB format. if not provided, a random color is generated.
    :param alpha: the opacity of the overlain mask.
    :return: the same as the input image, but with an overlay of the given mask and color.
    """
    # make sure this is a 3 channeled image (RGB format expected)
    image = __to_8bit(image.copy())  # assert image is 8bit
    if image.ndim == 2:  # handle 2D image
        image = __np.stack([image, image, image], axis=-1)
    elif image.ndim != 3:  # assert image with channels
        raise ValueError('input must be a single image')
    elif image.shape[-1] == 1:  # handle single cahnnel grayscale
        image = __np.dstack([image, image, image])
    elif image.shape[-1] != 3:  # assert 3 channels (RGB)
        raise ValueError('only support grayscale and RGB images')

    labels = __get_labels(mask.astype(int))
    if color is None:  # generate 1 color for each label
        color = generate_rgb_colors(len(labels))
    elif len(color) == 3 and isinstance(color[0], int):  # handle single color
        color = [color] * len(labels)

    for l, c in zip(labels, color):  # iterate labels and matching colors
        for channel in range(3):  # iterate each channel to update with mask color
            image[:, :, channel] = __np.where(mask == l,
                                              image[:, :, channel] * (1 - alpha) + alpha * c[channel] * 255,
                                              image[:, :, channel])

    return image


def visual_mask_to_prediction_comparison(image, ground_truth_mask, probability_map, threshold, axes=None):
    """
    crates a visual comparison between a ground truth segmentation and a prediction segmentation. the visualization
    contains 5 images side by side:
        1. the image the segmentation was performed on.
        2. the ground truth mask.
        3. the prediction according to a given threshold (probability_map > threshold).
        4. false positive detection (extras in prediction).
        5. false negative detection (missing in prediction).
    :param image: a numpy array that is the image the segmentation was performed on.
    :param ground_truth_mask: a ground truth binary mask with 0's (background) and 1's (objects)
    :param probability_map: a numpy array containing the prediction of the model on the image.
    :param threshold: the threshold with which to pick objects in the probability map.
    :param axes: a tuple of exactly 5 matplotlib.axes objects in which to show the 5 comparison images. if None, a new
                 figure is created.
    """
    # assert binary image
    ground_truth_mask = __bin_img(ground_truth_mask[None])[0]

    # find the right image color map
    img_cmap = 'viridis' if __is_rgb(image) else 'gray'

    #
    if axes is None:
        _, (ax1, ax2, ax3, ax4, ax5) = __plt.subplots(1, 5, figsize=(100, 100))
    else:
        ax1, ax2, ax3, ax4, ax5 = axes

    pred_mask = (probability_map > threshold).astype(int)

    # remove true objects from pred mask to see extra objects
    extras_in_pred = pred_mask - ground_truth_mask
    extras_in_pred[extras_in_pred < 0] = 0

    # remove pred objects from true mask to see missing objects
    missing_in_pred = ground_truth_mask - pred_mask
    missing_in_pred[missing_in_pred < 0] = 0

    # show image
    ax1.set_title('Input Image', fontsize=150)
    ax1.imshow(image, cmap=img_cmap)

    # show true mask
    ax2.set_title('Ground Truth', fontsize=150)
    ax2.imshow(ground_truth_mask, cmap='gray')

    # show prediction mask
    ax3.set_title('Prediction', fontsize=150)
    ax3.imshow(pred_mask, cmap='gray')

    # show false positives
    ax4.set_title('False Positives', fontsize=150)
    ax4.imshow(extras_in_pred, cmap='gray')

    # show false negatives
    ax5.set_title('False Negatives', fontsize=150)
    ax5.imshow(missing_in_pred, cmap='gray')

    __plt.tight_layout()
    __plt.show()


def plot_image_as_3d_histogram(image, save_path=None, image_title='Image', histogram_title='Histogram'):
    """
    plot an image as a 3d histogram beside itself.
    :param image: a 2D numpy array that is the image to plot
    :param save_path: the path to save the plot to. if None the figure is displayed.
    :param image_title: the title for the image.
    :param histogram_title: the title for the 3d histogram.
    :return:
    """
    # prepare axes
    fig = __plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122, projection='3d')

    # show image
    ax1.imshow(image, cmap='gray')
    ax1.set_title(image_title)

    # create and show bar plot

    ## axes
    h, w = image.shape
    _x = __np.arange(w)
    _y = __np.arange(h)
    _xx, _yy = __np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()

    ## data
    top = image.flatten()
    bottom = __np.zeros_like(top)
    width = depth = 1

    ## plot
    ax2.view_init(30, 70)
    ax2.bar3d(-x, y, bottom, width, depth, top, shade=True)
    ax2.set_title(histogram_title)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')

    fig.tight_layout()

    # save / show figure
    if save_path:
        __plt.savefig(save_path)
    else:
        __plt.show()
    return fig
