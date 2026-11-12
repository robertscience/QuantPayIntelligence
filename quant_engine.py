from decimal import Decimal, InvalidOperation


def analyze_dataset(data):
    """Genera un perfil cuantitativo de un DataFrame financiero."""
    import pandas as pd

    if data is None or data.empty:
        raise ValueError("No hay registros para analizar.")

    # Normalizar nombres para localizar las columnas requeridas.
    columns = {str(column).strip().lower(): column for column in data.columns}
    required = {"ingresos", "costos"}
    missing = required - set(columns)

    if missing:
        raise ValueError(
            "Faltan columnas requeridas: " + ", ".join(sorted(missing))
        )

    # Convertir a números y rechazar datos incompletos o inválidos.
    numeric = pd.DataFrame({
        "ingresos": pd.to_numeric(data[columns["ingresos"]], errors="coerce"),
        "costos": pd.to_numeric(data[columns["costos"]], errors="coerce"),
    })

    if numeric.isna().any().any():
        raise ValueError(
            "Ingresos y costos deben contener valores numéricos completos."
        )

    if not numeric.map(lambda value: __import__("math").isfinite(value)).all().all():
        raise ValueError("No se permiten valores infinitos.")

    if (numeric < 0).any().any():
        raise ValueError("Los ingresos y costos no pueden ser negativos.")

    numeric["utilidad"] = numeric["ingresos"] - numeric["costos"]
    total_revenue = float(numeric["ingresos"].sum())
    total_costs = float(numeric["costos"].sum())
    total_profit = total_revenue - total_costs

    import math
    if not all(math.isfinite(value) for value in (total_revenue, total_costs, total_profit)):
        raise ValueError("Los totales financieros exceden el rango numérico permitido.")

    if total_revenue <= 0:
        raise ValueError("Los ingresos totales deben ser mayores que cero.")

    # Concentración de ingresos en el 20 % de registros principales.
    top_count = max(1, int(len(numeric) * 0.20 + 0.999999))
    top_revenue = float(
        numeric.nlargest(top_count, "ingresos")["ingresos"].sum()
    )

    result = {
        "rows": int(len(numeric)),
        "financials": {
            "revenue": total_revenue,
            "costs": total_costs,
            "profit": total_profit,
            "margin_pct": total_profit / total_revenue * 100,
            "cost_ratio_pct": total_costs / total_revenue * 100,
        },
        "descriptive_statistics": {},
        "revenue_concentration": {
            "top_records": top_count,
            "top_records_pct": top_count / len(numeric) * 100,
            "revenue_share_pct": top_revenue / total_revenue * 100,
        },
        "outliers": {},
        "temporal_analysis": None,
        "limitations": [],
    }

    # Estadísticas descriptivas.
    for column in ("ingresos", "costos", "utilidad"):
        series = numeric[column]
        result["descriptive_statistics"][column] = {
            "mean": float(series.mean()),
            "median": float(series.median()),
            "min": float(series.min()),
            "max": float(series.max()),
            "std": float(series.std(ddof=1)) if len(series) > 1 else None,
        }

        # IQR: señal estadística, no prueba de fraude.
        if len(series) >= 4:
            q1 = float(series.quantile(0.25))
            q3 = float(series.quantile(0.75))
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            result["outliers"][column] = {
                "method": "IQR",
                "lower_bound": lower,
                "upper_bound": upper,
                "count": int(((series < lower) | (series > upper)).sum()),
                "indices": [
                    int(index) if isinstance(index, int) else str(index)
                    for index in series.index[
                        (series < lower) | (series > upper)
                    ]
                ],
            }
        else:
            result["outliers"][column] = {
                "method": "IQR",
                "count": None,
                "indices": [],
                "note": "Muestra insuficiente para una señal IQR útil.",
            }

    # Evolución por fecha, si el archivo contiene una columna adecuada.
    if "fecha" in columns:
        dates = pd.to_datetime(data[columns["fecha"]], errors="coerce")

        if dates.notna().all():
            temporal = numeric.copy()
            temporal["fecha"] = dates.dt.normalize()
            grouped = temporal.groupby("fecha", sort=True)[
                ["ingresos", "costos", "utilidad"]
            ].sum()

            result["temporal_analysis"] = [
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "revenue": float(row["ingresos"]),
                    "costs": float(row["costos"]),
                    "profit": float(row["utilidad"]),
                }
                for date, row in grouped.iterrows()
            ]

            if len(grouped) < 2:
                result["limitations"].append(
                    "Se requiere más de una fecha para comparar periodos."
                )
        else:
            result["limitations"].append(
                "La columna fecha contiene valores no interpretables."
            )
    else:
        result["limitations"].append(
            "Sin columna fecha no se puede analizar la evolución temporal."
        )

    if len(numeric) < 4:
        result["limitations"].append(
            "Muestra pequeña: los patrones y posibles anomalías son preliminares."
        )

    return result


