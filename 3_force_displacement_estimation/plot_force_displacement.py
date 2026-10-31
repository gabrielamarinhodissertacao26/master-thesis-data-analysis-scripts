"""
Estimated magnetic force and bead displacement from the FEMM simulation
of configuration 1 (magnetic block).

Input: FEMM line export (Plot X-Y -> |H| -> "Write data to text file") with two
columns, Length (mm) and |H| (A/m); lines starting with % are ignored.

Method (see Materials and Methods):
  1. |H| exported directly from FEMM, and its gradient along the line
     (Savitzky-Golay, 0.1 mm window);
  2. bead magnetization from the Frohlich-Kennelly equation:
         M(H) = chi0 * H / (1 + chi0 * H / Msat)
  3. magnetic force on one bead (induced moment aligned with the field):
         F = mu0 * Vp * M(H) * d|H|/dx
  4. bead displacement, quasi-static approach (rearranged E_quasistatic):
         U = F (5 - 6 nu)(1 + nu) / (12 pi (1 - nu) E a)

Usage: place this script in the same folder as the .txt file and run
    python plot_force_displacement.py
Requires: numpy, scipy, matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# ---- INPUT FILE (|H| exported from FEMM) -------------------------------------
FILE_BLOCK = "H_1500pontos_magneticblock.txt"   # configuration 1

# ---- PARAMETERS --------------------------------------------------------------
MU0 = 4e-7 * np.pi        # vacuum permeability (H/m)
CHI0 = 2.65               # initial susceptibility (precursor M(H) curve)
MSAT = 1.1e5              # saturation magnetization of the beads (A/m), datasheet
A = 150e-9                # bead radius (m), 300 nm beads
E_LIST = [520, 800]       # Young's modulus of 1.2% PEG-W (520 Pa) and 1.5% PEG-W (800 Pa)
LABELS = ["PEG-W 1.2% (E = 520 Pa)", "PEG-W 1.5% (E = 800 Pa)"]
NU = 0.3                  # Poisson's ratio
TRIM_MM = 0.05            # length excluded at each end of the line (mm)
WINDOW_MM = 0.1           # Savitzky-Golay window (mm)

VP = 4 / 3 * np.pi * A**3                                   # bead volume (m^3)
K_U = (5 - 6 * NU) * (1 + NU) / (12 * np.pi * (1 - NU) * A)  # U = K_U * F / E

COLORS = ["#1c3f72", "#eb6834"]   # same colours as the other Chapter 4 figures
plt.rcParams.update({"font.family": "serif", "font.size": 10})

# ---- Calculation -------------------------------------------------------------
data = np.loadtxt(FILE_BLOCK, comments="%")
x, H = data[:, 0], data[:, 1]                  # mm, A/m
dx = x[1] - x[0]
win = int(WINDOW_MM / dx) // 2 * 2 + 1         # odd number of points
dHdx = np.abs(savgol_filter(H, win, 2, deriv=1, delta=dx * 1e-3))   # A/m^2
M = CHI0 * H / (1 + CHI0 * H / MSAT)           # Frohlich-Kennelly (A/m)
F = MU0 * VP * M * dHdx                        # N
U = [K_U * F / E for E in E_LIST]              # m, one array per stiffness

keep = (x >= x[0] + TRIM_MM) & (x <= x[-1] - TRIM_MM)
x, F, M = x[keep], F[keep], M[keep]
U = [u[keep] for u in U]

# ---- Print values used in the text ------------------------------------------
# Distances of the imaging positions to the magnetic block (Fiji + wall of 0.9 mm)
POSITIONS = {"Position 1": 0.648 + 1,
             "Position 2": 0.992 + 1,
             "Position 3": 1.364 + 1}

print("Configuration 1 (Magnetic Block)")
print(f"M/Msat between {100*M.min()/MSAT:.0f} and {100*M.max()/MSAT:.0f}%")
for name, d in POSITIONS.items():
    i = np.argmin(np.abs(x - d))
    txt = ", ".join(f"U(E = {E} Pa) = {u[i]*1e9:.2f} nm" for E, u in zip(E_LIST, U))
    print(f"  {name} ({x[i]:.2f} mm): F = {F[i]*1e12:.2f} pN, {txt}")

# ---- Figure: force and displacement -----------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0), constrained_layout=True)
ax[0].plot(x, F * 1e12, color="#444444", lw=2)
for u, c, lab in zip(U, COLORS, LABELS):
    ax[1].plot(x, u * 1e9, color=c, lw=2, label=lab)
ax[1].legend(frameon=False, fontsize=9)
ax[0].set_ylabel("Magnetic force, $F$ (pN)")
ax[1].set_ylabel("Bead displacement, $U$ (nm)")
ax[0].set_title("(a)", loc="left")
ax[1].set_title("(b)", loc="left")
for a in ax:
    a.set_yscale("log")
    a.set_xlabel("Distance from the magnet surface (mm)")
    a.set_xlim(0, x.max())
    a.grid(True, color="#e6e5e1", lw=0.6)
    a.spines[["top", "right"]].set_visible(False)
fig.savefig("force_displacement_config1.pdf")
fig.savefig("force_displacement_config1.png", dpi=300)
plt.show()

