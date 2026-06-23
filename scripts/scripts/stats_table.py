import os
import subprocess as sp
import pandas as pd
import glob
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import gzip
from pathlib import Path

# Extraer de procentajes en falgstat
def extract_percentage(line):
  match = re.search(r"\(([\d\.]+)%", line)
  return float(match.group(1)) if match else None

# === Stats de Flagstat ===

# Lista de dicts para almacenar la información
records = [] 

# Glob de todos los logs
log_files = ( glob.glob("./logs/HISAT2/*time.log") + glob.glob("./logs/STAR/*time.log") )

for log in log_files:

  # Log de tiempo y recursos correspondiente
  with open(log) as file:
    text = file.read()

  # Minutos, segundos y decimales si hay
  time_match = re.search(r"Elapsed.*: (\d+):(\d+\.?\d*)", text)
  # CPU usado
  cpu_match = re.search(r"Percent of CPU.*: (\d+)", text)
  # Memoria máxima en Kb
  mem_match = re.search(r"Maximum resident set size.*: (\d+)", text)

  # Tiempo en segundos
  time_sec = None
  if time_match:
    # Lo capturado en el group respectivo
    minutes = int(time_match.group(1))
    seconds = float(time_match.group(2))
    time_sec = minutes*60 + seconds # Más legible

  cpu = int(cpu_match.group(1)) if cpu_match else None
  mem_gb = int(mem_match.group(1)) / (1024**2) if mem_match else None

  # Metadatos a partir del path
  tool = os.path.basename(os.path.dirname(log)).upper()
  sample = os.path.basename(log).split("_")[0] # <SRR>.log --> <SRR>

  # Directorio según alineador
  align_dir = f"./results/aligned/{tool.lower()}_PE"

  # Nombre del flagstat
  flagstat_name = f"{sample}_flagstat.txt"

  if tool == "STAR":
    flagstat_name = f"{sample}_Aligned.sortedByCoord.out_flagstat.txt"

  # Path completo
  flagstat_path = os.path.join(align_dir, flagstat_name)

  # Información del alineamiento
  total = primary_mapped = primary_mapped_pct = properly_paired = None

  if os.path.exists(flagstat_path):
    with open(flagstat_path) as file:
      for line in file:
        if "in total" in line:
          total = int(line.split()[0])

        elif "primary mapped (" in line:
          primary_mapped = int(line.split()[0])
          primary_mapped_pct = extract_percentage(line)

        elif "properly paired" in line:
          properly_paired = extract_percentage(line)

  # Dict con la información del alineamiento
  records.append({
    # Muestra
    "Sample": sample,
    "Tool": tool,
    "Mode": "PE",
    # Recursos
    "Time (s)": time_sec,
    "Memory (GB)": mem_gb,
    "CPU (%)": cpu,
    # Estadísticas de alineamiento
    "Total reads": total,
    "Primary mapped reads": primary_mapped,
    "Primary mapped (%)": primary_mapped_pct,
    "Properly paired (%)": properly_paired
  })

df = pd.DataFrame(records)

# === Stats de mapeo único ===

unique_records = []

with open("./results/aligned/unique_mapping_rate_per_sample.txt") as file:
  for line in file:
    # STAR
    if "Uniquely mapped reads %" in line:
      sample_match = re.search(r"(SRR\d+)", line)
      pct_match = re.search(r"([\d\.]+)%", line)
      sample = sample_match.group(1)
      pct = float(pct_match.group(1))
      unique_records.append({
        "Sample": sample,
        "Tool": "STAR",
        "Unique mapping (%)": pct
      })

    # HISAT2
    elif "aligned concordantly exactly 1 time" in line:
      sample_match = re.search(r"(SRR\d+)", line)
      pct_match = re.search(r"\(([\d\.]+)%\)", line)
      sample = sample_match.group(1)
      pct = float(pct_match.group(1))
      unique_records.append({
        "Sample": sample,
        "Tool": "HISAT2",
        "Unique mapping (%)": pct
      })

unique_df = pd.DataFrame(unique_records)

# === Merge de ambos ===

df = df.merge(unique_df, on=["Sample", "Tool"], how="left")
# Exportamos el df a tsv
df.to_csv("./results/aligned/alignment_stats.tsv", sep="\t", index=False)
