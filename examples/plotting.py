import numpy as np

from matplotlib.pyplot import figure


def multiple_time_series(events, labels, times):
    """
    Creates a plot of multiple time series given.
    :param events:  2D (numpy) array with actual event values
    :param labels:  list (len = events.ndim[0]) with label for every time serie
    :param times:   1D (numpy) array with times
    """
    fig = figure(figsize=(8, 6))

    title = 'Input (top) and map (bottom) neurons voltage traces'
    fig.canvas.set_window_title(title)

    for i, signal in enumerate(events):
        ax = fig.add_subplot(len(events), 1, i + 1)  # always vertical

        # limits of the x axis
        ax.set_xlim(times[0], times[-1])

        # limits of the y axis
        dmin = signal.min()
        dmax = signal.max()
        ax.set_ylim(dmin - 0.15 * np.abs(dmin), dmax + 0.15 * np.abs(dmax))

        ax.set_xlabel('time (ms)')
        ax.set_ylabel(labels[i])

        ax.plot(times, signal)

    return fig