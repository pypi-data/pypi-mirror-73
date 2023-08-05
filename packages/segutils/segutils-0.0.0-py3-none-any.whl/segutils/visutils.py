import matplotlib.pyplot as __plt
import numpy as __np

from .imutils import make_image_binary as __bin_img, is_rgb_image as __is_rgb


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
