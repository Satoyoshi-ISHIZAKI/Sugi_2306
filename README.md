# Python-based analysis of the amplicon sequence data for the phyllosphere microbiome of Japanese cedar, collected in June 2306.

## Data sources
Amplicon sequence data is available in the DDBJ Sequence Read Archive under the accession number <b>PRJDB20421</b>.
<br>Same data as the following paper.
<br>https://doi.org/10.1038/s41598-025-16496-2

## Setup

### 1. FAPROTAX Configuration

Copy `scripts/config.example.py` to `scripts/config.py` and set your FAPROTAX installation path:

```bash
# Windows PowerShell
Copy-Item scripts\config.example.py scripts\config.py
```

Then edit `scripts/config.py` to specify your FAPROTAX installation path:

```python
# scripts/config.py
FAPROTAX_DIR = r"C:\Path\to\Your\FAPROTAX\Directory\FAPROTAX_1.2.12\FAPROTAX_1.2.12"
```

**Note**: `scripts/config.py` is included in `.gitignore`, so your personal path information will not be pushed to GitHub.

### 2. Usage

```python
from scripts.FAPROTAX import run_faprotax_simple

# Simple execution
run_faprotax_simple(
    'input_otu_table.tsv',
    'output_functional_table.tsv',
    'report.txt'
)
```

## About FAPROTAX

FAPROTAX (Functional Annotation of Prokaryotic Taxa) is a database and tool for inferring microbial functions from 16S rRNA gene sequence data.

- Official site: http://www.loucalab.com/archive/FAPROTAX/lib/php/index.php?section=Home