"""
Índice de Atractividad Regional de España (IAR)
================================================
Caso de principio a fin: lectura -> limpieza -> cálculo -> visualización.

Pregunta de negocio
-------------------
Una empresa quiere abrir una nueva sede u operación en España.
¿Qué comunidad autónoma ofrece la mejor combinación de MERCADO, EMPLEO y COSTE?

Método
------
1. Se parte de 4 indicadores públicos del INE (una fila por CCAA).
2. Cada indicador se normaliza a una escala 0-100 (min-max) para poder
   sumar "peras con manzanas". Dos indicadores "cuanto menos mejor"
   (paro y coste laboral) se invierten al normalizar.
3. El Índice de Atractividad Regional (IAR) es la media ponderada de las
   4 dimensiones. Se calcula un escenario EQUILIBRADO (pesos iguales) y
   dos escenarios de estrategia para un análisis de sensibilidad.

Autor: Vicente Marco Pastor
Datos: INE (ver README y memo para fuentes y años de referencia).
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- Rutas ---------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "indicadores_ccaa.csv"
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

# --- Estilo de gráficos (sobrio y legible) -------------------------------
AZUL = "#2F5C8A"       # color principal
GRIS = "#B9C2CC"       # barras secundarias
ROJO = "#C04A3B"       # para destacar
plt.rcParams.update({
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "figure.dpi": 110,
})

# =========================================================================
# 1. LECTURA
# =========================================================================
df = pd.read_csv(DATA)
print("Filas leídas:", len(df))
print(df.head(3), "\n")

# =========================================================================
# 2. LIMPIEZA / CONTROL DE CALIDAD
# =========================================================================
# Comprobamos que no falten datos y que los tipos sean numéricos.
assert df["comunidad"].is_unique, "Hay comunidades duplicadas"
assert df.isnull().sum().sum() == 0, "Hay valores vacíos en el dataset"

# Control de coherencia: la media de paro ponderada por población debe
# parecerse a la tasa nacional publicada por el INE (~9,87% en 2T 2026).
paro_nacional = (df["tasa_paro_2t2026"] * df["poblacion_2025"]).sum() / df["poblacion_2025"].sum()
print(f"Paro medio ponderado por población: {paro_nacional:.2f}%  (INE nacional 2T26: 9,87%)\n")

# =========================================================================
# 3. NORMALIZACIÓN (min-max a escala 0-100)
# =========================================================================
def normaliza(serie, mas_es_mejor=True):
    """Lleva una serie a 0-100. Si 'mas_es_mejor' es False, invierte."""
    lo, hi = serie.min(), serie.max()
    base = (serie - lo) / (hi - lo) * 100
    return base if mas_es_mejor else 100 - base

df["s_riqueza"] = normaliza(df["pib_per_capita_2024"], mas_es_mejor=True)   # PIB pc: + mejor
df["s_empleo"]  = normaliza(df["tasa_paro_2t2026"],    mas_es_mejor=False)  # paro:  - mejor
df["s_mercado"] = normaliza(df["poblacion_2025"],      mas_es_mejor=True)   # tamaño: + mejor
df["s_coste"]   = normaliza(df["coste_laboral_2024"],  mas_es_mejor=False)  # coste: - mejor

DIMS = ["s_riqueza", "s_empleo", "s_mercado", "s_coste"]
ETIQ = {"s_riqueza": "Riqueza de mercado\n(PIB per cápita)",
        "s_empleo":  "Salud laboral\n(tasa de paro)",
        "s_mercado": "Tamaño de mercado\n(población)",
        "s_coste":   "Coste laboral\n(€/trabajador)"}

# =========================================================================
# 4. ÍNDICE COMPUESTO Y ESCENARIOS (análisis de sensibilidad)
# =========================================================================
escenarios = {
    # (riqueza, empleo, mercado, coste)  -- suman 1
    "Equilibrado":         (0.25, 0.25, 0.25, 0.25),
    "Orientado a mercado": (0.35, 0.15, 0.35, 0.15),  # abrir sede comercial
    "Orientado a coste":   (0.15, 0.15, 0.30, 0.40),  # back-office / centro de servicios
}

for nombre, pesos in escenarios.items():
    df[f"IAR_{nombre}"] = sum(p * df[d] for p, d in zip(pesos, DIMS))

df["IAR"] = df["IAR_Equilibrado"]
df = df.sort_values("IAR", ascending=False).reset_index(drop=True)
df.index = df.index + 1  # ranking desde 1

# --- Tabla de resultados -------------------------------------------------
cols_out = ["comunidad", "s_riqueza", "s_empleo", "s_mercado", "s_coste",
            "IAR_Equilibrado", "IAR_Orientado a mercado", "IAR_Orientado a coste"]
tabla = df[cols_out].round(1)
tabla.to_csv(OUT / "ranking_iar.csv", index_label="ranking")
print("RANKING (escenario equilibrado):")
print(tabla[["comunidad", "IAR_Equilibrado"]].to_string(), "\n")

# =========================================================================
# 5. VISUALIZACIÓN
# =========================================================================

# 5.1 Ranking base (barras horizontales)
fig, ax = plt.subplots(figsize=(8, 6))
orden = df.sort_values("IAR_Equilibrado")
colores = [ROJO if c in (orden["comunidad"].iloc[-1], orden["comunidad"].iloc[-2]) else AZUL
           for c in orden["comunidad"]]
ax.barh(orden["comunidad"], orden["IAR_Equilibrado"], color=colores)
ax.set_xlabel("Índice de Atractividad Regional (0-100)")
ax.set_title("Ranking de atractividad regional · escenario equilibrado",
             fontweight="bold", loc="left")
for y, v in enumerate(orden["IAR_Equilibrado"]):
    ax.text(v + 0.6, y, f"{v:.1f}", va="center", fontsize=9)
ax.margins(x=0.12)
fig.tight_layout()
fig.savefig(OUT / "ranking_base.png", bbox_inches="tight")
plt.close(fig)

# 5.2 Heatmap de dimensiones (top = más atractivo)
fig, ax = plt.subplots(figsize=(8, 7))
mat = df.set_index("comunidad")[DIMS]
im = ax.imshow(mat.values, aspect="auto", cmap="YlGnBu", vmin=0, vmax=100)
ax.set_xticks(range(len(DIMS)))
ax.set_xticklabels([ETIQ[d] for d in DIMS], fontsize=9)
ax.set_yticks(range(len(mat)))
ax.set_yticklabels(mat.index, fontsize=9)
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        val = mat.values[i, j]
        ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                color="white" if val > 55 else "black", fontsize=8)
ax.set_title("Perfil por dimensiones (0 = peor, 100 = mejor)",
             fontweight="bold", loc="left")
fig.colorbar(im, ax=ax, shrink=0.6, label="puntuación")
fig.tight_layout()
fig.savefig(OUT / "heatmap_dimensiones.png", bbox_inches="tight")
plt.close(fig)

# 5.3 Dispersión mercado vs coste (la tensión clave)
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(df["coste_laboral_2024"], df["pib_per_capita_2024"],
           s=df["poblacion_2025"] / 9000, color=AZUL, alpha=0.65, edgecolor="white")
ax.axhline(df["pib_per_capita_2024"].mean(), color=GRIS, ls="--", lw=1)
ax.axvline(df["coste_laboral_2024"].mean(), color=GRIS, ls="--", lw=1)
for _, r in df.iterrows():
    ax.annotate(r["comunidad"], (r["coste_laboral_2024"], r["pib_per_capita_2024"]),
                fontsize=7.5, xytext=(4, 4), textcoords="offset points")
ax.set_xlabel("Coste laboral (€/trabajador y mes, 2024)")
ax.set_ylabel("PIB per cápita (€, 2024)")
ax.set_title("Mercado vs. coste · el tamaño del círculo = población",
             fontweight="bold", loc="left")
fig.tight_layout()
fig.savefig(OUT / "dispersion_mercado_coste.png", bbox_inches="tight")
plt.close(fig)

# 5.4 Sensibilidad: cómo cambia la puntuación según la estrategia
# Mostramos las comunidades que entran en el Top-4 de algún escenario.
top_por_esc = set()
for nombre in escenarios:
    top_por_esc.update(df.nlargest(4, f"IAR_{nombre}")["comunidad"])
sel = df[df["comunidad"].isin(top_por_esc)].sort_values("IAR_Equilibrado")

import numpy as np
y = np.arange(len(sel))
h = 0.26
colores_esc = {"Equilibrado": AZUL, "Orientado a mercado": ROJO, "Orientado a coste": "#4C9A6B"}
fig, ax = plt.subplots(figsize=(9, 6))
for k, nombre in enumerate(escenarios):
    ax.barh(y + (k - 1) * h, sel[f"IAR_{nombre}"], height=h,
            color=colores_esc[nombre], label=nombre)
ax.set_yticks(y)
ax.set_yticklabels(sel["comunidad"])
ax.set_xlabel("Índice de Atractividad Regional (0-100)")
ax.set_title("Análisis de sensibilidad · el 'mejor sitio' depende de la estrategia",
             fontweight="bold", loc="left")
ax.legend(title="Escenario", loc="upper left", bbox_to_anchor=(1.01, 1))
fig.tight_layout()
fig.savefig(OUT / "sensibilidad_escenarios.png", bbox_inches="tight")
plt.close(fig)

# --- Top-3 por escenario para el memo ------------------------------------
print("TOP-3 POR ESCENARIO:")
for nombre in escenarios:
    top3 = df.nlargest(3, f"IAR_{nombre}")[["comunidad", f"IAR_{nombre}"]]
    ranked = ", ".join(f"{c} ({v:.1f})" for c, v in
                       zip(top3["comunidad"], top3[f"IAR_{nombre}"]))
    print(f"  {nombre:22s}: {ranked}")

print("\nGráficos y ranking_iar.csv guardados en:", OUT)