def analyze_financials(revenue, costs, cost_increase_pct=0, revenue_change_pct=0):
    """Calcula métricas financieras y escenarios con precisión decimal."""
    try:
        revenue = Decimal(str(revenue))
        costs = Decimal(str(costs))
        cost_increase_pct = Decimal(str(cost_increase_pct))
        revenue_change_pct = Decimal(str(revenue_change_pct))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("Todos los valores deben ser números válidos.") from exc

    values = (revenue, costs, cost_increase_pct, revenue_change_pct)

    if not all(value.is_finite() for value in values):
        raise ValueError("No se permiten valores infinitos o no numéricos.")

    if revenue <= 0 or costs < 0:
        raise ValueError(
            "Los ingresos deben ser positivos y los costos no negativos."
        )

    if cost_increase_pct < -100 or revenue_change_pct < -100:
        raise ValueError(
            "Las variaciones porcentuales no pueden ser menores a -100%."
        )

    profit = revenue - costs
    adjusted_costs = costs * (1 + cost_increase_pct / 100)
    adjusted_revenue = revenue * (1 + revenue_change_pct / 100)

    return {
        "revenue": revenue,
        "costs": costs,
        "profit": profit,
        "margin_pct": profit / revenue * 100,
        "cost_ratio_pct": costs / revenue * 100,
        "profit_cost_scenario": revenue - adjusted_costs,
        "profit_revenue_scenario": adjusted_revenue - costs,
    }


def generate_ai_insights(analysis):
    """Genera insights explicables a partir del análisis cuantitativo local."""

    if not isinstance(analysis, dict):
        raise ValueError("El análisis cuantitativo debe ser un diccionario.")

    financials = analysis.get("financials", {})
    concentration = analysis.get("revenue_concentration", {})
    outliers = analysis.get("outliers", {})
    limitations = analysis.get("limitations", [])

    profit = float(financials.get("profit", 0))
    margin_pct = float(financials.get("margin_pct", 0))
    cost_ratio_pct = float(financials.get("cost_ratio_pct", 0))
    revenue_share_pct = float(
        concentration.get("revenue_share_pct", 0)
    )

    insights = []

    if profit < 0:
        insights.append({
            "type": "critical",
            "title": "Pérdida operativa",
            "message": (
                "Los costos superan los ingresos en el conjunto analizado."
            ),
        })
    elif profit == 0:
        insights.append({
            "type": "warning",
            "title": "Punto de equilibrio",
            "message": (
                "Los ingresos cubren exactamente los costos del conjunto analizado."
            ),
        })
    else:
        insights.append({
            "type": "positive",
            "title": "Rentabilidad positiva",
            "message": (
                "El conjunto analizado presenta utilidad positiva."
            ),
        })

    if margin_pct < 10:
        insights.append({
            "type": "warning",
            "title": "Margen reducido",
            "message": (
                f"El margen de utilidad es de {margin_pct:.2f}%, "
                "lo que deja poco espacio ante variaciones de costos o ingresos."
            ),
        })
    elif margin_pct >= 30:
        insights.append({
            "type": "positive",
            "title": "Margen elevado",
            "message": (
                f"El margen de utilidad alcanza {margin_pct:.2f}%."
            ),
        })

    if cost_ratio_pct >= 90:
        insights.append({
            "type": "warning",
            "title": "Alta proporción de costos",
            "message": (
                f"Los costos representan {cost_ratio_pct:.2f}% de los ingresos."
            ),
        })

    if revenue_share_pct >= 50:
        insights.append({
            "type": "warning",
            "title": "Concentración de ingresos",
            "message": (
                f"El 20% superior de los registros concentra "
                f"{revenue_share_pct:.2f}% de los ingresos."
            ),
        })

    outlier_count = 0

    for details in outliers.values():
        if isinstance(details, dict):
            count = details.get("count")
            if isinstance(count, (int, float)) and count > 0:
                outlier_count += int(count)

    if outlier_count > 0:
        insights.append({
            "type": "review",
            "title": "Valores atípicos detectados",
            "message": (
                f"Se detectaron {outlier_count} valores atípicos mediante IQR. "
                "Esto es una señal estadística para revisión y no una prueba de fraude."
            ),
        })

    return {
        "engine": "QuantPay Explainable Insights",
        "version": "1.0",
        "source": "quantitative_analysis",
        "insights_count": len(insights),
        "insights": insights,
        "limitations": limitations,
    }
