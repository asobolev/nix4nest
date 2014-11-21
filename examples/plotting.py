import numpy as np

from matplotlib.pyplot import figure
import matplotlib.pyplot as plt


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


def weights_multiple(weights):
    """
    Creates a figure to plot several weight matrixes.

    :param weights: list of numpy 2D arrays with float values
    """
    fig = figure(figsize=(11, 7))
    fig.canvas.set_window_title('Weights input - map layers')

    to_plot = np.array(weights)
    total = len(to_plot)
    g_min = to_plot.min() # needed for colorbar
    g_max = to_plot.max()
    delta = g_max - g_min

    for i, matrix in enumerate(to_plot):
        key = 100 + total * 10 + (i+1) # always horizontal

        ax = fig.add_subplot(key)
        weights_normalized = matrix
        im = ax.imshow(weights_normalized.T, vmin=g_min, vmax=g_max,
                       interpolation='nearest', origin='lower')
        ax.set_xlabel('input neurons')
        ax.set_ylabel('output neurons')

    try:
        axc = fig.add_axes([0.1, 0.1, 0.8, 0.05]) # setup colorbar axes.
        bar = plt.colorbar(im, cax=axc, orientation='horizontal')
        labels = [round((g_min + (x * delta/10.0)), 2) for x in range(11)]
        bar.set_ticks(labels)
        bar.set_ticklabels([str(x) for x in labels])
    except NameError:
        pass

    return fig