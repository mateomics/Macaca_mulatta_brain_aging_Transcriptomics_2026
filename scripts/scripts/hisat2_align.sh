#!/bin/bash
#$ -cwd
#$ -pe smp 8
#$ -l h_vmem=8G
#$ -o results/aligned/hisat2_$JOB_ID.out
#$ -e results/aligned/hisat2_$JOB_ID.err

set -euo pipefail

# Default single-end
MODE="SE"

# Flag para paired-end
while getopts "p" opt; do
  case $opt in
    p)
      MODE="PE"
      ;;
  esac
done

shift $((OPTIND -1))

SRR=$1

DATA="./data/cleaned"
OUT="./results/aligned/hisat2_${MODE}"
INDEX=$2
LOG_DIR="./logs/HISAT2"

mkdir -p $OUT
mkdir -p $LOG_DIR

LOG="${LOG_DIR}/hisat2_log.txt"
echo "Starting job on $(hostname)" > $LOG
echo "HISAT2 alignment" >> $LOG
echo -e "\tMode: $MODE" >> $LOG
echo -e "\tSample: $SRR" >> $LOG
echo "Date: $(date)" >> $LOG

# /usr/bin/time para medir el tiempo y uso de recursos
if [ "$MODE" = "SE" ]; then
  INPUT="-U ${DATA}/${SRR}_1.cleaned.fastq.gz"
else
  INPUT="-1 ${DATA}/${SRR}_1.cleaned.fastq.gz -2 ${DATA}/${SRR}_2.cleaned.fastq.gz"
fi

/usr/bin/time -v hisat2 \
  -x $INDEX \
  $INPUT \
  -p 8 \
  -S ${OUT}/${SRR}.sam \
  --summary-file ${OUT}/${SRR}_summary.txt \
  2>> ${LOG_DIR}/${SRR}_time.log
