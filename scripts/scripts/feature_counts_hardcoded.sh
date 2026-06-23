#!/bin/bash
#$ -cwd
#$ -pe smp 8
#$ -o results/featureCounts/featureCounts_$JOB_ID.out
#$ -e results/featureCounts/featureCounts_$JOB_ID.err

set -euo pipefail

LIBRARY=$1

echo "Starting featureCounts on $(hostname)"
echo "Date: $(date)"

# Inicializar conda en shell batch
eval "$(conda shell.bash hook)"
conda activate subread

GTF="./data/references/Macaca_mulatta.Mmul_10.115.gtf"

mkdir -p results/featureCounts

########################################
# HISAT2 paired-end
########################################

echo "Running HISAT2 paired-end counting..."

/usr/bin/time -v featureCounts \
  -o "./results/aligned/hisat2_PE/counts_per_gene_${LIBRARY}.txt" \
  -T 8 \
  -a "$GTF" \
  --largestOverlap \
  -p \
  --countReadPairs \
  -B \
  -s $LIBRARY \
  ./results/aligned/hisat2_PE/*fs.bam

########################################
# STAR paired-end
########################################

echo "Running STAR paired-end counting..."

/usr/bin/time -v featureCounts \
  -o "./results/aligned/star_PE/counts_per_gene_${LIBRARY}.txt" \
  -T 8 \
  -a "$GTF" \
  --largestOverlap \
  -p \
  --countReadPairs \
  -B \
  -C \
  -s $LIBRARY \
  ./results/aligned/star_PE/*fs.bam

conda deactivate

echo "Finished at $(date)"
