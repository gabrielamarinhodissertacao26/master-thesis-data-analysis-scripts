"""Calibration curve: magnetic force on the beads vs distance to the magnetic block.
Values from Calibration_Curve_All_Calculations_corrected.xlsx (mean +/- SD, n = 3 tracks;
7.8 mm: repeated at the end of the series, n = 2)."""
import matplotlib.pyplot as plt

dist = [0.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8, 10.8]          # mm
force = [1093, 1001, 993, 687, 801, 861, 952, 315, 1052, 716, 835]       # fN
sd = [55, 145, 119, 387, 215, 59, 49, 97, 156, 260, 42]                  # fN
REPEATED = 7.8

plt.rcParams.update({"font.family": "serif", "font.size": 11})
fig, ax = plt.subplots(figsize=(6.0, 3.8), constrained_layout=True)
main = [i for i, d in enumerate(dist) if d != REPEATED]
rep = [i for i, d in enumerate(dist) if d == REPEATED]
ax.errorbar([dist[i] for i in main], [force[i] for i in main], yerr=[sd[i] for i in main],
            fmt="o", ms=7, color="#2a78d6", ecolor="#2a78d6", elinewidth=1.2, capsize=4,
            label="Mean $\\pm$ SD ($n = 3$)", zorder=3)
ax.errorbar([dist[i] for i in rep], [force[i] for i in rep], yerr=[sd[i] for i in rep],
            fmt="s", ms=7, mfc="white", color="#eb6834", ecolor="#eb6834", elinewidth=1.2,
            capsize=4, label="Repeated at the end ($n = 2$)", zorder=3)
ax.set_xlabel("Distance to the magnetic block (mm)")
ax.set_ylabel("Magnetic force (fN)")
ax.set_xlim(0, 11.5)
ax.set_ylim(0, 1600)
ax.set_xticks(range(0, 12))
ax.grid(True, color="#e6e5e1", lw=0.6, zorder=0)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="upper right", fontsize=9)
fig.savefig("calibration_curve.png", dpi=300)
fig.savefig("calibration_curve.pdf")
