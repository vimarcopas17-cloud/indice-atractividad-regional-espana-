# Índice de Atractividad Regional de España 🇪🇸

*🌐 [English version](README.en.md)*

**¿En qué comunidad autónoma debería una empresa abrir su próxima sede u operación?**
Un caso de análisis de datos de principio a fin que convierte 4 indicadores públicos
del INE en una recomendación de negocio clara y defendible.

## Qué resuelve

Comparar 17 comunidades autónomas es difícil porque cada una gana en algo distinto:
Madrid tiene el mercado más rico pero el coste más alto, el sur es barato pero con más
paro. Este proyecto construye un **índice compuesto (0–100)** que combina cuatro
dimensiones —**riqueza de mercado, salud laboral, tamaño de mercado y coste laboral**—
para poder rankearlas de forma objetiva y transparente.

## Resultado principal

- 🥇 **Apuesta más robusta: Cataluña** — única región en el Top-2 de los tres escenarios
  de estrategia analizados (mercado grande, paro bajo y coste inferior al de Madrid).
- 🏙️ **Si prima el mercado (sede comercial): Madrid.**
- 💶 **Si prima el coste (back-office / centro de servicios): Andalucía.**

La conclusión clave es metodológica: **"el mejor sitio" depende de la estrategia**, y el
análisis de sensibilidad lo demuestra en vez de esconderlo.

## Cómo está hecho

`lectura → limpieza y control de calidad → normalización 0-100 → índice ponderado →
análisis de sensibilidad → visualización`. Todo en **Python (pandas + matplotlib)**.
Control de calidad incluido: el paro medio ponderado por población da **9,89 %** frente
al **9,87 %** oficial del INE.

## Estructura

```
data/     indicadores_ccaa.csv     · dataset (datos reales del INE)
notebooks/analisis_atractividad.ipynb · análisis completo con narrativa y gráficos
src/      analisis.py              · versión script reproducible
output/   ranking + 4 gráficos     · resultados exportados
memo/     memo_ejecutivo.md        · entregable tipo consultoría (1 página)
```

## Reproducir

```bash
pip install -r requirements.txt
python src/analisis.py          # genera ranking y gráficos en output/
# o abrir notebooks/analisis_atractividad.ipynb
```

## Fuentes (INE)

PIB per cápita 2024 (Contabilidad Regional), tasa de paro 2T 2026 (EPA), población a
1-ene-2025 (Estadística Continua de Población) y coste laboral 2024 (Encuesta de Coste
Laboral). Detalle y limitaciones en [`memo/memo_ejecutivo.md`](memo/memo_ejecutivo.md).

---
*Proyecto personal de análisis de datos · Vicente Marco Pastor*
