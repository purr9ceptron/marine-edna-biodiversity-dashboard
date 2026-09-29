"""Making one labelled bar chart per diversity measure (top 15 and bottom 15 samples)."""
import pandas as pd
import matplotlib.pyplot as plt

RESULTS = "ESI22_COI_biodiversity_results.csv"
CHARTS = {
    "Richness": ("Species richness", "Number of species"),
    "Shannon Index": ("Shannon diversity index", "Shannon index"),
    "Simpson Index": ("Simpson diversity index", "Simpson index"),
}


def make_chart(df, column, title, ylabel, filename):
    ranked = df.sort_values(column, ascending=False)
    picked = pd.concat([ranked.head(15), ranked.tail(15)])
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("#0B2027")
    ax.set_facecolor("#0B2027")
    ax.bar(picked["Sample"], picked[column], color="#6ECEBB")
    ax.set_title(f"{title}: top 15 and bottom 15 samples", color="#E8DCC4")
    ax.set_ylabel(ylabel, color="#E8DCC4")
    ax.set_xlabel("Water sample", color="#E8DCC4")
    ax.tick_params(colors="#E8DCC4")
    plt.setp(ax.get_xticklabels(), rotation=90)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    data = pd.read_csv(RESULTS)
    for col, (title, ylabel) in CHARTS.items():
        name = f"ESI22_COI_{col.split()[0].lower()}_results.png"
        make_chart(data, col, title, ylabel, name)
