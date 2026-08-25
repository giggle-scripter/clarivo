# Clarivo data

Expected data areas:

```text
external/    Public datasets downloaded from their original sources
raw/         Original Clarivo recordings
processed/   Derived datasets
annotated/   Reviewed labels and annotations
benchmark/   Reproducible evaluation sets
```

Large raw datasets and audio files are intentionally ignored by Git. Commit
only small metadata or annotations where licensing permits, plus scripts and
instructions needed to reproduce the data locally.
