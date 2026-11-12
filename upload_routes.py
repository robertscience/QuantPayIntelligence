
from flask import Blueprint, request
from decimal import Decimal, InvalidOperation
from pathlib import Path
import data_engine
import quant_engine
import ai_insights as ai_insights_module

upload_api = Blueprint("upload_api", __name__)


@upload_api.route("/api/data/upload", methods=["POST"])
def upload_data_file():
    if "file" not in request.files:
        return {"error": "Adjunta un archivo en el campo 'file'."}, 400

    uploaded = request.files["file"]
    if not uploaded.filename:
        return {"error": "Selecciona un archivo CSV o XLSX."}, 400

    import hashlib

    content = uploaded.stream.read(data_engine.MAX_FILE_BYTES + 1)
    if len(content) > data_engine.MAX_FILE_BYTES:
        return {"error": "El archivo supera el límite permitido."}, 400

    sha256_hash = hashlib.sha256(content).hexdigest()
    uploaded.stream.seek(0)

    extension = Path(uploaded.filename).suffix.lower()
    if extension in {".jpg", ".jpeg", ".png"}:
        from io import BytesIO
        from PIL import Image, UnidentifiedImageError

        try:
            content = uploaded.stream.read(data_engine.MAX_FILE_BYTES + 1)
            if not content:
                return {"error": "La imagen est? vac?a."}, 400
            if len(content) > data_engine.MAX_FILE_BYTES:
                return {"error": "La imagen supera el l?mite de 10 MB."}, 400
            with Image.open(BytesIO(content)) as image:
                if image.format not in {"JPEG", "PNG"}:
                    return {"error": "El contenido no es una imagen JPEG o PNG v?lida."}, 400
                image.verify()
        except (UnidentifiedImageError, OSError):
            return {"error": "La imagen est? da?ada o no es v?lida."}, 400

        return {
            "filename": uploaded.filename,
            "status": "image_validated",
            "note": "Imagen validada. La extracci?n de texto OCR y el an?lisis financiero a?n no est?n disponibles."
        }, 200

    try:
        data = data_engine.load_financial_file(
            uploaded.stream, uploaded.filename
        )

        columns = {
            str(column).strip().lower(): column
            for column in data.columns
        }
        required = {"ingresos", "costos"}
        missing = required - set(columns)

        if missing:
            raise ValueError(
                "Faltan columnas requeridas: "
                + ", ".join(sorted(missing))
                + ". Se requieren ingresos y costos."
            )

        try:
            revenues = [
                Decimal(str(value))
                for value in data[columns["ingresos"]]
            ]
            costs = [
                Decimal(str(value))
                for value in data[columns["costos"]]
            ]
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError(
                "Las columnas ingresos y costos deben contener números."
            ) from exc

        if not all(value.is_finite() for value in revenues + costs):
            raise ValueError(
                "No se permiten valores infinitos o no numéricos."
            )

        if any(value < 0 for value in revenues + costs):
            raise ValueError(
                "Los ingresos y costos no pueden ser negativos."
            )

        total_revenue = sum(revenues, Decimal("0"))
        total_costs = sum(costs, Decimal("0"))

        if total_revenue <= 0:
            raise ValueError(
                "La suma de ingresos debe ser mayor que cero."
            )

        metrics = quant_engine.analyze_financials(
    total_revenue,
    total_costs,
    cost_increase_pct=5,
    revenue_change_pct=-5,
)

                # Perfil cuantitativo calculado localmente.
        quantitative_analysis = quant_engine.analyze_dataset(data)

        # Insights explicables calculados localmente.
        ai_insights = quant_engine.generate_ai_insights(
            quantitative_analysis
        )

        # Propuesta de Gemini basada en métricas del archivo cargado.
        ai_proposal = ai_insights_module.generate_uploaded_data_insights(
            quantitative_analysis
        )

    except ValueError as exc:
        return {"error": str(exc)}, 400

    return {
            "filename": uploaded.filename,
            "rows": int(len(data)),
            "columns": [str(column) for column in data.columns],
                        "status": "analyzed",
            "evidence": {
                "algorithm": "SHA-256",
                "sha256": sha256_hash,
            },
            "financial_analysis": {
                "revenue": str(metrics["revenue"]),
                "costs": str(metrics["costs"]),
                "profit": str(metrics["profit"]),
                "margin_pct": str(
                    metrics["margin_pct"].quantize(Decimal("0.01"))
                ),
                "cost_ratio_pct": str(
                    metrics["cost_ratio_pct"].quantize(Decimal("0.01"))
                ),
                "profit_cost_scenario": str(
                    metrics["profit_cost_scenario"]
                ),
                "profit_revenue_scenario": str(
                    metrics["profit_revenue_scenario"]
                ),
            },
            "quantitative_analysis": quantitative_analysis,
            "ai_insights": ai_insights,
            "ai_proposal": ai_proposal,
            "note": (
                "Archivo analizado en memoria; no se guardó "
                "ni se mezcló con PayPal."
                        ),
    }