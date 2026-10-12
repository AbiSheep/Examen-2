from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.impute import KNNImputer

# --------------------------------------------------------------------------
# Constantes (un solo lugar, en vez de "numeros magicos" repartidos)
# --------------------------------------------------------------------------
RAIZ = Path(__file__).parent
CSV_CRUDO = RAIZ / "data" / "cdmx_air_traffic_dirty.csv"
CSV_LIMPIO = RAIZ / "data" / "df_clean.csv"

CENTINELA = -999.0
COLS_NUM = ["Concentracion_PM25", "Nivel_NO2", "Indice_Trafico_Vehicular"]
FACTOR_IQR = 1.5
K_VECINOS = 2
UMBRAL_R = 0.85

# ==========================================================================
# TAREA 1: ingesta, diagnostico y centinelas
# ==========================================================================
def tarea1(df_raw: pd.DataFrame) -> pd.DataFrame:
    # a) Diagnóstico inicial de duplicados y centinelas 
    print("Tipos de datos:\n", df_raw.dtypes)
    print("Dimensiones:\n", df_raw.shape)
    print("\nNaN por columna:\n", df_raw.isna().sum())
    print(f"\nCentinelas ({CENTINELA}) por columna numerica:\n",
          (df_raw[COLS_NUM] == CENTINELA).sum())
    print("\nFilas duplicadas:", df_raw.duplicated().sum())

    # b) Reemplazar centinela -999.0 por np.nan y eliminar duplicados 
    df = df_raw.replace(CENTINELA, np.nan)
    df = df.drop_duplicates()
    return df


# ==========================================================================
# TAREA 2: pipeline de limpieza (el ORDEN importa: IQR antes de imputar)
# ==========================================================================
def tarea2(df_t1: pd.DataFrame) -> pd.DataFrame:
    df = df_t1.copy()
    # 1. Homogeneizar 'Zona_Estacion' 
    df["Zona_Estacion"] = df["Zona_Estacion"].str.title().str.replace(" ", "_")
    print("\nZonas unicas:\n", df["Zona_Estacion"].unique())
     
    # 2. Convertir Timestamp a datetime y extraer Hora_Dia
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Hora_Dia"] = df["Timestamp"].dt.hour

    # Ordenar la nueva columna justo después de Timestamp
    columnas = df.columns.tolist()
    idx_hora = columnas.index("Hora_Dia")
    columnas.insert(columnas.index("Timestamp") + 1, columnas.pop(idx_hora))
    df = df[columnas]

    # 3. Detección de outliers por IQR en 'Concentracion_PM25' y sustitución por np.nan 
    q1,q3 = df["Concentracion_PM25"].quantile([0.25, 0.75])
    iqr = q3 - q1
    limites = (q1 - FACTOR_IQR*iqr, q3 + FACTOR_IQR*iqr)
    fuera_de_limites = (df["Concentracion_PM25"] < limites[0]) | (df["Concentracion_PM25"] > limites[1])
    df.loc[fuera_de_limites, "Concentracion_PM25"] = np.nan

    # 4. Imputación avanzada k-NN sobre variables numéricas 
    imp = KNNImputer(n_neighbors=K_VECINOS)
    df[COLS_NUM] = imp.fit_transform(df[COLS_NUM])
    return df


# ==========================================================================
# TAREA 3: EDA y multicolinealidad
# ==========================================================================
def tarea3(df: pd.DataFrame) -> None:
    print("\nResumen estadistico:\n", df.describe())
    print("\nResumen estadistico de Concentracion_PM25:\n", df["Concentracion_PM25"].describe())

    # 1. Estadísticas de forma para Concentracion_PM25
    # Se imprimen la media, mediana, desviación estándar, asimetría y curtosis.
    estadisticos_pm25 = df["Concentracion_PM25"].agg(["mean", "median", "std", "skew", "kurt"])
    print("\nEstadisticos de forma de Concentracion_PM25:\n", estadisticos_pm25)
    print("\nCurtosis de Concentracion_PM25:\n", df["Concentracion_PM25"].kurt())
    print("\nSkewness de Concentracion_PM25:\n", df["Concentracion_PM25"].skew())

    # 2. Matrices de correlación Pearson y Spearman
    corr_p = df.corr(method="pearson", numeric_only=True)
    corr_s = df.corr(method="spearman", numeric_only=True)
    print("\nCorrelacion de Pearson:\n", corr_p)
    print("\nCorrelacion de Spearman:\n", corr_s)

    # 3. Visualización de correlaciones
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.heatmap(corr_p, annot=True, cmap="coolwarm", center=0, ax=axes[0], fmt=".2f")
    axes[0].set_title("Correlación de Pearson")
    sns.heatmap(corr_s, annot=True, cmap="coolwarm", center=0, ax=axes[1], fmt=".2f")
    axes[1].set_title("Correlación de Spearman")
    fig.tight_layout()
    fig.savefig("correlaciones.png")
    plt.close(fig)

    # 4. Diagnóstico de multicolinealidad
    # Se buscan pares con |r| >= UMBRAL_R sin repetir la diagonal ni pares duplicados.
    abs_corr = corr_p.abs()
    mask = np.triu(np.ones_like(abs_corr, dtype=bool), k=1)
    pares_altos = (
        abs_corr.where(~mask)
        .stack()
        .loc[lambda s: s >= UMBRAL_R]
        .sort_values(ascending=False)
    )
    print("\nPares altamente correlacionados (|r| >= 0.85):")
    if pares_altos.empty:
        print("  No se encontraron pares con correlación mayor o igual al umbral.")
    else:
        for (var1, var2), valor in pares_altos.items():
            print(f"  {var1} - {var2}: |r| = {valor:.3f}")


if __name__ == "__main__":
    # 1. Cargar o definir el dataset 
    df_raw = pd.read_csv(CSV_CRUDO)
    df_t1 = tarea1(df_raw)
    df_clean = tarea2(df_t1)
    print("\nNaN restantes:\n", df_clean.isna().sum())
    df_clean.to_csv(CSV_LIMPIO, index=False)  
    print("Guardado:", CSV_LIMPIO)
    tarea3(df_clean)
    plt.show()
