import csv
from collections import Counter
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scienceplots
black = [0,0,0]
red   = [1,0,0]
blue  = [0,0,1]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
          'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',]


unique_labels = [
    '\\textbf{CMB with Planck}',
    '\\textbf{CMB without Planck}',
    '\\textbf{No CMB; with BBN}',
    #'\\textbf{Pl(k) + CMB lensing}',
    '\\textbf{Cepheids-SNIa}',
    '\\textbf{TRGB, SN-Ia}',
    '\\textbf{Mira stars, SN-Ia}',
    '\\textbf{Masers}',
    '\\textbf{Tully-Fisher Relation}',
    '\\textbf{Surface Brightness Fluctuations}',
    '\\textbf{SNII}',
    #'\\textbf{HII galaxies}',
    #'\\textbf{Lensing related; mass model-dependent}',
    #'\\textbf{Optimistic average}',
    #'\\textbf{Ultra Conservative - no cepheids no lensing}',
    '\\textbf{GW related}',
    ]

#+++++++++++++++++++++++++++++
from matplotlib import rcParams
config = {
	#"mathtext.fontset":'stix',
    'font.family':'Times New Roman',
    'text.usetex': True,
    #'text.latex.preamble': r'\usepackage{amsmath}\boldmath',

	}
#plt.rcParams['text.latex.preamble'] = r'\usepackage{mathastext}'
rcParams.update(config)
plt.style.use('science')
#+++++++++++++++++++++++++++++

class ErrorLinePloter:
    def __init__(self,data,position):
        self.data = data
        self.position = position

# Horizontal line
        self.hlwidth = 0.8
        self.hlstyle = '-'
        self.hlcolor = red

# Point props
        self.point_size = 0.34
        self.point_color = blue
        self.point_lwidth = 0.8 
        
        self.middle_point_type = 'line'
        self.middle_point_size=self.point_size
        self.middle_point_color=self.point_color

        self.middle_point_lwidth=self.point_lwidth
        self.middle_point_mshape='o'

    def set_props(self,hlwidth,hlstyle,hlcolor,
                    psize,pcolor,pwidth,
                    middle_point_type='line',
                    **lmprop):

        self.hlwidth=hlwidth
        self.hlstyle=hlstyle
        self.hlcolor=hlcolor
        self.point_size = psize
        self.point_color = pcolor
        self.point_lwidth = pwidth
        
        self.middle_point_size = psize
        self.middle_point_color= pcolor
        self.middle_point_type=middle_point_type
        if middle_point_type == 'line':
            if len(lmprop)!=0:
                self.middle_point_size=lmprop['mpsize']
                self.middle_point_color=lmprop['mpcolor']
                self.middle_point_lwidth=lmprop['lwidth']
        elif middle_point_type == 'marker':
            if len(lmprop)!=0:
                self.middle_point_size=lmprop['mpsize']
                self.middle_point_color=lmprop['mpcolor']
                self.middle_point_mshape=lmprop['mshape']

    def plot(self):
        list_3=[self.data['ml']+self.data['e1_sig'][0],
                self.data['ml'],
                self.data['ml']+self.data['e1_sig'][1]]
        
        plt.hlines(y=self.position,xmin=list_3[0],xmax=list_3[-1],color=self.hlcolor,ls=self.hlstyle,lw=self.hlwidth,zorder=1)
        plt.vlines(x=[list_3[0],list_3[-1]],
                    ymin=self.position-self.point_size/2,
                    ymax=self.position+self.point_size/2,
                    color=self.point_color,
                    ls='-',
                    lw=self.point_lwidth,
                    zorder=2)

        if self.middle_point_type == 'line':
            plt.vlines(x=list_3[1],
                    ymin=self.position-self.middle_point_size/2,
                    ymax=self.position+self.middle_point_size/2,
                    color=self.middle_point_color,
                    ls='-',
                    lw=self.middle_point_lwidth,
                    zorder=3)
        elif self.middle_point_type == 'marker':
            plt.scatter(list_3[1],self.position,
                    s=self.middle_point_size,
                    color=self.middle_point_color,
                    marker=self.middle_point_mshape,
                    zorder=3)
        else:
            print("Error: Invalid middle point type.")
            sys.exit()

### Repository containing the .csv with the dataset
### See README for more info on the structure
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
fil = os.path.join(data_path, 'dataset2.csv')

### Load the dataset and count the number of data points
nr=1
with open(fil, 'r+') as file:
    reader = csv.reader(file)
    first_line = file.readline()
    next(reader, None)
    for row in reader:
        nr += 1
    nc = first_line.count(',')+1

### Load the data points into arrays
H0 = np.zeros(nr)
Hl = np.zeros(nr)
Hp = np.zeros(nr)
method = ["" for x in range(nr)]
lbl    = ["" for x in range(nr)]
auth   = ["" for x in range(nr)]
etal   = ["" for x in range(nr)]
year   = ["" for x in range(nr)]
set    = ["" for x in range(nr)]

i=0
with open(fil, 'r+') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        method[i] = row[0]
        lbl[i]    = row[1]
        auth[i]   = row[2]
        etal[i]   = row[3]
        year[i]   = row[4]
        set[i]    = row[5]
        H0[i] = float(row[6])
        Hl[i] = float(row[7])
        Hp[i] = float(row[8])
        i += 1

