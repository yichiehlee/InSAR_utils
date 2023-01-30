import os                        
import matplotlib.pyplot as plt   
import numpy as np 
import datetime         
import matplotlib as mpl 
from mintpy.objects import ifgramStack
from mintpy.objects.colors import ColormapExt
from mpl_toolkits.axes_grid1 import make_axes_locatable

data = np.loadtxt('coherenceSpatialAvg.txt', skiprows=5, dtype=bytes).astype(str)

date = data[:, 0].astype(str)
mean = data[:, 1].astype(float)
Btemp = data[:, 2].astype(float)
Bperp = data[:, 3].astype(float)
num = data[:, 4].astype(float)

date12List = np.loadtxt('coherenceSpatialAvg.txt', skiprows=5, dtype=bytes).astype(str)[:,0].tolist() # number of interferograms
mDates = [i.split('_')[0] for i in date12List] # master date
sDates = [i.split('_')[1] for i in date12List] # slave date
dateList = sorted(list(set(mDates + sDates)))  # number of acquisitions

d2 = [datetime.datetime.strptime(d, "%Y%m%d") for d in dateList]

ifgram_num = len(dateList)
pbase12 = np.zeros(ifgram_num)
tbase12 = np.zeros(ifgram_num)

A = ifgramStack.get_design_matrix4timeseries(date12List)[0]

pbaseList = np.zeros(len(dateList), dtype=np.float32)
pbaseList[1:] = np.linalg.lstsq(A, np.array(Bperp), rcond=None)[0]

for i in range(ifgram_num):
    m_idx = dateList.index(mDates[i])
    s_idx = dateList.index(sDates[i])
    pbase12[i] = pbaseList[s_idx] - pbaseList[m_idx]
    #tbase12[i] = tbaseList[sDates[i]] - tbaseList[mDates[i]]

dropDate = np.loadtxt('excludeIfgDate.txt', dtype=bytes).astype(str).tolist()
drop_mDates = [i.split('_')[0] for i in dropDate] # master date
drop_sDates = [i.split('_')[1] for i in dropDate] # slave date

keepDate = np.loadtxt('keepIfgDate.txt', dtype=bytes).astype(str).tolist()
keep_mDates = [i.split('_')[0] for i in keepDate] # master date
keep_sDates = [i.split('_')[1] for i in keepDate] # slave date

cmap = ColormapExt('RdBu').colormap

# Plot
plt.figure(figsize=(8, 5))
plt.subplot(211)
plt.tight_layout() 
# plot dot (SAR acquisition)
plt.plot(d2, pbaseList, 'ko')
plt.grid()
plt.title('Interferogram Network (keep)')
plt.xlabel('Year')
plt.ylabel('Perpendicular Baseline (m)')

# # plot line (pair/interferogram)
ax = plt.gca()
cax = make_axes_locatable(ax).append_axes("right", '3%', pad = '3%')
norm = mpl.colors.Normalize(vmin=np.min(mean), vmax=np.max(mean))
cbar = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm)
cbar.set_label('Average Spatial Coherence')

for i in range(len(keepDate)):
    m_idx = dateList.index(keep_mDates[i])
    s_idx = dateList.index(keep_sDates[i])
    x = np.array([d2[m_idx], d2[s_idx]])
    y = np.array([pbaseList[m_idx], pbaseList[s_idx]])
    val = Bperp[i]
    val_norm = (val - np.min(mean)) / (np.max(mean) - np.min(mean))
    
    ax.plot(x, y ,'-', c = cmap(val_norm), linewidth = 1)   


plt.subplot(212)
plt.tight_layout() 
plt.plot(d2, pbaseList, 'ko')
plt.grid()
plt.title('Interferogram Network')
plt.xlabel('Year')
plt.ylabel('Perpendicular Baseline (m)')

ax2 = plt.gca()
cax = make_axes_locatable(ax2).append_axes("right", '3%', pad = '3%')
norm = mpl.colors.Normalize(vmin=np.min(mean), vmax=np.max(mean))
cbar = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm)
cbar.set_label('Average Spatial Coherence')

# # plot keep pairs & drop pairs
for i in range(len(dropDate)):
    m_idx = dateList.index(drop_mDates[i])
    s_idx = dateList.index(drop_sDates[i])
    x = np.array([d2[m_idx], d2[s_idx]])
    y = np.array([pbaseList[m_idx], pbaseList[s_idx]])
    val = Bperp[i]
    val_norm = (val - np.min(mean)) / (np.max(mean) - np.min(mean))
    
    ax2.plot(x, y ,'--', c = cmap(val_norm), linewidth = 1)   

for i in range(len(keepDate)):
    m_idx = dateList.index(keep_mDates[i])
    s_idx = dateList.index(keep_sDates[i])
    x = np.array([d2[m_idx], d2[s_idx]])
    y = np.array([pbaseList[m_idx], pbaseList[s_idx]])
    val = Bperp[i]
    val_norm = (val - np.min(mean)) / (np.max(mean) - np.min(mean))
    
    ax2.plot(x, y ,'-', c = cmap(val_norm), linewidth = 1)   

# # plot
# plt.figure(figsize=(10, 6))
# plt.subplot(211)
# plt.tight_layout() 

# # plot dot (SAR acquisition)
# plt.plot(d2, pbaseList, 'o')
# plt.grid()
# for i in range(len(keepDate)):
#     m_idx = dateList.index(keep_mDates[i])
#     s_idx = dateList.index(keep_sDates[i])
#     x = np.array([d2[m_idx], d2[s_idx]])
#     y = np.array([pbaseList[m_idx], pbaseList[s_idx]])
#     plt.plot(x, y ,'k-', linewidth = 0.8)


# plt.title('Interferogram Network (keep)')
# plt.xlabel('Year')
# plt.ylabel('Perpendicular Baseline (m)')

# plt.subplot(212)
# plt.tight_layout() 
# plt.plot(d2, pbaseList, 'o')
# plt.grid()
# # # plot keep pairs & drop pairs
# for i in range(len(dropDate)):
#     m_idx = dateList.index(drop_mDates[i])
#     s_idx = dateList.index(drop_sDates[i])
#     x = np.array([d2[m_idx], d2[s_idx]])
#     y = np.array([pbaseList[m_idx], pbaseList[s_idx]])
#     plt.plot(x, y ,'r--', linewidth = 0.8)

# for i in range(len(keepDate)):
#     m_idx = dateList.index(keep_mDates[i])
#     s_idx = dateList.index(keep_sDates[i])
#     x = np.array([d2[m_idx], d2[s_idx]])
#     y = np.array([pbaseList[m_idx], pbaseList[s_idx]])
#     plt.plot(x, y ,'k-', linewidth = 0.8)


# plt.title('Interferogram Network')
# plt.xlabel('Year')
# plt.ylabel('Perpendicular Baseline (m)')

plt.savefig('IfgNetwork.png')
