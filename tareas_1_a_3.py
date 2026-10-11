"""
tareas_1_a_3.py  -  TAREAS 1, 2 y 3 en un solo script
=============================================================================
QUE HACE:
    Carga el CSV sucio, lo diagnostica y limpia (T1), aplica el pipeline de
    limpieza e imputacion (T2), hace el EDA (T3) y guarda data/df_clean.csv,
    que es el archivo que consume la app de Streamlit.

QUE PROBLEMA RESUELVE:
    Reproducir todo el procesamiento con un solo comando y separar la
    limpieza (aqui) de la visualizacion (app_ecotransito.py).

USO:
    python tareas_1_a_3.py

Todo vive en este archivo, asi no hay imports entre modulos que puedan fallar.
"""

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

    print("Dimensiones:", df_raw.shape)
    print("\nNaN por columna:\n", df_raw.isna().sum())
    print(f"\nCentinelas ({CENTINELA}) por columna numerica:\n",
          (df_raw[COLS_NUM] == CENTINELA).sum())
    print("\nFilas duplicadas:", df_raw.duplicated().sum())

    df = df_raw.replace(CENTINELA, np.nan)   # dato falso -> dato ausente
    df = df.drop_duplicates()                # un registro repetido pesa doble
    return df


# ==========================================================================
# TAREA 2: pipeline de limpieza (el ORDEN importa: IQR antes de imputar)
# ==========================================================================
def tarea2(df_t1: pd.DataFrame) -> pd.DataFrame:
    df = df_t1.copy()

    # TODO 2a: homogeneizar df["Zona_Estacion"] (str.lower()/map o str.title())
    #          Debe quedar: Centro_Historico, Zona_Oriente, Zona_Sur.

    # TODO 2b: df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    # TODO 2c: df["Hora_Dia"] = df["Timestamp"].dt.hour

    # TODO 2d: outliers por IQR en "Concentracion_PM25":
    #          q1, q3 = quantile(0.25), quantile(0.75); iqr = q3 - q1
    #          limites = q1 - FACTOR_IQR*iqr  y  q3 + FACTOR_IQR*iqr
    #          df.loc[fuera_de_limites, "Concentracion_PM25"] = np.nan

    # TODO 2e: imputacion k-NN sobre COLS_NUM:
    #          imp = KNNImputer(n_neighbors=K_VECINOS)
    #          df[COLS_NUM] = imp.fit_transform(df[COLS_NUM])
    #          (fit_transform devuelve un arreglo NumPy: hay que reasignarlo)
    return df


# ==========================================================================
# TAREA 3: EDA y multicolinealidad
# ==========================================================================
def tarea3(df: pd.DataFrame) -> None:
    # TODO 3a: imprimir media, mediana, std, skew() y kurt() de Concentracion_PM25
    #          (kurt() de pandas ya es exceso de curtosis: normal = 0)

    # TODO 3b: corr_p = df.corr(method="pearson", numeric_only=True)
    #          corr_s = df.corr(method="spearman", numeric_only=True)

    # TODO 3c: dibujar ambos con sns.heatmap en plt.subplots(1, 2) y guardar la
    #          captura (plt.savefig("correlaciones.png"))

    # TODO 3d: buscar pares con abs(r) >= UMBRAL_R (sin la diagonal ni repetidos)
    pass


if __name__ == "__main__":
    df_raw = pd.read_csv(CSV_CRUDO)
    df_t1 = tarea1(df_raw)
    df_clean = tarea2(df_t1)
    print("\nNaN restantes:\n", df_clean.isna().sum())
    df_clean.to_csv(CSV_LIMPIO, index=False)   # lo lee la app
    print("Guardado:", CSV_LIMPIO)
    tarea3(df_clean)
    plt.show()
