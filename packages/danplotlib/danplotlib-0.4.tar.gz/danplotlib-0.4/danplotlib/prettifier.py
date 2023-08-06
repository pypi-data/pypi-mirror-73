"""
Prettified versions of matplotlib plotting functions
"""
from __future__ import division, print_function
from functools import wraps, partial, update_wrapper
import matplotlib as mpl
import matplotlib.pyplot as plt
import os.path
import logging

_log = logging.getLogger(__name__)

def default_rc_params():
    rc_file = os.path.join(os.path.dirname(__file__), "styles/matplotlibrc")
    plt.style.use(rc_file)
    _log.info(f'Loaded rc parameters from "{rc_file}".')

    return plt.rcParams

default_rc_params()

def restore_rc_params():
    rc_file = mpl.matplotlib_fname()
    plt.style.use(rc_file)
    _log.info(f'Restored rc parameters from "{rc_file}".')

    return plt.rcParams

def use_style(style):
    folder = os.path.join(os.path.dirname(__file__), "styles/stylelib")
    file = os.path.join(folder, style+".mplstyle")
    
    plt.style.use(file)
    _log.info(f'Loaded rc parameters from "{file}".')

    return plt.rcParams


#Define new plot functions which also plot minorticks
def minorticks_decorate(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        output = func(*args, **kwargs)  #call the original function
        plt.minorticks_on()
        return output

    return func_wrapper

plot = minorticks_decorate(plt.plot)
step = minorticks_decorate(plt.step)
errorbar_temp = minorticks_decorate(plt.errorbar)
hist_temp = minorticks_decorate(plt.hist)

#Change default linewidth for histograms to global default
hist = partial(hist_temp, linewidth=plt.rcParams["lines.linewidth"], histtype="step")
update_wrapper(hist, hist_temp)

#Change default appearance for errorbar
errorbar = partial(errorbar_temp, fmt=".", ms=0)
update_wrapper(errorbar, errorbar_temp)

#Change default position for xlabel and ylabel
xlabel = partial(plt.xlabel, ha="right", x=1)
update_wrapper(xlabel, plt.xlabel)
ylabel = partial(plt.ylabel, ha="right", y=1)
update_wrapper(ylabel,plt.ylabel)



def trafo_subplots_axes(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        f, ax = func(*args, **kwargs)  #call the original function
        #ax might be single axis object or array of axis objects
        to_list = False   #If artificially cast to list
        if not hasattr(ax, '__iter__'):
            ax = [ ax ]
            to_list = True

        for axis in ax:  #Do the update of the methods
            axis.minorticks_on() #Turn on minorticks
            #Adjust default xlabel position
            set_xlabel_temp = axis.set_xlabel
            axis.set_xlabel = partial(set_xlabel_temp, ha="right", x=1)
            update_wrapper(axis.set_xlabel, set_xlabel_temp)
            #Adjust default ylabel position
            set_ylabel_temp = axis.set_ylabel
            axis.set_ylabel = partial(set_ylabel_temp, ha="right", y=1)
            update_wrapper(axis.set_ylabel, set_ylabel_temp)

            #Set default linewidth and hist type for histogram plots
            axis_hist_temp = axis.hist
            axis.hist = partial(axis_hist_temp, linewidth=plt.rcParams["lines.linewidth"],
                                histtype="step")
            update_wrapper(axis.hist, axis_hist_temp)


            #Set default errorbar format and ms
            axis_errorbar_temp = axis.errorbar
            axis.errorbar = partial(axis_errorbar_temp, fmt=".", ms=0)
            update_wrapper(axis.errorbar, axis_errorbar_temp)

        if to_list: #Restore old behaviour
            ax = ax[0]

        return f, ax
    return func_wrapper

subplots = trafo_subplots_axes(plt.subplots)
