"""
Figures for the README (English labels), saved in docs/figures/.

Inputs (not tracked by git), produced by the notebooks:
- ERA_PV_stazioni_clearsky_daily.csv       daily GHI of stations and ERA5-Land on clear-sky days
- ERA_PV_stazioni_clearsky_giornalieri.csv same, aggregated from the 9-15 hourly data (Untitled2.ipynb)

Usage:  python scripts/readme_figures.py [folder with the two CSV files]   (default: archive/ARPA)
"""
import sys
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "archive" / "ARPA"
OUT = ROOT / "docs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# stations whose measurements are affected by their siting (shading by trees, a tower, ...)
ANOMALOUS = ["BORGOMANERO", "MOMBALDONE", "MOMBARCARO", "PINO_TORINESE", "PONZONE", "TORINO"]
# stations used in pianura.ipynb for the mean station-ERA5 difference
SELECTED = ["ALBA", "CASALE_MONFERRATO", "ASTI", "ALESSANDRI", "AVIGLIANA", "BASALUZZO", "BORGOFRANCO_IVREA",
            "BRA", "CANDIA_CANAVESE", "CARMAGNOLA", "COSTIGLIOLE_SALUZZO", "CUMIANA", "CUNEO", "FOSSANO",
            "MONCALIERI", "NOVI_LIGURE", "SALICETO", "TREISO", "VERCELLI", "VEROLENGO", "VILLANOVA_SOLARO"]
SEASONS = {1: "winter", 2: "spring", 3: "summer", 4: "autumn"}
GREEN, DARKGREEN, BLUE, NAVY, RED = "#2ca02c", "#1b5e20", "#1f77b4", "#0b3d91", "#d62728"

plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def load_daily():
    d = pd.read_csv(DATA / "ERA_PV_stazioni_clearsky_daily.csv", sep=";")
    d["data"] = pd.to_datetime(d["data"], format="%d/%m/%Y")
    for c in ["rad", "shortwave_radiation"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.dropna(subset=["rad", "shortwave_radiation"])
    d["diff_pct"] = (d["rad"] - d["shortwave_radiation"]) / d["shortwave_radiation"] * 100
    return d


def station_bias(d):
    """Mean signed difference station - ERA5 for every station: the anomalous ones stand out."""
    s = d.groupby("nome")["diff_pct"].mean().sort_values()
    names = {"ALESSANDRI": "Alessandria", "BORGOFRANCO_IVREA": "Borgofranco d’Ivrea",
             "BUTTIGLIERA_D'ASTI": "Buttigliera d’Asti", "ISOLA_SANT'ANTONIO": "Isola Sant’Antonio"}
    labels = [names.get(n, n.replace("_", " ").title()) for n in s.index]
    colors = [RED if n in ANOMALOUS else GREEN for n in s.index]
    fig, ax = plt.subplots(figsize=(7, 7.5))
    ax.barh(range(len(s)), s.values, color=colors)
    ax.set_yticks(range(len(s)), labels, fontsize=9)
    ax.axvline(0, color="k", lw=0.6)
    for x in (-5, 5):
        ax.axvline(x, color="0.5", lw=0.8, ls=":")
    ax.set_xlabel("mean difference station − ERA5-Land on clear-sky days [%]")
    ax.set_title("Bias of each ARPA station (dotted: ±5% instrument accuracy)", fontsize=11)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(OUT / "station_bias.png", dpi=150)
    plt.close(fig)


def percentage_difference(d, window=20):
    """Daily mean |station - ERA5| / ERA5 over the selected stations, with a 20-day moving average."""
    k = d[d["nome"].isin(SELECTED)].copy()
    k["abs_pct"] = k["diff_pct"].abs()
    daily = k.groupby("data")["abs_pct"].mean()
    seasonal = daily.groupby(daily.index.month % 12 // 3 + 1).mean()
    text = f"mean {daily.mean():.1f}%\n" + "\n".join(f"{SEASONS[i]} {v:.1f}%" for i, v in seasonal.items())

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(daily.index, daily.values, "o", ms=3.5, color=GREEN, alpha=0.8, label="clear-sky day")
    ax.plot(daily.index, daily.rolling(window, min_periods=1).mean(), color=DARKGREEN, lw=2,
            label=f"moving average ({window} clear-sky days)")
    ax.text(0.99, 0.97, text, transform=ax.transAxes, ha="right", va="top", fontsize=10,
            bbox=dict(boxstyle="round", fc="white", ec="0.8"))
    ax.set_ylim(0, 20)
    ax.set_ylabel("mean |station − ERA5| / ERA5 [%]")
    ax.legend(loc="upper left", frameon=False)
    ax.xaxis.set_major_locator(mdates.YearLocator(4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout()
    fig.savefig(OUT / "station_vs_era5.png", dpi=150)
    plt.close(fig)


def spread():
    """Day-by-day spread (coefficient of variation) across stations vs across the ERA5 grid points."""
    g = pd.read_csv(DATA / "ERA_PV_stazioni_clearsky_giornalieri.csv")
    g["data"] = pd.to_datetime(g["data"])
    first = g.groupby("nome")["data"].min()
    long_running = first[first < "2005-01-01"].index
    g = g[g["nome"].isin(long_running) & g["nome"].isin(SELECTED)]  # same stations for both series

    fig, ax = plt.subplots(figsize=(9, 4.5))
    for col, label, c1, c2 in [("rad", "ARPA stations", GREEN, DARKGREEN),
                               ("shortwave_radiation", "ERA5-Land at the same sites", BLUE, NAVY)]:
        r = g.groupby("data")[col].agg(["mean", "std", "count"]).dropna()
        r["cv"] = r["std"] / r["mean"] * 100
        weighted = (r["cv"] * r["count"]).rolling(20, min_periods=1).sum() / r["count"].rolling(20, min_periods=1).sum()
        total = (r["cv"] * r["count"]).sum() / r["count"].sum()
        ax.plot(r.index, r["cv"], "o", ms=3, color=c1, alpha=0.7)
        ax.plot(r.index, weighted, color=c2, lw=2, label=f"{label} (weighted mean {total:.1f}%)")
    ax.set_ylabel("spread across sites (std / mean) [%]")
    ax.set_ylim(0, 15)
    ax.legend(loc="upper left", frameon=False)
    ax.xaxis.set_major_locator(mdates.YearLocator(4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout()
    fig.savefig(OUT / "spread_stations_vs_era5.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    d = load_daily()
    station_bias(d)
    percentage_difference(d)
    spread()
    print("figures written to", OUT)
