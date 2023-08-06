# Make all functions of matplotlib.pyplot available here as well
from matplotlib.pyplot import *
import matplotlib.pyplot as plt #To access native functions
from matplotlib.backends.backend_pdf import PdfPages

# Import danplotlib objects
from .prettifier import *
from .colors import *
from .utils import *
