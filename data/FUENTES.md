# Fuentes de los datos

Todos los datos proceden del **Instituto Nacional de Estadística (INE)**. Se documenta
cada indicador con su operación estadística, periodo de referencia y valor nacional de
control.

| Columna | Indicador | Operación INE | Periodo | Control nacional |
|---|---|---|---|---|
| `pib_per_capita_2024` | PIB per cápita (€/hab.) | Contabilidad Regional de España (avance) | 2024 | Media España: 32.633 € |
| `tasa_paro_2t2026` | Tasa de paro (%) | Encuesta de Población Activa (EPA) | 2º trim. 2026 | España: 9,87 % |
| `poblacion_2025` | Población (habitantes) | Estadística Continua de Población (ECP) | 1 enero 2025 | España: 49.077.984 hab. |
| `coste_laboral_2024` | Coste laboral (€/trabajador y mes) | Encuesta de Coste Laboral | 2024 | Media España: 3.258,14 € |

## Notas

- El análisis cubre las **17 comunidades autónomas**. Ceuta y Melilla se excluyen porque
  la Encuesta de Coste Laboral no publica su coste laboral y por su tamaño atípico.
- Se combinan indicadores anuales (PIB, coste, población) con uno trimestral (paro). Es
  una foto de situación reciente, no una serie temporal; para un uso operativo conviene
  fijar todos los indicadores al mismo año de cierre.
- Verificación: el paro medio ponderado por población de las 17 CCAA reproduce la tasa
  nacional del INE con una diferencia de 0,02 puntos, lo que valida la transcripción.

*Consulta oficial: [www.ine.es](https://www.ine.es).*
