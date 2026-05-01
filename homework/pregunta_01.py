"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import os

import pandas as pd


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = pd.read_csv(
        "files/input/solicitudes_de_credito.csv",
        sep=";",
        index_col=0,
        dtype={"estrato": str},
    )

    # Drop rows with any NaN values
    df = df.dropna()

    # Normalize text columns: lowercase + strip whitespace
    text_cols = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "línea_credito"]
    for col in text_cols:
        df[col] = df[col].str.lower().str.strip()

    # Replace underscores and hyphens with spaces in idea_negocio and barrio
    for col in ["idea_negocio", "barrio"]:
        df[col] = df[col].str.replace("_", " ", regex=False)
        df[col] = df[col].str.replace("-", " ", regex=False)

    # Clean monto_del_credito: remove $, commas, spaces and trailing .00
    df["monto_del_credito"] = df["monto_del_credito"].astype(str).str.strip()
    df["monto_del_credito"] = df["monto_del_credito"].str.replace(r"[\$\s,]", "", regex=True)
    df["monto_del_credito"] = df["monto_del_credito"].str.replace(r"\.00$", "", regex=True)
    df["monto_del_credito"] = df["monto_del_credito"].astype(int)

    # Normalize fecha_de_beneficio to DD/MM/YYYY (handles DD/MM/YYYY and YYYY/MM/DD)
    df["fecha_de_beneficio"] = pd.to_datetime(df["fecha_de_beneficio"], dayfirst=True)
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].dt.strftime("%d/%m/%Y")

    # Strip whitespace from estrato (preserves "02" as distinct from "2")
    df["estrato"] = df["estrato"].str.strip()

    # Convert comuna_ciudadano float to int
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)

    # Remove duplicate rows
    df = df.drop_duplicates()

    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";")
