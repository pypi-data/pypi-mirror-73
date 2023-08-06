
from skimage.segmentation import quickshift, mark_boundaries
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as display


def is_jupyter():
    # ref: https://stackoverflow.com/a/39662359/4834515
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def show_important_parts(image, lime_weights, label=None, segments=None, ratio_superpixels=0.2):
    if label is None:
        label = list(lime_weights.keys())[0]

    if label not in lime_weights:
        raise KeyError('Label not in interpretation')

    if segments is None:
        segments = quickshift(image, sigma=1)

    num_sp = int(ratio_superpixels * len(lime_weights[label]))
    lime_weight = lime_weights[label]
    mask = np.zeros(segments.shape, segments.dtype)
    temp = image.copy()

    fs = [x[0] for x in lime_weight if x[1] > 0][:num_sp]
    for f in fs:
        temp[segments == f, 1] = 255
        mask[segments == f] = 1

    return mark_boundaries(temp, mask)


def visualize_image(image):
    if is_jupyter():
        display.display(display.Image(image))
    else:
        plt.imshow(image)
        plt.show()