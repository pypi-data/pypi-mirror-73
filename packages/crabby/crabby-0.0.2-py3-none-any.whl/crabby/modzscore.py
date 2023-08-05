import numpy as np

__all__ = ['modified_z_score', 'outliers_modified_z_score']
def modified_z_score(array, axis=-1):
    """Applies a modified z on the inputted array

    :param array: np.array, array to calc mod zscore over
    :param axis: int, axis over which to apply
    :return: modified zscore
    """
    # Below is basically copying how it's done in scipy.stat.zscore
    # .6745 is constant for conversion 
    a = np.asanyarray(array)
    median = np.nanmedian(a, axis=axis)
    median_absolute_deviation = np.nanmedian(np.abs(a - median), axis=axis)

    if axis and median_absolute_deviation.ndim < a.ndim:
        return ((0.6745 * (a - np.expand_dims(median, axis=axis))) /
                np.expand_dims(median_absolute_deviation, axis=axis))
    else:
        return (0.6745 * (a - median)) / median_absolute_deviation


def outliers_modified_z_score(array, threshold=3.5, axis=-1):
    """Return an array to mask at all points that are not outliers

    :param array: np.array, array to calc mod zscore over
    :param threshold: float, value at which to threshold
    :param axis: int, axis over which to apply
    :return: masked_array: array to mask at all points that are not outliers
    """
    modified_z_scores = modified_z_score(array, axis=axis)
    return np.where(np.abs(modified_z_scores) > threshold)
