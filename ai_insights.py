import os
from google import genai


MODEL_NAME = "gemini-3.6-flash"


def generate_ai_insights(financial_metrics):
    """
    Genera insights sobre un escenario financiero simulado.
    No modifica datos, pagos ni operaciones del sistema.
    """
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return {
            "ok": False,
            "insight": "AI Insights no estÃ¡ disponible: falta configurar la API.",
        }

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
Eres un analista financiero de RobertScience QuantPay Intelligence.

Analiza exclusivamente este escenario financiero SIMULADO:
- Ingresos: {financial_metrics["revenue"]}
- Costos: {financial_metrics["costs"]}
- Utilidad estimada: {financial_metrics["profit"]}
- Margen operativo: {financial_metrics["margin"]}%
- Utilidad con costos 5% mayores: {financial_metrics["costs_up_5"]}
- Utilidad con ingresos 5% menores: {financial_metrics["revenue_down_5"]}

Devuelve en espaÃ±ol:
1. Un insight ejecutivo breve.
2. Dos observaciones cuantitativas.
3. Una recomendaciÃ³n de anÃ¡lisis que se pueda evaluar.

No inventes datos ni afirmes que son transacciones reales.
No ejecutes operaciones ni recomiendes comprar o vender activos.
Aclara que las conclusiones se basan en un escenario simulado.
MÃ¡ximo 150 palabras.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={"http_options": {"timeout": 60000}},
        )

        insight = (response.text or "").strip()

        if not insight:
            return {
                "ok": False,
                "insight": "Gemini no devolviÃ³ contenido. Intenta nuevamente.",
            }

        return {"ok": True, "insight": insight}

    except Exception as exc:
        return {
            "ok": False,
            "insight": f"Error de Gemini: {type(exc).__name__}",
        }

def generate_uploaded_data_insights(quantitative_analysis):
    """
    Genera una propuesta cuantitativa basada en métricas calculadas
    localmente a partir de un archivo del cliente.
    """
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return {
            "ok": False,
            "insight": "AI Insights no disponible: falta configurar la API.",
        }

    if not isinstance(quantitative_analysis, dict):
        return {
            "ok": False,
            "insight": "El análisis recibido no tiene un formato válido.",
        }

    try:
        import json

        payload = json.dumps(
            quantitative_analysis,
            ensure_ascii=False,
            allow_nan=False,
        )

        prompt = f"""
Eres el analista cuantitativo de RobertScience QuantPay Intelligence.

Analiza las métricas calculadas localmente a partir de un archivo
proporcionado por un cliente. Los datos de entrada son:

{payload}

Responde en español con:
1. Un diagnóstico ejecutivo breve.
2. Hasta tres hallazgos respaldados por las métricas.
3. Una propuesta cuantitativa que pueda evaluarse.
4. Las limitaciones relevantes del análisis.

Reglas:
- Basa cada afirmación en los datos recibidos.
- No inventes cifras, columnas, causas ni tendencias.
- Distingue hechos calculados de hipótesis por comprobar.
- Si faltan datos temporales, no afirmes tendencias en el tiempo.
- Los valores atípicos son señales estadísticas, no pruebas de fraude.
- No ejecutes operaciones ni recomiendes comprar o vender activos.
- Aclara que la propuesta requiere validación humana.
- Máximo 200 palabras.
"""

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={"http_options": {"timeout": 60000}},
        )

        insight = (response.text or "").strip()

        if not insight:
            return {
                "ok": False,
                "insight": "Gemini no devolvió contenido.",
            }

        return {"ok": True, "insight": insight}

    except Exception as exc:
        return {
            "ok": False,
            "insight": f"Error de Gemini: {type(exc).__name__}",
        }

