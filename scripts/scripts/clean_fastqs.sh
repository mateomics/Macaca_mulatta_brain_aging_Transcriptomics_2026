#!/usr/bin/env bash
set -euo pipefail

INPUT_DIR="$1"
OUT_DIR="$2"
THREADS="$3"

mkdir -p "${OUT_DIR}";
fastqc -t "${THREADS}" -o "${OUT_DIR}" "${INPUT_DIR}"/*.fastq.gz
multiqc "${OUT_DIR}" -o "${OUT_DIR}"
