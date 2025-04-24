"""
Author: Philippe de Saint-Seine

Purpose of the file:
Writing code to plot an HR diagram with the data from the SDSS DR7.
"""
import matplotlib.pyplot as plt
import scienceplots
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import os

# Plotting parameters:
#+++++++++++++++++++++++++++++
from matplotlib import rcParams
config = {
	"mathtext.fontset":'stix',
    'font.family':'Times New Roman',
    'text.usetex': True,
    #'text.latex.preamble': r'\usepackage{amsmath}\boldmath',

	}
#plt.rcParams['text.latex.preamble'] = r'\usepackage{mathastext}'
rcParams.update(config)
plt.style.use('science')
#+++++++++++++++++++++++++++++

# Data file
### Repository containing the .csv with the dataset
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),)
#file = os.path.join(data_path, 'NGC2967.xlsx')
#df = pd.read_excel(file)

file = os.path.join(data_path, 'NGC4424.xlsx')
#df = pd.read_csv(file, delimiter=',', header=0)
df = pd.read_excel(file)

df = df.dropna()
df['B-V'] = df['inst_vega_mag2'] - df['inst_vega_mag1']
#df_stars = df[df['type'] == 6].copy()

# All this to plot g-r vs. r
x_axis_vals = df['B-V'].values
y_axis_vals = df['inst_vega_mag2'].values

# Plotting the data
pdf = PdfPages('HR_diagram2.pdf')

plt.rcParams['figure.figsize'] = (7,5)

plt.plot(x_axis_vals, y_axis_vals, 'o', color='blue', markersize=0.5, label='Data')
plt.xlabel('g-r')
plt.ylabel('r')
#plt.xlim(-2.5, 5)
plt.gca().invert_yaxis()
#plt.ylim(25, 10)

plt.minorticks_off()
plt.tight_layout()
pdf.savefig()
pdf.close()

