from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker


def plot_spend_by_year(
    csv_path: str | Path,
    *,
    out_path: str | Path = "plot.png",
    show: bool = False,
) -> None:
    """Create a stacked bar chart of spend by year/category."""
    csv_path = Path(csv_path)
    out_path = Path(out_path)

    data = pd.read_csv(csv_path)

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"])
    data["year"] = data["date"].dt.to_period("Y")

    aggregated = (
        data.groupby(["year", "category"], dropna=False)
        .agg({"price_with_tax": "sum"})
        .reset_index()
    )

    pivot = (
        aggregated.pivot(index="year", columns="category", values="price_with_tax")
        .fillna(0)
        .sort_index()
    )

    # Keep 'Other' last for nicer legend ordering.
    pivot = pivot[sorted(pivot.columns, key=lambda x: (x == "Other", str(x)))]

    color_map = plt.colormaps["Accent"]

    ax = pivot.plot(
        kind="bar",
        stacked=True,
        figsize=(12, 8),
        color=[color_map(i) for i in range(len(pivot.columns))],
    )

    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.yaxis.grid(True, linestyle="dotted")

    category_sums = pivot.sum(axis=0)
    legend_labels = [f"{cat} (${total:.2f})" for cat, total in category_sums.items()]

    legend = ax.legend(
        legend_labels,
        title="",
        loc="upper center",
        ncol=2,
        bbox_to_anchor=(0.5, 0.925),
        handleheight=1.75,
        borderpad=1.5,
        labelspacing=1.25,
    )
    plt.setp(legend.get_texts(), fontsize=12)

    ax.set_xticklabels(
        [label.get_text() for label in ax.get_xticklabels()],
        fontsize=12,
        fontweight="bold",
        rotation=0,
    )
    for label in ax.get_xticklabels():
        label.set_y(label.get_position()[1] - 0.01)

    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: "" if pos == 0 else f"${x:0.0f}")
    )

    plt.title("Mobile Game Spendings by Year", fontsize=20, fontweight="bold")
    plt.xlabel("")
    plt.ylabel("")
    plt.yticks(fontsize=12)
    plt.tick_params(axis="x", which="both", length=0)
    plt.tick_params(axis="y", which="both", length=0)
    plt.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)

    if show:
        plt.show()
    else:
        plt.close(plt.gcf())
