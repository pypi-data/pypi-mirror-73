"""detect.py script used for detection of spikes author loganfickling@gmail.com"""
import numpy as np
from scipy.stats import zscore
import math
# Things that you can import from the file...
__all__ = ['find_consecutive_data', 'find_close_data', 'find_spike_indices', 'realign_spikes', 'find_nearest']

# ------------> Define utility functions for vectorization of code
def find_consecutive_data(data, step=1):
    """Splits Data into a list of arrays when there is more than step (default=1)

    Parameters
    ----------
    data: np.array (of zeroes and ones, True or False, etc.)
          the data to split
    step: int, by default 1

    Returns
    -------
    list of split data
    """
    return np.split(data, np.where(np.diff(data) != step)[0] + 1)


def find_close_data(data, allowable_step=1):
    """Splits Data into a list of arrays where there a adjacent increase greater than allowable_step

    Parameters
    ----------
    data: np.array, the data to split
    allowable_step: int, by default 1

    Returns
    -------
    list of split data
    """
    return np.split(data, np.where(np.diff(data) > allowable_step)[0] + 1)

# ------------> Define spike detection code
def find_spike_indices(data_dict, minimum_isi=.01, minimum_peak=1, maximum_peak=None,
                       zscore_data=True, find_troughs=False, start_time=None, end_time=None):
    """Finds valid extracellular spikes given user-defined constraints
    
    Parameters
    ----------
    data_dict: dict, data of a SINGLE CHANNEL of data with required keys:
         'data', 'times', 'sampling rate', 'channel'
    minimum_isi: int, default=.01(s), minimum amount of time in seconds where another spike 
             is not allowed to be counted as valid
    minimum_peak: int/float, default=1, minimum threshold to be counted as a peak
    maximum_peak: int/float, default=None, value for maximum tolerance of a peak
    zscore_data: bool, default=True, if True converts signal into standard deviations from the mean 
                (i.e. applies a zscore on the data)
    find_troughs: bool, default=False, if True find minimum troughs instead of peaks
    start_time:
    end_time:

    Returns
    --------
    indices_of_spikes: np.array like, indices --in samples-- of valid spike locations
    """
    # ---------> Define variables
    times = data_dict['times']  # Get time values in file
    data = np.array(data_dict['data'], dtype=np.double)
    # ---------> Load Data & Check user option variables
    if zscore_data:  # If they want a zscore do this:
        data = zscore(data, axis=None)
        
    if find_troughs:  # Find troughs instead of peaks by flipping array
        data = -1*data
    # ---------> Calculate relevant thresholds then apply them across the data
    # The following are just boolean arrays with shapes matching the data structure
    above_minimum = data > minimum_peak  # Indices where point is above the minimum spike threshold
    # Don't require a max peak but if there is one provided, include it.
    if maximum_peak is not None:
        below_maximum = data < maximum_peak  # Indices where point is below the maximum spike threshold
        passes_threshold = above_minimum & below_maximum  # Combine the Boolean arrays from above
    # If a maximum peak wasn't provided just use minimum for threshold
    elif maximum_peak is None:
        passes_threshold = above_minimum
    # Find out locations of Indices where signal 1) decreases afterward and 2) is increasing prior to it
    decreasing_after_point = np.append(np.sign(np.diff(data)), 0) < 0
    increasing_to_point = np.sign(np.append(0, np.diff(data))) > 0
    # Combine the boolean arrays, True only where all constraints so far are valid
    defined_constraints = (increasing_to_point & decreasing_after_point & passes_threshold)
    # ---------> Group data by minimum distance allowed before allowing something to count
    # As another spike and then Select only first point of each grouping
    # Don't want to double-count the spikes; minimum amount of time to not count as valid spike
    spike_time_values = np.array([x[0] for x in find_close_data(times[defined_constraints], minimum_isi)])
    # TODO: Use np.apply_along axis and broadcast instead of above?
    # Get indices by checking where there's a match in the corresponding times array; [0] so it's array not tuple
    indices_of_spikes = np.where(np.isin(element=times, test_elements=spike_time_values))[0]
    # If they only want a subset of the detected spikes, give them that subset
    if (start_time is not None) and (end_time is not None):
        locations = np.where((times > start_time) & (times < end_time))
        valid_subset = np.where(np.isin(element=indices_of_spikes, test_elements=locations))[0]
        return indices_of_spikes[valid_subset]

    return indices_of_spikes


def realign_spikes(data, spike_times, samples_around=30):
    """Given raw extracellular data and associated spike times returns an array aligned to the spikes
    
    INPUTS
    ------
    data: np.array like, raw extracellular trace of a single channel (e.g. dgn)
    spike_times: np.array like, spike times generated from find_valid_spikes function
    samples_around: int, 30 by default, number of samples before and after spike peak to grab data
    """
    index_array = np.array([np.arange(val-samples_around, val+samples_around) for val in spike_times])
    spike_values = data[index_array]
    
    return spike_values


def find_nearest(array, value, return_index_not_value=True, is_sorted=True):
    """Given an array and a value, returns either the index or value of the nearest match

    Parameters
    ----------
    array: np.array, array of values to check for matches
    value: int/float, value to find the closest match to
    return_index_not_value: bool, whether to return the index(True) or the value (False)
        of the found match
    is_sorted: bool, whether the array is sorted in order of values
    Returns
    -------
    Either the index or value of the nearest match
    """
    if is_sorted:
        idx = np.searchsorted(array, value, side="left")

        if ((idx > 0) and (idx == len(array)) or (math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx]))):

            if not return_index_not_value:
                return array[idx - 1]

            if return_index_not_value:
                return idx - 1

        else:

            if not return_index_not_value:
                return array[idx]

            if return_index_not_value:
                return idx

    elif not is_sorted:
        idx = (np.abs(array - value)).argmin()

        if not return_index_not_value:
            return array[idx]

        if return_index_not_value:
            return idx

if __name__ == '__main__': # If running the script locally...
    a = np.random.randint(low=0, high=500, size=100)
    # Cool code possibly faster? but way less readable
    # This means check that this point is smaller than neighbor
    smaller_than_neighbor = np.r_[True, a[1:] < a[:-1]] & np.r_[a[:-1] < a[1:], True]
    larger_than_neighbor = np.r_[True, a[1:] > a[:-1]] & np.r_[a[:-1] > a[1:], True]
    #display('array: ', a)
    #display('values smaller than neighbor: ', smaller_than_neighbor)
    #display('values larger than neighbor: ', larger_than_neighbor)