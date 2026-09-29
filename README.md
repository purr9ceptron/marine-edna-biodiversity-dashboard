# Marine eDNA Biodiversity Dashboard

Streamlit dashboard that analyses marine eDNA metabarcoding data (COI gene): 91 water samples and 178 species.

## What it does
- Calculates species richness, Shannon index and Simpson index per sample (`diversity_calc.py`)
- Flags low-biodiversity sites using an adjustable Shannon threshold, and lists samples with no DNA detected separately
- Shows top species by total reads, a single-sample inspector, and labelled charts (`plots.py`)

## Run it
```
pip install -r requirements.txt
python diversity_calc.py
python plots.py
streamlit run app.py
```

## Status
- Dashboard and diversity analysis: done
- DNA sequence species classifier (k-mers + Naive Bayes): in progress, practised on human/chimp/dog sequences, not yet connected to this data
