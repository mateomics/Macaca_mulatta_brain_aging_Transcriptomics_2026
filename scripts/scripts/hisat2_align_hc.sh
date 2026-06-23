#!/bin/bash
#$ -cwd
#$ -o results/featureCounts/featureCounts_$JOB_ID.out
#$ -e results/featureCounts/featureCounts_$JOB_ID.err
#$ -pe smp 8

set -euo pipefail

BAM_PATH=$1
GTF=$2
STRAND=$3

LOG="${BAM_PATH}/featureCounts_${STRAND}_log.txt"
echo "Starting job on $(hostname)" >> "$LOG"
echo "FeatureCounts" >> "$LOG"
echo -e "\tMode: PE" >> "$LOG"
echo -e "\tStrand type: $STRAND" >> "$LOG"
echo -e "\tPath: $BAM_PATH" >> "$LOG"
echo "Date: $(date)" >> "$LOG"

conda activate subread

# Comando con medición de tiempo y recursos
/usr/bin/time -v featureCounts \
  -o "${BAM_PATH}/counts_per_gene_${STRAND}.txt" \
  -T 8 \
  -a "${GTF}" \
  --largestOverlap \
  -p -B -s ${STRAND} \
  --countReadPairs \
  "${BAM_PATH}"/*fs.bam \
  2>> "${LOG}"

conda deactivate
