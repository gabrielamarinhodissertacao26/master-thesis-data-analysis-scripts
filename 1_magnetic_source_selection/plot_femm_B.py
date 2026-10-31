"""
Analysis of the simulated magnetic flux density (FEMM line exports).

Each input file is a FEMM "Plot X-Y -> Write data to text file" export with two
columns: Length (mm) and |B| (T). Lines starting with % are ignored.

The script:
  1. computes the gradient of |B| along the line, smoothed with a Savitzky-Golay
     filter (2nd-order polynomial, 0.1 mm window), excluding 0.05 mm at each end;
  2. prints |B| at 0.05 mm from each end and the average gradient between them;
  3. saves the main figure (|B| and gradient) and the appendix figure
     (gradient with and without smoothing).

Usage: place this script in the same folder as the .txt files and run
    python plot_femm_B.py
Requires: numpy, scipy, matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# ---- INPUT FILES -------------------------------------------------------------
FILE_BLOCK = "B_1500pontos_magneticblock.txt"   # configuration 1
FILE_CYL = "B_1500pontos_cylindricals.txt"      # configuration 2
LABEL_BLOCK = "Configuration 1 (Magnetic Block)"
LABEL_CYL = "Configuration 2 (Cylindrical Magnets)"

# ---- ANALYSIS PARAMETERS -----------------------------------------------------
TRIM_MM = 0.05      # length excluded at each end of the line (edge effects)
WINDOW_MM = 0.1     # Savitzky-Golay window
POLY_ORDER = 2      # Savitzky-Golay polynomial order

C1, C2 = "#2a78d6", "#eb6834"   # colorblind-safe pair
plt.rcParams.update({"font.family": "serif", "font.size": 10})


def analyse(path):
    data = np.loadtxt(path, comments="%")
    x, B = data[:, 0], data[:, 1]                       # mm, T
    dx = x[1] - x[0]
    win = int(WINDOW_MM / dx) // 2 * 2 + 1              # odd number of points
    grad_raw = np.abs(np.gradient(B, x * 1e-3))         # T/m
    grad = np.abs(savgol_filter(B, win, POLY_ORDER, deriv=1, delta=dx * 1e-3))
    keep = (x >= x[0] + TRIM_MM) & (x <= x[-1] - TRIM_MM)
    i0, i1 = np.argmax(keep), len(keep) - 1 - np.argmax(keep[::-1])
    avg = abs(B[i0] - B[i1]) / ((x[i1] - x[i0]) * 1e-3)
    return dict(x=x, B=B, grad_raw=grad_raw, grad=grad, keep=keep,
                B_start=B[i0], B_end=B[i1], avg=avg)


r1, r2 = analyse(FILE_BLOCK), analyse(FILE_CYL)
for name, r in [(LABEL_BLOCK, r1), (LABEL_CYL, r2)]:
    print(f"{name}: |B| {r['B_start']:.3f} -> {r['B_end']:.3f} T, "
          f"average gradient {r['avg']:.0f} T/m")


def style(ax):
    ax.grid(True, color="#e6e5e1", lw=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel("Distance from the magnet surface (mm)")
    ax.set_xlim(0, max(r1["x"].max(), r2["x"].max()))


# ---- Main figure: |B| and smoothed gradient ---------------------------------
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0), constrained_layout=True)
for r, c, lab in [(r1, C1, LABEL_BLOCK), (r2, C2, LABEL_CYL)]:
    k = r["keep"]
    ax[0].plot(r["x"][k], r["B"][k], color=c, lw=2, label=lab)
    ax[1].plot(r["x"][k], r["grad"][k], color=c, lw=2)
ax[0].set_ylabel("|B| (T)")
ax[0].set_ylim(bottom=0)
ax[1].set_ylabel(r"$|\nabla |B||$ (T/m)")
ax[1].set_yscale("log")
ax[0].set_title("(a)", loc="left")
ax[1].set_title("(b)", loc="left")
for a in ax:
    style(a)
fig.legend(*ax[0].get_legend_handles_labels(), loc="outside lower center",
           ncol=2, frameon=False)
fig.savefig("femm_B_comparison.pdf")
fig.savefig("femm_B_comparison.png", dpi=300)

# ---- Appendix figure: gradient with and without smoothing -------------------
fig2, ax2 = plt.subplots(1, 2, figsize=(7.2, 3.0), constrained_layout=True)
for a, r, c, title in [(ax2[0], r1, C1, "(a) " + LABEL_BLOCK),
                       (ax2[1], r2, C2, "(b) " + LABEL_CYL)]:
    k = r["keep"]
    a.plot(r["x"], r["grad_raw"], color="#b8b7b2", lw=0.8, label="Without smoothing")
    a.plot(r["x"][k], r["grad"][k], color=c, lw=2, label="Savitzky-Golay (0.1 mm)")
    a.set_yscale("log")
    a.set_title(title, loc="left", fontsize=9)
    a.legend(frameon=False, fontsize=8, loc="upper right")
    style(a)
ax2[0].set_ylabel(r"$|\nabla |B||$ (T/m)")
fig2.savefig("gradient_smoothing.pdf")
fig2.savefig("gradient_smoothing.png", dpi=300)

plt.show()
