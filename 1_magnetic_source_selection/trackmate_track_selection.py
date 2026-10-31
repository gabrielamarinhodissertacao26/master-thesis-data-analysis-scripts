"""
Selection of the TrackMate tracks and calculation of the terminal velocity of
the beads for one distance to the magnetic block (calibration experiments).

Input: TrackMate spots export (.csv) of one distance, with the columns
"Track ID", "X" (um) and "T" (s).

For each track with a minimum duration of 5 s, a linear fit X = (dx/dt) T + b
is performed. The 3 tracks with the highest R2 are selected, and the terminal
velocity is reported as the mean +/- SD of their slopes.

Usage: change the file name below (example: 0 mm) and run
    python trackmate_track_selection.py
Requires: pandas, scipy
"""
import pandas as pd
from scipy.stats import linregress

# ============================================================
# 1. READ THE FILE
# ============================================================
file = "0mm.csv"   # example: distance to the magnetic block = 0 mm
df = pd.read_csv(file, skiprows=2)

# Convert the relevant columns to numeric values
df["Track ID"] = pd.to_numeric(df["Track ID"], errors="coerce")
df["X"] = pd.to_numeric(df["X"], errors="coerce")
df["T"] = pd.to_numeric(df["T"], errors="coerce")

# Remove rows with invalid or missing data
df = df.dropna(subset=["Track ID", "X", "T"])

# Sort by track and time
df = df.sort_values(["Track ID", "T"])

# ============================================================
# 2. CALCULATE R2 AND dx/dt FOR EACH TRACK
# ============================================================
MIN_DURATION = 5  # s
results = []

for track_id, track in df.groupby("Track ID"):
    track = track.sort_values("T")

    # Duration of the track
    duration = track["T"].max() - track["T"].min()

    # Only consider tracks with the minimum duration
    if duration >= MIN_DURATION:
        # Linear fit: X = (dx/dt) * T + b
        fit = linregress(track["T"], track["X"])

        results.append({
            "Track ID": int(track_id),
            "Duration (s)": duration,
            "dx/dt (um/s)": fit.slope,   # velocity = slope of the fit
            "R2": fit.rvalue ** 2
        })

# ============================================================
# 3. SELECT THE 3 TRACKS WITH THE HIGHEST R2
# ============================================================
results = pd.DataFrame(results).sort_values("R2", ascending=False)
top3 = results.head(3)

print("3 BEST TRACKS")
print(top3.to_string(index=False))

# ============================================================
# 4. MEAN AND STANDARD DEVIATION OF THE VELOCITY
# ============================================================
velocities = top3["dx/dt (um/s)"]
mean_velocity = velocities.mean()
standard_deviation = velocities.std(ddof=1)

print(f"Terminal velocity = {mean_velocity:.4f} +/- "
      f"{standard_deviation:.4f} um/s")