### Count the number of indirect measures
nind=0
for i in range(nr):
    if method[i]=='Indirect':
        nind += 1
#---------------------------label-------------------------------------
aut = ["" for x in range(nr)]
for i in range(nr):
    if etal[i]=='Y':
      aut[i] = auth[i]+' et al. ('+str(year[i])+')'
    else:
      aut[i] = auth[i]+' ('+str(year[i])+')'

paras=[]
for i in range(nr):
    if Hl[i]==Hp[i]:
        paras.append(aut[i])#+' '+str(H0[i])+'${\pm}$'+str(Hp[i]))
    else:
        paras.append(aut[i])#+' '+str(H0[i])+'$^{+'+str(Hp[i])+'}_{-'+str(Hl[i])+'}$')

#---------------------------data-------------------------------------
all_data = []
for i in range(nr):
    all_data.append({'ml':H0[i],'e1_sig':[Hp[i],-Hl[i]]})

#---------------------------style-------------------------------------
unique_lbl = np.unique(lbl)
n_lbl = len(unique_lbl)
pos_num = nr + 2 * n_lbl

positions=[]
labels=[]
for i in range(pos_num+3):
    positions.append(i)
    labels.append('')

#unique_labels=[]
#unique_pos=[]

#---------------------------plot-------------------------------------#
pdf = PdfPages('H0whisker.pdf')

plt.rcParams['figure.figsize'] = (5,6.8)

### Plot each data point with attached label
j=0
k=nind
current_label = None
label_pos = 0
color_index = -1  # Add this to track which color to use

# Container for the special lbl labels:
lbl_positions = []
lbl_labels = []
direct_position = 0
direct_check = True

for i in range(len(paras)):
    # Check that the label is the correct one.
    # If the lbl value is different, the method of measurement changes,
    # so we need to change the label value.
    if lbl[i] != current_label:
        label_pos += 1
        current_label = lbl[i]
        if method[i]=='Indirect':
            lbl_positions.append(pos_num-j+1-label_pos)
            #lbl_labels.append(lbl[i])
        else:
            lbl_positions.append(pos_num-k-label_pos)
            #lbl_labels.append('!!!TO BE REPLACED LATER ON IN CODE!!!')
            #lbl_labels.append(f'$\textbf{lbl[i]}$')
        label_pos += 1
        color_index = (color_index + 1) % len(colors)# To cycle through the colors, if necessary.
        
    current_color = colors[color_index]
    # Plot the data point:
    if method[i]=='Indirect':
        elp = ErrorLinePloter(all_data[i],position=pos_num-j+1-label_pos)
        j += 1
    elif method[i]=='Direct':
        if direct_check:
            direct_position = pos_num-k-label_pos+2
            direct_check = False
        elp = ErrorLinePloter(all_data[i],position=pos_num-k-label_pos)
        k += 1
    labels[elp.position]=paras[i]
    elp.set_props(
          0.8,'-',current_color,
          0.7,current_color,0.8,
          'marker',
          mpsize=2.0,
          mpcolor=current_color,
          mshape='o')
    elp.plot()

elp = ErrorLinePloter({'ml':0.0,'e1_sig':[100.,-100.]},position=direct_position)
labels[elp.position]=''
elp.set_props(0.8,'-.',black,
       0.7,black,0.8,
        'marker',mpsize=2.0,mpcolor=black,mshape='o')
elp.plot()

plt.tick_params(axis='x',labelsize=8)
plt.tick_params(axis='y',labelsize=0)
plt.xticks([i for i in range(60,100,5)])#,fontweight='semibold')
plt.xlim(61,82.5)

plt.ylim(positions[0],positions[-1])

tick_position = np.concatenate((positions,lbl_positions))
tick_label = np.concatenate((labels,unique_labels))

#print(len(tick_position), len(tick_label), len(positions), len(labels), len(unique_labels), len(lbl_positions))


plt.yticks(tick_position, tick_label,)#fontweight='semibold')


# Apply formatting: boldface and size for some, normal and size for others
yticklabels = plt.gca().get_yticklabels()
for tick, label in zip(yticklabels, tick_label):
    #tick.set_text(label)
    if '20' not in label:
        # change the colour to white:
        tick.set_color('k')
        tick.set_fontsize(6)
    
    #if 'textbf' in label:
    
        #tick.set_fontsize(0.0)
    else:
        tick.set_fontsize(6)
plt.gca().set_yticklabels(yticklabels)

plt.text(77.5,direct_position+1.,"Indirect",size=9)
plt.text(77.5,direct_position-1.8,"Direct",size=9)
plt.text(74.7,pos_num-3,"${H_0}\,$\n[km$\,$s$^{-1}\,$Mpc$^{-1}$]",size=10)

### Plot the vertical bars for reference: R22 vs CMB
plt.bar(73.04, 100, width=1.04*2, facecolor = 'cyan', alpha = 0.15)
plt.bar(67.27, 100, width=1.2, facecolor = 'pink', alpha = 0.25)

plt.minorticks_off()
plt.tight_layout()
pdf.savefig()
pdf.close()

print( np.log(3e5 / 700) )