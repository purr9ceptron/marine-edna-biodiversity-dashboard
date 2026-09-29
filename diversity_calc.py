"""Computing species richness, Shannon and Simpson diversity for each water sample."""
import numpy as np
import pandas as pd

ASV_FILE = "ESI22.COI.FilteredMergedASVtable.csv"
OUT_FILE = "ESI22_COI_biodiversity_results.csv"


def compute_diversity(asv_file=ASV_FILE):
    df = pd.read_csv(asv_file)
    sample_cols = [c for c in df.columns if c.startswith("Sample.")]


    species_reads = df.groupby("Species")[sample_cols].sum()

    rows = {}
    for sample in sample_cols:
        reads = species_reads[sample]
        reads = reads[reads > 0]
        if reads.empty:  # no DNA detected in this sample
            rows[sample] = {"Richness": 0, "Shannon Index": 0.0, "Simpson Index": 0.0}
            continue
        p = reads / reads.sum()
        rows[sample] = {
            "Richness": len(reads),
            "Shannon Index": float(-(p * np.log(p)).sum()),
            "Simpson Index": float(1 - (p ** 2).sum()),
        }

    result = pd.DataFrame(rows).T
    result["Richness"] = result["Richness"].astype(int)
    result.index.name = "Sample"
    return result


if __name__ == "__main__":
    table = compute_diversity()
    table.round(4).to_csv(OUT_FILE)
