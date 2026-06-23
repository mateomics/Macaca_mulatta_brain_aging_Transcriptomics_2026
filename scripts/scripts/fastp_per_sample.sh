#!/bin/bash
#$ -cwd
#$ -o logs/fastp_$JOB_ID.out
#$ -e logs/fastp_$JOB_ID.err

set -euo pipefail

RAW_PATH="./data/raw"
TRIMMED_PATH="./data/trimmed"

mkdir -p "${TRIMMED_PATH}"

LOG="./logs/fastp_log.txt"
echo "Starting job on $(hostname)" > $LOG
echo "Date: $(date)" >> $LOG

conda activate fastp

for file in ${RAW_PATH}/SRR*_1.fastq.gz; do
  srr=$(basename "$file" _1.fastq.gz) # Solo el SRR

  BASE_RAW="${RAW_PATH}/${srr}"
  BASE_TRIMMED="${TRIMMED_PATH}/${srr}"

  # Paired End
  fastp \
    -i "${BASE_RAW}_1.fastq.gz" -I "${BASE_RAW}_2.fastq.gz" \
    -o "${BASE_TRIMMED}_1.trimmed.fastq.gz" \
    -O "${BASE_TRIMMED}_2.trimmed.fastq.gz" \
    --detect_adapter_for_pe --trim_poly_g \
    --cut_tail --length_required 35 --thread 8 \
    --json "${TRIMMED_PATH}/${srr}.json" \
    --html "${TRIMMED_PATH}/${srr}.html"
done

conda deactivate

echo "Job finished at $(date)" >> $LOG
