import pandas as pd
import re
from pathlib import Path

# Path de los archivos de conteo
RESULTS_DIR = Path("./results/aligned")

# Lista de cuantificadores a procesar
cuants = ["hisat2_PE", "star_PE"]

# Dict de los paths de cada matriz
count_files = {cuant: RESULTS_DIR / cuant / "counts_per_gene_0.txt" for cuant in cuants}

# Path para guardar matrices homogenizadas
OUTPUT_DIR = Path("./results/DEG/count_matrices")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Limpieza de matrices
def clean_matrix(df) -> pd.DataFrame:
  """
  Pasos generales de homogenización para matrices de conteos.
  """
  # Limpiar nombres de muestras
  df.columns = clean_sample_names(df.columns)
  # Convertir el input a numérico
  df = df.apply(pd.to_numeric)
  # Siempre valores enteros (salmon tiene floats)
  df = df.round().astype(int)
  
  return df

# Limpieza de nombres de muestras
def clean_sample_names(columns) -> list:
  """
  Homogeniza los nombres de las muestras a partir de los nombres de las columnas,
  eliminando partes comunes y dejando solo el identificador de la muestra.
  """
  # Lista de nombres limpios
  cleaned = []
  for col in columns:
    # Quitar path y dejar solo el nombre del archivo
    sample = re.sub(r".*/", "", col)
    # Quitar sufijos de las tablas de STAR
    sample = re.sub(r"_Aligned.sortedByCoord.out.fs.bam", "", sample)
    # Quitar sufijos de las tablas de HISAT2
    sample = re.sub(r"\.fs\.bam", "", sample)

    cleaned.append(sample)
  return cleaned

# Carga de matrices de featureCounts
def load_featurecounts_matrix(path) -> pd.DataFrame:
  """
  Carga matriz de conteos de featureCounts, eliminando columnas de metadatos y
  homogenizando nombres de muestras.
  """
  # Cargar tabla de conteos
  df = pd.read_csv(path, sep="\t", comment="#")
  # Quitar columnas no necesarias, si existen
  df = df.drop(columns=["Chr", "Start", "End", "Strand", "Length"], errors="ignore")
  # gene_id como índice
  df = df.set_index("Geneid")

  return clean_matrix(df)

# Si hubiera de Salmon
def load_salmon_matrix(path) -> pd.DataFrame:
  """
  Carga matriz de conteos de salmon.
  """
  df = pd.read_csv(path, sep="\t", index_col=0)
  return clean_matrix(df)

def load_matrix(path, method="featureCounts") -> pd.DataFrame:
  """
  Wrapper para cargar matrices de conteos, dependiendo del método de cuantificación utilizado.
  """
  if method.lower() == "salmon":
    return load_salmon_matrix(path)
  return load_featurecounts_matrix(path)

# Pipeline de homogenización

# Dict para las matrices de conteos
matrices = {}

for dataset, path in count_files.items():
  # Método según el nombre del dataset 
  method = "salmon" if "salmon" in dataset.lower() else "featureCounts"
  # Guardar matriz limpia en el dict
  matrices[dataset] = load_matrix(path, method)

# Encontrar genes comunes entre las matrices
# '*' desempaqueta la lista de sets para ser argumento del set
common_genes = set.intersection(*[set(df.index) for df in matrices.values()])

# Ordenar los genes
common_genes = sorted(common_genes)

print(f"Genes comunes entre las matrices: {len(common_genes)}")

for dataset in matrices:
  df = matrices[dataset]

  # Solo las filas de los genes comunes
  df = df.loc[common_genes]
  # Ordenar columnas alfabéticamente --> Iguales entre matrices
  df = df[sorted(df.columns)]
  # Matriz filtrada y ordenada en el dict
  matrices[dataset] = df

  print(f"{dataset}: {df.shape}")

# Guardar matrices homogenizadas
for dataset, df in matrices.items():
  output_file = OUTPUT_DIR / f"{dataset}_counts.tsv"
  df.to_csv(output_file, sep="\t")