"""Ranking species by total reads across all samples."""
import pandas as pd

def top_species(asv_file="ESI22.COI.FilteredMergedASVtable.csv", n=10):
    df = pd.read_csv(asv_file)
    sample_cols = [c for c in df.columns if c.startswith("Sample.")]
    df["Total reads"] = df[sample_cols].sum(axis=1)
    return (df.groupby("Species")["Total reads"].sum()
              .sort_values(ascending=False).head(n).reset_index())

if __name__ == "__main__":
    top_species()