#!/bin/bash
#$ -cwd
#$ -pe smp 8
#$ -l h_vmem=16G
#$ -o results/aligned/star_$JOB_ID.out
#$ -e results/aligned/star_$JOB_ID.err

set -euo pipefail

# Default single-end
MODE="SE"

# Flag para paired-end
while getopts "p" opt; do # Manejo de flags
  case $opt in
    p)
      MODE="PE"
      ;;
  esac
done

shift $((OPTIND -1)) # Elimina argumentos ya procesados por getopts

SRR=$1

DATA="./data/cleaned"
OUT="./results/aligned/star_${MODE}"
INDEX=$2
LOG_DIR="./logs/STAR"

mkdir -p $OUT; mkdir -p $LOG_DIR

LOG="${LOG_DIR}/star_log.txt"
echo "Starting job on $(hostname)" > $LOG
echo "STAR alignment" >> $LOG
echo -e "\tMode: $MODE" >> $LOG
echo -e "\tSample: $SRR" >> $LOG
echo "Date: $(date)" >> $LOG

conda activate star

# /usr/bin/time para medir el tiempo y uso de recursos
INPUT="${DATA}/${SRR}_1.cleaned.fastq.gz"
if [ "$MODE" = "PE" ]; then
  # Ambos argumentos en la misma variable
  INPUT="${INPUT} ${DATA}/${SRR}_2.cleaned.fastq.gz"
fi

# Incluye reads mapeados y no mapeados en el bam
/usr/bin/time -v STAR \
  --genomeDir $INDEX \
  --readFilesIn ${INPUT} \
  --readFilesCommand zcat \
  --runThreadN 8 \
  --outFileNamePrefix ${OUT}/${SRR}_ \
  --outSAMtype BAM SortedByCoordinate \
  --outSAMunmapped Within \
  2>> ${LOG_DIR}/${SRR}_time.log

conda deactivate
