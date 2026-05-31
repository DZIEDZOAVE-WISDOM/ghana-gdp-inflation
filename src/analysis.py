"""
Ghana GDP Growth vs. Inflation (1970-2024)
Reads the World Bank WDI series and plots both on a shared time axis with a
secondary y-axis, annotating the major peaks and troughs.

The two y-axes are symmetric (GDP -15..15, inflation -140..140) so their zero
lines coincide at the vertical centre of the plot.

Source: World Bank, World Development Indicators
    - GDP growth (annual %)                  [NY.GDP.MKTP.KD.ZG]
    - Inflation, consumer prices (annual %)  [FP.CPI.TOTL.ZG]
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ghana_gdp_inflation_1970_2024.csv"
OUT = ROOT / "figures" / "ghana_gdp_inflation_1970_2024.png"

GDP_C = "#2E74B5"   # blue
INF_C = "#C00000"   # red

pct = FuncFormatter(lambda v, _: f"{v:.0f}%")


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    return df.sort_values("year").reset_index(drop=True)


def plot(df: pd.DataFrame) -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.edgecolor": "#bfbfbf",
        "axes.linewidth": 0.8,
    })

    fig, ax1 = plt.subplots(figsize=(13, 7))

    # GDP growth (left axis) — symmetric -15..15
    ax1.plot(df.year, df.gdp_growth, color=GDP_C, lw=1.8,
             label="GDP growth (annual %)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("GDP growth (annual %)", color="#404040")
    ax1.set_ylim(-15, 15)
    ax1.yaxis.set_major_locator(MultipleLocator(5))
    ax1.yaxis.set_major_formatter(pct)
    ax1.xaxis.set_major_locator(MultipleLocator(5))
    ax1.set_xlim(1970, 2024)
    ax1.grid(True, axis="y", color="#d9d9d9", lw=0.8)
    ax1.set_axisbelow(True)

    # Inflation (right axis) — symmetric -140..140 so zero aligns with GDP zero
    ax2 = ax1.twinx()
    ax2.plot(df.year, df.inflation, color=INF_C, lw=1.8,
             label="Inflation, consumer prices (annual %)")
    ax2.set_ylabel("Inflation (annual %)", color="#404040")
    ax2.set_ylim(-140, 140)
    ax2.yaxis.set_major_locator(MultipleLocator(20))
    ax2.yaxis.set_major_formatter(pct)

    # Event annotations: (year, text, axis, (dx, dy) offset in points).
    # Text colour follows the axis: blue for GDP events, red for inflation.
    notes = [
        (1977, "1977: inflation 116%", ax2, (-66, 14)),
        (1983, "1983: 123% drought", ax2, (12, 10)),
        (1984, "1983: ERP begins", ax1, (12, 0)),
        (1995, "1995: inflation 59%", ax2, (14, 6)),
        (2011, "2011: GDP +14% (oil boom)", ax1, (-150, 2)),
        (2023, "2022-23 debt crisis", ax2, (-70, 30)),
        (2020, "2020: COVID, GDP 0.5%", ax1, (-30, -48)),
        (1982, "1982: GDP -6.9% (pre-ERP trough)", ax1, (10, -40)),
        (1975, "1975: GDP -12.4%", ax1, (14, -10)),
    ]
    for yr, txt, ax, off in notes:
        col = df.loc[df.year == yr].iloc[0]
        y = col.gdp_growth if ax is ax1 else col.inflation
        colour = GDP_C if ax is ax1 else INF_C
        ax.annotate(txt, xy=(yr, y), xytext=(off[0], off[1]),
                    textcoords="offset points", fontsize=8.5,
                    color=colour, fontweight="bold", ha="left",
                    arrowprops=dict(arrowstyle="-", color="#9a9a9a", lw=0.8))

    # Combined legend along the bottom
    l1, lab1 = ax1.get_legend_handles_labels()
    l2, lab2 = ax2.get_legend_handles_labels()
    fig.legend(l1 + l2, lab1 + lab2, loc="lower center",
               ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.02))

    fig.suptitle("Ghana: GDP Growth and Inflation, 1970-2024",
                 fontsize=14, fontweight="bold", y=0.97)

    fig.tight_layout(rect=[0, 0.04, 1, 0.96])
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(f"Saved -> {OUT}")


if __name__ == "__main__":
    plot(load())
