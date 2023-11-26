import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


l=[]
dH = []
ddH = []
dPV = []
ddPV = []
for lambda_par in tqdm([i for i in range(0,41)]):
	l.append(lambda_par)
	if lambda_par == 0:
		t, l_mass, l_coul, l_vdw, l_bonded, l_rest, dH_0, dH_p1, PV = np.loadtxt(f"Lambda_{lambda_par}/md{lambda_par}.xvg",comments=["@", "#"],unpack=True) 
	else:
		t, l_mass, l_coul, l_vdw, l_bonded, l_rest, dH_m1, dH_0, dH_p1, PV = np.loadtxt(f"Lambda_{lambda_par}/md{lambda_par}.xvg",comments=["@", "#"],unpack=True) 
	dH.append(np.average(dH_p1))
	ddH.append(np.sqrt(np.std(dH_p1)))
	dPV.append(np.average(PV))
	ddPV.append(np.sqrt(np.std(PV)))
dH=np.array(dH)
ddH = np.array(ddH)
dPV=np.array(dPV)
ddPV = np.array(ddPV)
print(dH.sum()+dPV.sum(), ddH.sum()+ddPV.sum())

font_size=22

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.set_ylabel(r"$\Delta$G, kJ/mol", fontsize=font_size)
ax.set_xlabel(r"$\lambda$", fontsize=font_size)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)

ax.errorbar(l, dH+dPV, ddH+ddPV, fmt='o', color="black", markersize=0, linewidth=1, capsize=3)
ax.plot(l, dH+dPV, "o", color="green", label=r'$\Delta$ G', markersize=5)
plt.axhline(y=0, xmin=0, xmax=40, color='r', linestyle='--', linewidth=1)

ax.set_title(r'$\Delta$G in TI method', fontsize=font_size, pad=8)
plt.legend()
plt.savefig(f'dG_TI.png', bbox_inches='tight')

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.set_ylabel(r"$\Delta$G, kJ/mol", fontsize=font_size)
ax.set_xlabel(r"$\lambda$", fontsize=font_size)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)

ax.plot(l, np.cumsum(dH+dPV), "-", color="red", label=r'$\Delta$G$_{cumsum}$', markersize=5)
ax.set_title(r'$\Delta$G$_{sum}$ in TI method', fontsize=font_size, pad=8)
plt.legend()
plt.savefig(f'dG_TI_sum.png', bbox_inches='tight')
plt.close()
