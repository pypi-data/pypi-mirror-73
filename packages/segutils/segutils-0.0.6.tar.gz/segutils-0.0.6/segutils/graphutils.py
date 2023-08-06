import matplotlib.pyplot as __plt
from sklearn.metrics import roc_curve as __roc_curve


def plot_keras_history(history, metric='loss', save_path=None, ylim=None):
    """
    plot the training history returned by keras.fit or keras.fit_generator.
    :param history: a history object returned by keras.fit or keras.fit_generator
    :param metric: the name of the metric to plot. must exist as a key for the history.history dictionary.
    :param save_path: if provided, the plot will be saved to this path, otherwise the plot will be displayed.
    :param ylim: a tuple (min_y, max_y) describing the scale of the y axis, if not provided the scale will be
                 determined by the plotted values.
    """
    # prepare figure
    __plt.figure()
    __plt.title(f'{metric.capitalize()} by Epochs')
    __plt.xlabel('Epochs')
    __plt.ylabel(metric.capitalize())
    if ylim:
        __plt.ylim(*ylim)

    # plot metric
    to_plot = history.history[metric]
    __plt.plot(to_plot, label=f'training {metric}')

    # check for validation data and plot if exists
    validation_metric_key = f'val_{metric}'
    if validation_metric_key in history.history:
        __plt.plot(history.history[validation_metric_key], label=f'validation {metric}')
        __plt.legend()  # with 2 plots in the same figure we need a legend in order to distinguish between them

    # save or show figure
    if save_path is None:
        __plt.show()
    else:
        __plt.savefig(save_path)


def roc_curve(ground_truth_masks, probability_maps, save_path=None):
    """
    plots the ROC curve of a model according to a given set of predictions
    :param ground_truth_masks: a numpy array consisting of a mask or stack of masks to be used as the ground truth
                               compared to the actual predictions.
    :param probability_maps: a numpy array containing the predictions of the model on the images corresponding to the
                             `ground_truth_masks` provided.
    :param save_path: if provided, the plot will be saved to this path, otherwise the plot will be displayed.
    :return: a list of thresholds used to acheive the plotted ROC curve.
    """

    assert ground_truth_masks.shape == probability_maps.shape, 'incompatible prediction and label stacks'

    # flatten matrices to vectors
    y_true = ground_truth_masks.reshape(-1)
    y_scores = probability_maps.reshape(-1)

    # calculate ROC curve
    fpr, tpr, thresholds = __roc_curve(y_true, y_scores)

    # prepare figure and plot
    __plt.figure()
    __plt.title('ROC Curve')
    __plt.xlabel("False Positive Rate")
    __plt.ylabel("True Positive Rate")
    __plt.ylim(0, 1)
    __plt.plot(fpr, tpr)

    # save or show figure
    if save_path is None:
        __plt.show()
    else:
        __plt.savefig(save_path)

    return thresholds
