from collections.abc import Iterable

import matplotlib.patches as patches
import matplotlib.pyplot as plt

from .imutils import is_rgb_image

# default box color
DEFAULT_BOX_COLOR = 'red'


class Visualizer:
    """
    A visualization tool for segmentation datasets and results
    """

    def __init__(self, image):
        """
        Initialize a Visualizer object.
        :param image: a 2d or 3d image grayscale or RGB image
        """
        self.image = image.copy()
        self.cmap = 'viridis' if is_rgb_image(image) else 'gray'
        self.bboxes = {}

    def add_bbox(self, idx, box, padding=0, color=DEFAULT_BOX_COLOR):
        """
        add a bounding box to the final figure.
        :param idx: the index or key that describes the boxed object
        :param box: a tuple (x_min, y_min, x_max, y_max) defining a bounding box in the image
        :param padding: padding to add to each side of the bounding box (default 0)
        :param color: the color of the bounding box to add (default "red")
        :return: self
        """
        x_min, y_min, x_max, y_max = box
        self.bboxes.setdefault(color, {})[idx] = x_min - padding, y_min - padding, x_max + padding, y_max + padding
        return self

    def add_bbox_stack(self, boxes, indices=None, padding=0, color=DEFAULT_BOX_COLOR):
        """
        add a stack of bounding boxes of a certain color to the final figure.
        :param boxes: either a list of boxes or a dictionary (index --> box), where a box is a tuple
                      (x_min, y_min, x_max, y_max) defining a bounding box in the image
        :param indices: an iterable containing the indices for each of the given boxes. if `boxes` is a dictionary this
                        value is ignored. if `boxes` is a list then we use the indices for each corresponding box. if
                        this is None then we use range(1, len(boxes) + 1).
        :param padding: padding to add to each side of the bounding box (default 0).
        :param color: the color of the bounding box to add (default "red") .
        :return: self
        """
        if isinstance(boxes, dict):
            indices = boxes.keys()
            boxes = boxes.values()
        elif indices is None:
            indices = range(1, len(boxes) + 1)
        for idx, box in zip(indices, boxes):
            self.add_bbox(idx, box, padding, color)
        return self

    def remove_bbox(self, idx, color=DEFAULT_BOX_COLOR):
        """
        removes a bounding box from the final figure.
        :param idx: the index of the box to remove
        :param color: the color of the box to remove (default "red")
        :return: self
        """
        self.bboxes[color].pop(idx)
        return self

    def remove_bbox_stack(self, indices, color=DEFAULT_BOX_COLOR):
        """
        removes a stack of bounding boxes of a certain color from the final figure.
        :param indices: an iterable containing indices of bounding boxes to remove
        :param color: the color of the bounding boxes to remove (default "red")
        :return:
        """
        for idx in indices:
            self.remove_bbox(idx, color)
        return self

    def show(self, idx=None, color=None, plot_title=''):
        """
        creates the figure defined by the image and operations performed on this object and displays it.
        :param idx: one of the following:
                    - a dctionary (c --> i where c is an existing bounding box color and i is an existing index or
                      iterable of indices in color c.
                    - an iterable of keys existing in all colors mentioned in all colors mentioned in `color`.
                    - a single index that has an existing bounding box in all colors mentioned in `color`.
                    - None. in this case, all existing indices are shown in all colors mentioned in `color`.
        :param color: one of the following:
                      - an iterable of matplotlib colors that some boudning box has been registered under it at some
                        point.
                      - a string matplotlib color that some boudning box has been registered under it at some
                      - None. in this case, all colors are shown
        :param plot_title: a title to add to the final figure (default no title)
        :return: self
        """
        self.create_figure(idx, color, plot_title)
        plt.show()
        return self

    def save(self, path, idx=None, color=None, plot_title=''):
        """
        creates the figure defined by the image and operations performed on this object and saves it to the given path.
        :param path: the path in which to save the image (the file extension will define the save format).
        :param idx: one of the following:
                    - a dctionary (c --> i where c is an existing bounding box color and i is an existing index or
                      iterable of indices in color c.
                    - an iterable of keys existing in all colors mentioned in all colors mentioned in `color`.
                    - a single index that has an existing bounding box in all colors mentioned in `color`.
                    - None. in this case, all existing indices are shown in all colors mentioned in `color`.
        :param color: one of the following:
                      - an iterable of matplotlib colors that some boudning box has been registered under it at some
                        point.
                      - a string matplotlib color that some boudning box has been registered under it at some
                      - None. in this case, all colors are shown
        :param plot_title: a title to add to the final figure (default no title)
        :return: self
        """
        fig, ax = self.create_figure(idx, color, plot_title)
        fig.savefig(path)
        return self

    def create_figure(self, idx=None, color=None, plot_title=''):
        """
        creates the figure defined by the image and operations performed on this object.
        :param idx: one of the following:
                    - a dctionary (c --> i where c is an existing bounding box color and i is an existing index or
                      iterable of indices in color c.
                    - an iterable of keys existing in all colors mentioned in all colors mentioned in `color`.
                    - a single index that has an existing bounding box in all colors mentioned in `color`.
                    - None. in this case, all existing indices are shown in all colors mentioned in `color`.
        :param color: one of the following:
                      - an iterable of matplotlib colors that some boudning box has been registered under it at some
                        point.
                      - a string matplotlib color that some boudning box has been registered under it at some
                      - None. in this case, all colors are shown
        :param plot_title: a title to add to the final figure (default no title)
        :return: a tuple (fig, ax) of the created figure.
        """
        idx, color = self.__normalize_params(idx, color)

        # create new figure in the correct size
        dpi = 80
        height, width = self.image.shape[:2]
        figsize = height / float(dpi), width / float(dpi)
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        if plot_title:
            ax.set_title(plot_title)
        ax.axis('off')

        # show image
        ax.imshow(self.image, cmap=self.cmap)

        # show boxes
        for c in color:
            boxes_to_show = [(i, self.bboxes[c][i]) for i in idx[c]]
            for i, box in boxes_to_show:
                # create bbox object
                x_min, y_min, x_max, y_max = box
                rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, edgecolor=c, facecolor='none')
                ax.add_patch(rect)

                # create text object
                if y_min > 100:
                    vertical_alignment = 'bottom'
                    x, y = x_min, y_min
                else:
                    vertical_alignment = 'top'
                    x, y = x_min, y_max
                ax.text(x, y, str(i), color='white', verticalalignment=vertical_alignment)

        return fig, ax

    def __normalize_params(self, idx, color):
        """
        normalize the index and color parameters from the figure creation functions to one unified API. in order to
        allow for multiple combinations of `idx` and `color` parameters. also check for compatibility between the
        parameters.
        :param idx: a key, an iterable of keys, or a dictionary (c --> indices) where i is a color and indices
                    are either a single index or an iterable of them, or None
                    color
        :param color: color can be a string describing a matplotlib color, an iterable of such strings, or None
        :return: idx, color in the following format:
                 idx - return a dictionary (c --> indices) where c is a color and indices are an iterable of bounding
                       box indices in color c to remove.
                 color - return an iterable of matplotlib color strings
        """
        # if no color is given, take
        if color is None:
            if isinstance(idx, dict):
                color = idx.keys()  # idx is dict, use color keys
            else:
                color = self.bboxes.keys()  # idx is not dict, use all bounding box keys

        # generalize single object to collection
        if not isinstance(color, Iterable) or isinstance(color, str):
            color = [color]

        # check for irrelevant color
        for c in color:
            assert c in self.bboxes, f'color {c} has not yet been added'

        if idx is None:
            idx = {c: self.bboxes[c].keys() for c in color}

        # generalize single object to collection on default color
        if not isinstance(idx, Iterable):
            idx = {c: [idx] for c in color}
        elif not isinstance(idx, dict):
            idx = {c: idx for c in color}
        elif isinstance(idx, dict):
            for c, i in idx.items():
                if not isinstance(i, Iterable):
                    idx[c] = [i]

        assert isinstance(idx, dict), 'expected key, an iterable of keys, or a dictionary with idx for each color'

        for c in idx:
            assert c in self.bboxes, f'color {c} has not yet been added'
            for i in idx[c]:
                assert i in self.bboxes[c], f'color {c} does not have idx {i}'

        return idx, color
