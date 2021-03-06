import numpy as np
import matplotlib.pylab as plt
import networkx as nx
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable


def plot_graph(graph, ax):
    """ Plot the network used for the current simulation
    """
    # generate some node properties
    labels = {}
    for n in graph.nodes():
        labels[n] = n

    # compute layout
    pos = nx.nx_pydot.graphviz_layout(graph, prog="neato")

    # draw graph
    nx.draw(graph, pos, node_color="lightskyblue", node_size=400, font_size=20, ax=ax)
    nx.draw_networkx_labels(graph, pos, labels)


def plot_corr_vals(corr_vals, t, ax):
    """ Plot the correlation values between each of the nodes, over time
	"""
    for i in range(np.size(corr_vals, 0)):
        ax.plot(t, corr_vals[i, :])
    ax.set_xlabel("t")
    ax.set_ylabel("correlation values")


def plot_time_evolution(sol, t, Omega, ax):
    """ Plot the time evolution of the system
	"""
    Phi = lambda t: Omega * t
    nf = np.size(sol, 0)
    for i in range(nf):
        ax.plot(t, sol[i, :], label="f %d" % (i))
    ax.plot(t, (Phi(t) % (2 * np.pi)), linewidth=2, color="r", label="driver")
    ax.legend(loc="upper right", prop={"size": 7})
    ax.set_xlabel("t")
    ax.set_ylabel(r"$\theta$")


def plot_heatmap_evolutions(sol, t, ax):
    """ Plot system evolution as a heat map
    """
    ax.imshow(
        sol,
        aspect="auto",
        cmap=plt.cm.gray,
        interpolation="nearest",
        extent=(0, t[-1], 0, np.size(sol, 0)),
    )

    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$\Theta_i$")


def plot_sum_corr_mat(sum_rho_avg, ax):
    """ Plot the averaged sum of the correlation matrices
	"""
    im = ax.imshow(sum_rho_avg, cmap=plt.cm.coolwarm, interpolation="nearest")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    cbar = plt.colorbar(im, cax=cax)
    cbar.ax.tick_params(labelsize=10)
    ax.set_title("Correlation matrix", fontsize=10)


def plot_time_to_sync(D_average, ax):
    """ Plot the matrix stroring the time to correlation for one run
	"""
    im = plt.imshow(D_average, cmap=plt.cm.coolwarm, interpolation="nearest")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    cbar = plt.colorbar(im, cax=cax)
    cbar.ax.tick_params(labelsize=10)
    ax.set_title("Time to synchronization in DCM", fontsize=10)


def plot_corr_mat_dcm(G, sum_rho_avg, D_average, no_runs):
    """ Plot the sum of the correlation matrices, 
		avergaed over a number of runs
	"""
    plt.figure()
    gs = mpl.gridspec.GridSpec(1, 3)
    plot_graph(G, plt.subplot(gs[:, 0]))
    plot_sum_corr_mat(sum_rho_avg, plt.subplot(gs[:, 1]))
    plot_time_to_sync(D_average, plt.subplot(gs[:, 2]))
    plt.suptitle("Average over %s runs" % (no_runs))
    plt.savefig("images/corrMat_dcm.png")
    plt.savefig("images/corrMat_dcm.pdf")


def plot_time_corr(G, sol, corr_vals, Omega, t):
    """ Plot the time evolution (as time series and as heat-map), together
		with the corresponding correlation values between each of the nodes
	"""
    plt.figure()
    gs = mpl.gridspec.GridSpec(2, 2)
    plot_graph(G, plt.subplot(gs[0, 0]))
    plot_time_evolution(sol, t, Omega, plt.subplot(gs[0, 1]))
    plot_corr_vals(corr_vals, t, plt.subplot(gs[1, 1]))
    plot_heatmap_evolutions(sol, t, plt.subplot(gs[1, 0]))
    plt.savefig("images/time_corr.png")
    plt.savefig("images/time_corr.pdf")
