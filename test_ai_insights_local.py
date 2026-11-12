
import os
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import ai_insights


class TestAIInsightsLocal(unittest.TestCase):

    def setUp(self):
        self.key_patch = patch.dict(
            os.environ,
            {"GEMINI_API_KEY": "local-test-key"},
        )
        self.key_patch.start()
        self.addCleanup(self.key_patch.stop)

        self.response = SimpleNamespace(text="Prueba simulada correcta")

        self.models = SimpleNamespace(
            generate_content=self.fake_generate_content
        )

        self.client = SimpleNamespace(models=self.models)

        self.client_patch = patch(
            "ai_insights.genai.Client",
            return_value=self.client,
        )
        self.client_patch.start()
        self.addCleanup(self.client_patch.stop)

    def fake_generate_content(self, **kwargs):
        self.assertIn("model", kwargs)
        self.assertIn("contents", kwargs)
        self.assertIn("config", kwargs)
        return self.response

    def test_financial_insights(self):
        metrics = {
            "revenue": "100000",
            "costs": "72000",
            "profit": "28000",
            "margin": "28",
            "costs_up_5": "24400",
            "revenue_down_5": "23000",
        }

        result = ai_insights.generate_ai_insights(metrics)

        self.assertTrue(result["ok"], result)
        self.assertEqual(
            result["insight"],
            "Prueba simulada correcta",
        )

    def test_uploaded_data_insights(self):
        metrics = {
            "rows": 3,
            "total": 844.5,
        }

        result = ai_insights.generate_uploaded_data_insights(metrics)

        self.assertTrue(result["ok"], result)
        self.assertEqual(
            result["insight"],
            "Prueba simulada correcta",
        )

class TestUploadRoute(unittest.TestCase):

    def setUp(self):
        import io
        import app
        import upload_routes

        self.io = io
        self.client = app.app.test_client()

        self.gemini_patch = patch(
            "upload_routes.ai_insights_module.generate_uploaded_data_insights",
            return_value={
                "ok": True,
                "insight": "Propuesta simulada sin llamada externa",
            },
        )
        self.gemini_patch.start()
        self.addCleanup(self.gemini_patch.stop)

    def upload_csv(self, content, filename="test.csv"):
        return self.client.post(
            "/api/data/upload",
            data={
                "file": (
                    self.io.BytesIO(content),
                    filename,
                ),
            },
            content_type="multipart/form-data",
        )

    def test_valid_csv_returns_financial_scenarios(self):
        response = self.upload_csv(
            b"ingresos,costos\n100,60\n200,120\n300,180\n400,200\n"
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()

        import hashlib

        expected_hash = hashlib.sha256(
            b"ingresos,costos\n100,60\n200,120\n300,180\n400,200\n"
        ).hexdigest()

        self.assertEqual(result["evidence"]["algorithm"], "SHA-256")
        self.assertEqual(result["evidence"]["sha256"], expected_hash)

        self.assertEqual(result["status"], "analyzed")
        self.assertEqual(result["financial_analysis"]["revenue"], "1000")
        self.assertEqual(result["financial_analysis"]["costs"], "560")
        self.assertEqual(result["financial_analysis"]["profit"], "440")
        self.assertEqual(
            result["financial_analysis"]["profit_cost_scenario"],
            "412.00",
        )
        self.assertEqual(
            result["financial_analysis"]["profit_revenue_scenario"],
            "390.00",
        )
        self.assertTrue(result["ai_proposal"]["ok"])
        response.close()

    def test_invalid_numeric_data_returns_400(self):
        response = self.upload_csv(
            b"ingresos,costos\n100,60\nabc,20\n",
            "invalid.csv",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("números", response.get_json()["error"])

    def test_oversized_file_returns_413(self):
        import io
        import app

        response = self.client.post(
            "/api/data/upload",
            data={
                "file": (
                    io.BytesIO(
                        b"x" * (app.app.config["MAX_CONTENT_LENGTH"] + 1)
                    ),
                    "oversized.csv",
                ),
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 413)

    def test_missing_file_returns_400(self):
        response = self.client.post("/api/data/upload")

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Adjunta un archivo",
            response.get_json()["error"],
        )

    def test_gemini_is_mocked(self):
        response = self.upload_csv(
            b"ingresos,costos\n100,60\n200,120\n300,180\n400,200\n"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["ai_proposal"]["insight"],
            "Propuesta simulada sin llamada externa",
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
