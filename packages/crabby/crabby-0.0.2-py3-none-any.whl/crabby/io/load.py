from neo.io import Spike2IO
import numpy as np
__all__ = ['time2index', 'get_channel_names', 'loadspike2']

def obj2arr(obj):
    """Utility function for conversion of object into numpy array
    obj: neo.core.analogsignal.AnalogSignal; single channel of data
    """
    return np.array(obj).T[0]

def time2index(time, sfreq=4464.285714285715):
    """Returns the index for the array based upon the desired time and sampling frequency

    :param time: int,
    :param sfreq: float, by default should be 4464.285714285715
    :return: index value matched to the relevant time.
    """
    return int(time*sfreq)


def get_signal_proxy(path):
    """Return a proxy signal (see Spike2IO) that can then be further examined

    :param path: str, path to the file
    """
    # Get a reader
    reader = Spike2IO(filename=path, try_signal_grouping=False)#
    # read the block, With updated version .8 you know need to split the channel or it groups by default
    signalproxy = reader.read_segment(lazy=True, signal_group_mode='split-all')
    return signalproxy.analogsignals


def get_channel_names(path):
    """Return the channel names associated with the file

    :param path: str, path to the file
    """
    return [sig.name for sig in get_signal_proxy(path)]


def incorrect_channel(_input, signalproxy):
    """Warn of incorrect channels

    :param _input:
    :param signalproxy:
    :return:
    """
    print('{} not recognized as valid channel, try: \n{}'.format(_input, get_channel_names(signalproxy)))


def load_single_channel(channel_name, path, time_slice=None):
    """Loads a single channel of data

    :param channel_name: str, channel name
    :param path: str, file to data
    :param time_slice: #TODO: Is this used?
    :return:
    """
    for sig in get_signal_proxy(path):
        if sig.name != channel_name:
            continue

        elif sig.name == channel_name:
            data = sig.load(time_slice=time_slice)
            # Load data values
            arr = data.as_array().T[0]
            # Extract sample times
            times = data.times.rescale('s').magnitude
            # Determine channel name
            ch = str(data.name)
            # Extract sampling frequency
            fs = np.float64(data.sampling_rate)
            signal_data = {'channel': ch, 'sampling rate': fs, 'data': arr, 'times': times}
            return signal_data
    # If it could not find the channel then raise an error and print the channels that are valid
    raise ValueError('could not find {} in {}'.format(channel_name, str(get_channel_names(path=path))))


def loadspike2(path, channel_name=None, time_slice=None):
    """Loads spike2 .smr files into a python dictionary
    INPUTS
    ---------
    path: str, path to the file
    channel_name: None, or str; channel name to load, by default all are loaded
    time_slice: tuple; start stop time in seconds of data to load

    OUTPUTS
    ----------
    signal_data: dict, containing relevant data values

    NOTES:
    Currently doesn't do anything for event annotations.
    Compatible with Neo .8
    """

    signal_data = {}

    # read the block, With updated version .8 you know need to split the channel or it groups by default
    if channel_name is not None:
        return load_single_channel(channel_name=channel_name,
                                   path=path,
                                   time_slice=time_slice)

    signal_proxy = get_signal_proxy(path)
    for sig in signal_proxy:
        # Load whole segment
        data = sig.load(time_slice=time_slice)
        # Load data values
        arr = data.as_array().T[0]
        # Extract sample times
        times = data.times.rescale('s').magnitude
        # Determine channel name
        ch = str(data.name)
        # Extract sampling frequency
        fs = np.float64(data.sampling_rate)
        signal_data[ch] = {'channel': ch, 'sampling rate': fs, 'data': arr, 'times': times}
    return signal_data