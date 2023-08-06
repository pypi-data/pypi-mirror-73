import matplotlib as mpl
import pprint
from cycler import cycler #color cycler
import itertools

#All colors
colors = {u"gcred" : u"#BE1818",
          u"gcorange" : u"#FF9900",
          u"gclime" : u"#9DCE09",
          u"gcgreen" : u"#488F38",
          u"gcdarkgrey" : u"#808080",
          u"gcgrey" : u"#C0C0C0",
          u"gclightgrey" : u"#E6E6E6",
          u"gcsilver" : u"#EFF2F9",
          u"gcdarkblue" : u"#00006E",
          u"gcblue" : u"#000099",
          u"gcgreyblue" : u"#1C3363",
          u"gccyan" : u"#009999",
          u"gcgreycyan" : u"#BBE0E3",
          u"gcmagenta" : u"#9467bd",
          u"gcbrown" : u"#8c564b"}

#Colorcycle
colorcycle = ["gcblue", "gcred", "gcgreen", "gcorange", "gccyan",
              "gcmagenta", "gcbrown", "gcdarkgrey"]
lscycle = ['-', '--', '-.', ':']
markercycle = ['x', '*', 'v', '^']

def make_colorcycler(iterator=False):
    if iterator:
        return itertools.cycle(colorcycle)

    return cycler(color=colorcycle)


#Patch matplotlib color palette
if int(mpl.__version__[0]) < 2:
    mpl.colors.cnames.update(colors)
else:
    mpl.colors._colors_full_map.update(colors)

#Update default color palette
_orig_propcycle = mpl.rcParams["axes.prop_cycle"]
def patch_propcycle():
    cycle = (cycler(ls=lscycle)+cycler(marker=markercycle))*cycler(color=colorcycle)
    mpl.rcParams["axes.prop_cycle"] = cycle
patch_propcycle()

#Restore original colorcycle
def restore_propcycle():
    mpl.rcParams["axes.prop_cycle"] = _orig_propcycle


def show_colors():
    #Function to print the GC colors
    pprint.pprint(colors)
