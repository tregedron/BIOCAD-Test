import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

l_1, l_2, dG, ddG = np.loadtxt(f"bar_norm.xvg",comments="@",unpack=True)

dG_int = np.cumsum(dG)

font_size=22

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.set_ylabel(r"$\Delta$G, kJ/mol", fontsize=font_size)
ax.set_xlabel(r"$\lambda$", fontsize=font_size)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)

ax.errorbar(l_1, dG, ddG, fmt='o', color="black", markersize=0, linewidth=1, capsize=3)
ax.plot(l_1, dG, "o", color="green", label=r'$\Delta$ G', markersize=5)
plt.axhline(y=0, xmin=0, xmax=40, color='r', linestyle='--', linewidth=1)


ax.set_title(r'$\Delta$G in BAR method', fontsize=font_size, pad=8)
plt.legend()
plt.savefig(f'dG_BAR.png', bbox_inches='tight')


fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.set_ylabel(r"$\Delta$G, kJ/mol", fontsize=font_size)
ax.set_xlabel(r"$\lambda$", fontsize=font_size)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)

ax.plot(l_1, dG_int, "-", color="red", label=r'$\Delta$G$_{cumsum}$', markersize=5)
ax.set_title(r'$\Delta$G$_{sum}$ in BAR method', fontsize=font_size, pad=8)
plt.legend()
plt.savefig(f'dG_BAR_sum.png', bbox_inches='tight')
plt.close()

