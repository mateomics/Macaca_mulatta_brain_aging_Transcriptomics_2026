# Transcriptomic Analysis of Brain Aging in *Macaca mulatta*

## Overview

This project investigates transcriptomic changes associated with normal brain aging in the dorsolateral prefrontal cortex (dlPFC) of female *Macaca mulatta* using bulk RNA-seq data.

The analysis reproduces a complete RNA-seq workflow, from raw sequencing reads to biological interpretation, including differential expression analysis and functional enrichment.

Dataset source:

- BioProject: PRJNA743289
- GEO accession: GSE179330

The study focuses on comparing young (5–8 years) and adult (12–16 years) female macaques to identify age-associated transcriptional signatures.

---

## Objectives

- Perform quality assessment and preprocessing of RNA-seq reads.
- Align reads against the *Macaca mulatta* reference genome.
- Quantify gene expression levels.
- Identify differentially expressed genes (DEGs) associated with aging.
- Characterize enriched biological processes and pathways.
- Explore transcriptomic signatures of normal primate brain aging.

---

## Pipeline

### 1. Sample Selection

Samples were filtered according to:

- Female individuals
- Dorsolateral prefrontal cortex (dlPFC)
- Paired-end RNA-seq
- Age groups:
  - Young: 5–8 years
  - Old: 12–16 years

Final dataset:

| Group | Samples |
|---------|---------|
| Young | 5 |
| Old | 5 |
| Total | 10 |

---

### 2. Quality Control

Tools:

- FastQC
- MultiQC

Evaluated metrics:

- Per-base quality scores
- Adapter contamination
- GC content
- Sequence duplication levels

---

### 3. Read Cleaning

Tool:

- fastp

Processing included:

- Adapter removal
- Poly-G trimming
- Low-quality tail trimming
- Removal of reads shorter than 50 bp

---

### 4. Alignment

Reference:

- *Macaca mulatta* Mmul_10
- Ensembl Release 115

Aligners:

- STAR
- HISAT2

STAR was selected for downstream analyses due to its higher uniquely mapped read rate.

---

### 5. BAM Processing

Tool:

- samtools

Steps:

- MAPQ filtering (≥10)
- Sorting
- Indexing

---

### 6. Gene Quantification

Tool:

- featureCounts

Settings:

- Paired-end fragment counting
- Properly paired reads only
- Largest-overlap assignment strategy

---

### 7. Differential Expression Analysis

Tools:

- DESeq2
- edgeR

Reported results correspond to DESeq2.

Criteria for differential expression:

- Adjusted p-value < 0.05
- |log2FC| > 0.5

Statistical design:

```R
~ 0 + condition
```

Comparison:

```text
old vs young
```

---

### 8. Functional Enrichment

Performed using:

- Gene Ontology (GO)
- DAVID
- STRING
- GSEA (MSigDB Hallmark)

Because most enrichment databases are curated for humans, *Macaca mulatta* genes were mapped to human orthologs prior to downstream analyses.

---

## Main Findings

### Differential Expression

A small but biologically meaningful set of genes was identified as differentially expressed between age groups.

### Functional Signals

Enrichment analyses suggested age-associated changes involving:

- Immune response
- Inflammatory signaling
- Apoptosis
- Interferon response
- Angiogenesis
- Neuronal maintenance pathways

### Network Analysis

STRING identified modules related to:

- Myelination
- Oligodendrocyte-associated genes
- TNF signaling
- Cellular stress responses

### GSEA

Hallmark pathways showed enrichment patterns associated with:

- Interferon alpha response
- Apoptosis
- Inflammatory response
- Epithelial-mesenchymal transition (EMT)

---

## Project Structure

```text
.
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── metadata/
│   └── references/
│
├── scripts/
│
├── results/
│   ├── aligned/
│   ├── DEG/
│   ├── GO/
│   └── count_matrices/
│
├── docs/
│
└── README.md
```

---

## Software

| Tool | Version |
|--------|--------|
| Python | 3.11 |
| R | 4.5 |
| FastQC | 0.12.1 |
| MultiQC | 1.33 |
| fastp | 0.24.1 |
| STAR | 2.7.11b |
| HISAT2 | 2.2.1 |
| samtools | 1.21 |
| featureCounts | 2.0.8 |
| DESeq2 | Bioconductor |
| edgeR | Bioconductor |

---

## Reproducibility

The workflow follows:

```text
SRA download
    ↓
FastQC / MultiQC
    ↓
fastp
    ↓
STAR / HISAT2
    ↓
samtools
    ↓
featureCounts
    ↓
DESeq2 / edgeR
    ↓
GO / STRING / GSEA
```

All scripts, parameters, and analysis steps are included in this repository to facilitate reproducibility.

---

## References

Chiou KL et al. (2022). *Multiregion transcriptomic profiling of the primate brain reveals signatures of aging and the social environment*. Nature Neuroscience.

DOI: https://doi.org/10.1038/s41593-022-01197-0
