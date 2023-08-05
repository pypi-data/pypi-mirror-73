import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

__all__ = ['plot_ts_slide', ]

def plot_ts_slide(x_dat, y_dat, channel='lgnL'):
    """Function that allows for plotting a timeseries with a scrollable x_axis

    :param signal_data: dict, dictionary returned from loadspike2 function
    :param channel: str, channel to load
    :return: matplotlib plot
    """
    # Create figure and axis of plot
    #fig = Figure(figsize=(20, 6))
    fig, ax = plt.subplots(1, figsize=(20, 6))
    plt.subplots_adjust(bottom=.25)

    # Determine boundaries for axises
    y_min, y_max = np.min(y_dat), np.max(y_dat)
    x_min, x_max = np.min(x_dat), np.max(x_dat)

    # Initialize plot
    l, = plt.plot(x_dat, y_dat)
    plt.axis([0, 100, y_min, y_max])

    # Label plot and axises
    plt.title('{} Spikes'.format(channel), fontsize=40)
    plt.xlabel('Time (s)', fontsize=30)
    plt.ylabel('Voltage (μV)', fontsize=30)

    # Create Slider object to change time value
    axpos = plt.axes([.2, .1, .65, .03], facecolor='lightgoldenrodyellow')
    spos = Slider(ax=axpos, label='Time', valmin=.1, valmax=x_max - 100)

    # Throw away function for updating the slider
    def update_xaxis(val):
        pos = spos.val
        ax.axis([pos, pos + 100, y_min, y_max])
        fig.canvas.draw_idle()

    spos.on_changed(update_xaxis)

    return fig