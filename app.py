from flask import Flask, render_template_string, request
from decimal import Decimal
import quant_engine
import data_engine
import os
import json
import urllib.request
import urllib.error
import base64
from ai_insights import generate_ai_insights

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = data_engine.MAX_FILE_BYTES
from upload_routes import upload_api
app.register_blueprint(upload_api)

def paypal_access_token():
    client_id = os.environ.get("PAYPAL_CLIENT_ID")
    client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Faltan las credenciales de PayPal Sandbox en las variables de entorno.")

    credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode("utf-8")
    ).decode("ascii")
    request = urllib.request.Request(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        data=b"grant_type=client_credentials",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    token = payload.get("access_token")
    if not token:
        raise RuntimeError("PayPal no devolvió un token de acceso.")
    return token

def paypal_create_order():
    token = paypal_access_token()
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {"currency_code": "USD", "value": "1.00"},
            "description": "QuantPay Intelligence Sandbox Demo"
        }]
    }
    request = urllib.request.Request(
        "https://api-m.sandbox.paypal.com/v2/checkout/orders",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        order = json.loads(response.read().decode("utf-8"))
    approval = next(
        (link["href"] for link in order.get("links", [])
         if link.get("rel") == "approve"),
        None
    )
    return {
        "id": order.get("id"),
        "status": order.get("status"),
        "approval_url": approval,
    }

def paypal_get_order(order_id):
    token = paypal_access_token()
    request = urllib.request.Request(
        f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def paypal_capture_order(order_id):
    token = paypal_access_token()
    request = urllib.request.Request(
        f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture",
        data=b"{}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


HTML = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#101112">
    <title>QuantPay Intelligence | RobertScience</title>

    <style>
        :root {
            --bg: #101112;
            --panel: #191a1c;
            --panel-soft: #202123;
            --line: #303033;
            --gold: #C8A24C;
            --text: #F2F0EA;
            --muted: #96969B;
            --green: #8BBE9B;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            background: var(--bg);
            color: var(--text);
            font-family: "Segoe UI", Arial, sans-serif;
        }

        .app {
            display: flex;
            min-height: 100vh;
        }

        .sidebar {
            width: 245px;
            flex-shrink: 0;
            padding: 28px 18px;
            background: #141516;
            border-right: 1px solid var(--line);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 42px;
        }

        .brand-mark {
            display: grid;
            place-items: center;
            width: 42px;
            height: 42px;
            border: 1px solid var(--gold);
            border-radius: 12px;
            color: var(--gold);
            font-size: 22px;
        }

        .brand-name {
            font-size: 15px;
            font-weight: 650;
            letter-spacing: 1.3px;
        }

        .brand-sub {
            margin-top: 5px;
            color: var(--muted);
            font-size: 10px;
            letter-spacing: 1.5px;
        }

        .nav-label {
            margin: 0 10px 13px;
            color: #77777C;
            font-size: 10px;
            letter-spacing: 1.8px;
        }

        .nav-item {
            margin-bottom: 6px;
            padding: 12px 13px;
            border-radius: 8px;
            color: #B9B9BC;
            font-size: 13px;
        }

        .nav-item.active {
            border: 1px solid #514326;
            background: #30291C;
            color: var(--gold);
        }

        .sidebar-bottom {
            margin-top: 50px;
            padding: 15px 12px;
            border: 1px solid var(--line);
            border-radius: 10px;
            color: var(--muted);
            font-size: 11px;
            line-height: 1.7;
        }

        .sidebar-bottom strong {
            color: var(--gold);
            font-weight: 500;
        }

        main {
            flex: 1;
            min-width: 0;
            padding: 30px 34px 40px;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            margin-bottom: 38px;
        }

        .eyebrow {
            color: var(--gold);
            font-size: 10px;
            letter-spacing: 2px;
        }

        h1 {
            margin: 10px 0;
            font-size: clamp(24px, 3vw, 34px);
            font-weight: 550;
            letter-spacing: -1px;
        }

        .subtitle {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .status {
            padding: 8px 11px;
            border: 1px solid #62502D;
            border-radius: 5px;
            background: #282216;
            color: var(--gold);
            font-size: 10px;
            letter-spacing: 1px;
            white-space: nowrap;
        }

        .section-heading {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin-bottom: 15px;
        }

        h2 {
            margin: 0;
            font-size: 14px;
            font-weight: 550;
        }

        .small {
            color: var(--muted);
            font-size: 11px;
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
            margin-bottom: 30px;
        }

        .metric {
            min-width: 0;
            padding: 19px 17px;
            border: 1px solid var(--line);
            border-radius: 11px;
            background: var(--panel);
        }

        .metric-label {
            margin-bottom: 17px;
            color: var(--muted);
            font-size: 11px;
            line-height: 1.5;
        }

        .metric-value {
            overflow-wrap: anywhere;
            font-size: clamp(20px, 2vw, 28px);
            font-weight: 550;
            letter-spacing: -.6px;
        }

        .metric-note {
            margin-top: 11px;
            color: var(--muted);
            font-size: 10px;
            line-height: 1.5;
        }

        .metric-note.gold {
            color: var(--gold);
        }

        .main-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.55fr) minmax(260px, 1fr);
            gap: 17px;
        }

        .panel {
            min-width: 0;
            border: 1px solid var(--line);
            border-radius: 11px;
            background: var(--panel);
        }

        .panel-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            padding: 19px 20px;
            border-bottom: 1px solid var(--line);
        }

        .panel-body {
            padding: 20px;
        }

        .chart {
            display: flex;
            align-items: end;
            gap: 12px;
            height: 190px;
            padding: 10px 4px 0;
        }

        .bar-wrap {
            display: flex;
            flex: 1;
            flex-direction: column;
            justify-content: end;
            align-items: center;
            gap: 10px;
            height: 100%;
        }

        .bar {
            width: min(100%, 34px);
            min-height: 8px;
            border-radius: 4px 4px 0 0;
            background: #69552D;
        }

        .bar.highlight {
            background: var(--gold);
        }

        .bar-label {
            color: var(--muted);
            font-size: 10px;
        }

        .chart-foot {
            margin-top: 12px;
            padding-top: 14px;
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: 10px;
            line-height: 1.6;
        }

        .insight {
            margin-bottom: 16px;
            padding: 15px;
            border: 1px solid #4A3D24;
            border-radius: 8px;
            background: #242117;
        }

        .insight-label {
            margin-bottom: 9px;
            color: var(--gold);
            font-size: 10px;
            letter-spacing: 1.2px;
        }

        .insight p {
            margin: 0;
            color: #D5D0C4;
            font-size: 12px;
            line-height: 1.8;
        }

        .workflow {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 7px;
            margin-top: 18px;
        }

        .step {
            padding: 8px 9px;
            border: 1px solid var(--line);
            border-radius: 5px;
            color: #D0CFCA;
            font-size: 10px;
        }

        .arrow {
            color: var(--gold);
            font-size: 12px;
        }

        .table-panel {
            margin-top: 18px;
        }

        .table-wrap {
            overflow-x: auto;
        }

        table {
            width: 100%;
            min-width: 450px;
            border-collapse: collapse;
        }

        th,
        td {
            padding: 14px 19px;
            border-bottom: 1px solid var(--line);
            text-align: left;
            font-size: 11px;
        }

        th {
            color: var(--muted);
            font-weight: 450;
        }

        td {
            color: #D8D7D2;
        }

        td.muted {
            color: var(--muted);
        }

        .pill {
            display: inline-block;
            padding: 5px 7px;
            border: 1px solid #385343;
            border-radius: 4px;
            color: var(--green);
            font-size: 10px;
        }

        .demo-note {
            margin-top: 22px;
            color: #77777C;
            font-size: 10px;
            line-height: 1.8;
        }

        @media (max-width: 1050px) {
            .sidebar {
                width: 205px;
            }

            main {
                padding: 25px 22px;
            }

            .metrics {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 650px) {
            .app {
                display: block;
            }

            .sidebar {
                width: 100%;
                padding: 16px;
                border-right: 0;
                border-bottom: 1px solid var(--line);
            }

            .brand {
                margin-bottom: 18px;
            }

            .nav-label,
            .nav-item:not(.active),
            .sidebar-bottom {
                display: none;
            }

            .nav-item.active {
                display: inline-block;
                margin: 0;
            }

            main {
                padding: 23px 15px;
            }

            .topbar {
                align-items: flex-start;
                margin-bottom: 28px;
            }

            .status {
                font-size: 9px;
            }

            .metrics {
                gap: 9px;
            }

            .metric {
                padding: 15px 12px;
            }

            .metric-label {
                min-height: 32px;
            }

            .metric-value {
                font-size: 21px;
            }

            .panel-head,
            .panel-body {
                padding: 15px;
            }

            .chart {
                gap: 8px;
            }

            .section-heading {
                align-items: flex-start;
            }
        }

        @media (max-width: 360px) {
            .metrics {
                grid-template-columns: 1fr;
            }

            .topbar {
                flex-direction: column;
            }
        }
    </style>
<script src="/static/plotly.min.js"></script>
</head>

<body>
<div class="app">
    <aside class="sidebar">
        <div class="brand">
            <div class="brand-mark">Q</div>
            <div>
                <div class="brand-name">QUANTPAY</div>
                <div class="brand-sub">ROBERTSCIENCE</div>
            </div>
        </div>

        <div class="nav-label">INTELLIGENCE PLATFORM</div>
        <div class="nav-item active">Executive Overview</div>
        <div class="nav-item">Payment Analytics</div>
        <div class="nav-item">Quantitative Signals</div>
        <div class="nav-item">AI Insights</div>
        <div class="nav-item">Evidence &amp; Integrity</div>

        <div class="sidebar-bottom">
            PROJECT STATUS<br>
            <strong>Prototype · Phase 1</strong><br>
            Local interface only
        </div>
    </aside>

    <main>
        <header class="topbar">
            <div>
                <div class="eyebrow">FINANCIAL INTELLIGENCE / 01</div>
                <h1>From payments to decisions.</h1>
                <div class="subtitle">
                    Una perspectiva cuantitativa de la actividad financiera.
                </div>
            </div>
            <div class="status">LOCAL PROTOTYPE</div>
        </header>

        <section>
            <div class="section-heading">
                <h2>Executive Overview</h2>
                <span class="small">Indicadores de demostración</span>
            </div>

            <div class="metrics">
                <article class="metric">
                    <div class="metric-label">Volumen procesado</div>
                    <div class="metric-value">{{ metrics.volume }}</div>
                    <div class="metric-note">USD · Datos ilustrativos</div>
                </article>

                <article class="metric">
                    <div class="metric-label">Transacciones</div>
                    <div class="metric-value">{{ metrics.count }}</div>
                    <div class="metric-note">Registros de ejemplo</div>
                </article>

                <article class="metric">
                    <div class="metric-label">Ticket promedio</div>
                    <div class="metric-value">{{ metrics.average }}</div>
                    <div class="metric-note">Volumen / transacciones</div>
                </article>

                <article class="metric">
                    <div class="metric-label">Integridad del reporte</div>
                    <div class="metric-value">Pendiente</div>
                    <div class="metric-note gold">SHA-256 por implementar</div>
                </article>
                        </div>
        </section>

        <section class="panel" id="ai-insights" style="margin-bottom:22px">
            <div class="panel-head">
                <h2>AI Insights</h2>
                <span class="small">Análisis financiero simulado</span>
            </div>
            <div class="panel-body">
                <p class="small">
                    Genera una interpretación ejecutiva de los escenarios
                    cuantitativos de demostración.
                </p>
                <button
                    id="generate-ai-insights"
                    type="button"
                    style="background:#C8A24C;color:#171717;border:0;border-radius:6px;padding:10px 16px;font-weight:600;cursor:pointer"
                >
                    Generar análisis
                </button>
                <p
                    id="ai-insights-status"
                    class="small"
                    role="status"
                    aria-live="polite"
                    style="margin-bottom:0"
                >
                    Listo para solicitar el análisis.
                </p>
                <div
                    id="ai-insights-result"
                    class="small"
                    style="display:none;margin-top:16px;white-space:pre-wrap;line-height:1.7"
                ></div>
            </div>
        </section>

        <section class="panel" id="financial-upload" style="margin-bottom:22px">  <div class="panel-head">
        <h2>Financial Data Upload</h2>
        <span class="small">CSV / XLSX · Máximo 10 MB</span>
    </div>
    <div class="panel-body">
        <p class="small">Carga un archivo para validar su estructura. Esta acción no modifica las transacciones de PayPal.</p>
        <form id="data-upload-form" enctype="multipart/form-data" style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">
            <input type="file" name="file" accept=".csv,.xlsx,.jpg,.jpeg,.png" required style="max-width:100%;color:#ddd">
            <button type="submit" style="background:#C8A24C;color:#171717;border:0;border-radius:6px;padding:10px 16px;font-weight:600;cursor:pointer">Validar archivo</button>
        </form>
        <p id="data-upload-result" class="small" role="status" aria-live="polite" style="margin-bottom:0">Esperando un archivo.</p>
        <div id="quant-charts" class="panel" style="display:none;margin-top:18px"></div>
    </div>
</section>
<script src="/static/upload_charts.js"></script>
<div class="main-grid">
            <section class="panel">
                <div class="panel-head">
                    <h2>Financial Performance</h2>
                    <span class="small">Escenario simulado · USD</span>
                </div>
                <div class="panel-body">
                    <div class="small" style="margin-bottom:18px">
                        Comparativo de ingresos, costos y utilidad estimada.
                    </div>
                    <div style="display:grid;gap:22px">
                        <div>
                            <div style="display:flex;justify-content:space-between;margin-bottom:8px;gap:12px">
                                <span class="small">Ingresos</span><strong>{{ financial_metrics.revenue }}</strong>
                            </div>
                            <div style="height:10px;background:#303033;border-radius:5px;overflow:hidden">
                                <div style="height:100%;width:100%;background:#C8A24C"></div>
                            </div>
                        </div>
                        <div>
                            <div style="display:flex;justify-content:space-between;margin-bottom:8px;gap:12px">
                                <span class="small">Costos</span><strong>{{ financial_metrics.costs }}</strong>
                            </div>
                            <div style="height:10px;background:#303033;border-radius:5px;overflow:hidden">
                                <div style="height:100%;width:{{ financial_metrics.cost_ratio }}%;background:#8A7650"></div>
                            </div>
                        </div>
                        <div>
                            <div style="display:flex;justify-content:space-between;margin-bottom:8px;gap:12px">
                                <span class="small">Utilidad operativa estimada</span>
                                <strong style="color:#8BBE9B">{{ financial_metrics.profit }}</strong>
                            </div>
                            <div style="height:10px;background:#303033;border-radius:5px;overflow:hidden">
                                <div style="height:100%;width:{{ financial_metrics.margin }}%;background:#8BBE9B"></div>
                            </div>
                        </div>
                    </div>
                    <div class="chart-foot">
                        Ejemplo conceptual; no representa datos reales de clientes
                        ni de PayPal. No incluye impuestos ni otros conceptos.
                    </div>
                </div>
            </section>

            <section class="panel">
                <div class="panel-head">
                    <h2>Quantitative Insights</h2>
                    <span class="small">Escenario simulado</span>
                </div>
                <div class="panel-body">
                    <div class="insight">
                        <div class="insight-label">MARGEN OPERATIVO ESTIMADO</div>
                        <div style="font-size:30px;font-weight:600;color:#C8A24C">{{ financial_metrics.margin }}%</div>
                        <p>Utilidad estimada como proporción de los ingresos.</p>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
                        <div style="padding:14px;border:1px solid #303033;border-radius:8px">
                            <div class="small">Ingresos</div>
                            <div style="font-size:19px;margin-top:9px">{{ financial_metrics.revenue }}</div>
                        </div>
                        <div style="padding:14px;border:1px solid #303033;border-radius:8px">
                            <div class="small">Costos</div>
                            <div style="font-size:19px;margin-top:9px">{{ financial_metrics.costs }}</div>
                        </div>
                    </div>
                    <div class="insight" style="margin-top:16px;margin-bottom:0">
                        <div class="insight-label">BUSINESS QUESTION</div>
                        <p>¿Cómo cambiaría la rentabilidad si aumentan los costos,
                        se retrasan los cobros o suben las comisiones de pago?</p>
                    </div>
                    <div class="insight" style="margin-top:16px">
                        
                        <div class="insight-label">SENSIBILIDAD FINANCIERA · SIMULACIÓN</div>

                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px">
                            <div style="padding:12px;border:1px solid #303033;border-radius:8px">
                                <div class="small">Costos +5%</div>
                                <strong style="display:block;margin-top:8px;color:#C8A24C">{{ financial_metrics.costs_up_5 }}</strong>
                            </div>
                            <div style="padding:12px;border:1px solid #303033;border-radius:8px">
                                <div class="small">Ingresos -5%</div>
                                <strong style="display:block;margin-top:8px;color:#C8A24C">{{ financial_metrics.revenue_down_5 }}</strong>
                            </div>
                        </div>
                        <p class="small" style="margin-bottom:0">Utilidad estimada bajo cada escenario; datos sintéticos, no resultados reales.</p>
                    </div>
                    <div class="workflow">
                        <span class="step">Financial Data</span>
                        <span class="arrow">&rarr;</span>
                        <span class="step">Quant Models</span>
                        <span class="arrow">&rarr;</span>
                        <span class="step">AI Analysis</span>
                    </div>
                </div>
            </section>
        </div>

        <section class="panel table-panel">
            <div class="panel-head">
                <h2>Recent Transactions</h2>
                <span class="small">Registros ilustrativos · No sincronizados con PayPal</span>
            </div>

            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>REFERENCE</th>
                            <th>DATE</th>
                            <th>AMOUNT</th>
                            <th>STATUS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for tx in transactions %}
                        <tr>
                            <td class="muted">{{ tx.reference }}</td>
                            <td>{{ tx.date }}</td>
                            <td>{{ tx.amount }}</td>
                            <td><span class="pill">{{ tx.status }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </section>

    
    <section class="panel" style="margin-top: 22px;">
        <div class="panel-head">
            <h2>PayPal Sandbox Checkout</h2>
            <span class="small">Test payment · 1.00 USD</span>
        </div>
        <div class="panel-body">
            <p class="small">Approve a test payment through PayPal Sandbox. Capture is processed by the server.</p>
            <div id="paypal-button-container"></div>
            <p id="paypal-result" class="small" role="status" aria-live="polite">Ready for Sandbox checkout.</p>
        </div>
    </section>
{% if paypal_client_id %}
    <script src="https://www.paypal.com/sdk/js?client-id={{ paypal_client_id }}&currency=USD&intent=capture"></script>
    <script>
    (() => {
        const output = document.getElementById("paypal-result");
        const show = message => { output.textContent = message; };

        if (!window.paypal || !window.paypal.Buttons) {
            show("PayPal SDK unavailable. Check the connection and Sandbox Client ID.");
            return;
        }

        paypal.Buttons({
            createOrder: async () => {
                const response = await fetch("/api/paypal/order", {method: "POST"});
                const order = await response.json();
                if (!response.ok) throw new Error(order.error || "Order creation failed.");
                show("Order created. Approve it in PayPal Sandbox.");
                return order.id;
            },
            onApprove: async data => {
                show("Approval received. Capturing...");
                const response = await fetch(
                    "/api/paypal/order/" + encodeURIComponent(data.orderID) + "/capture",
                    {method: "POST"}
                );
                const result = await response.json();
                if (!response.ok) throw new Error(result.error || "Capture failed.");
                const capture = result.purchase_units?.[0]?.payments?.captures?.[0];
                show(capture
                    ? "Capture: " + capture.status + " | " +
                      (capture.amount?.currency_code || "USD") + " " +
                      (capture.amount?.value || "-") + " | ID: " + capture.id
                    : "Order status: " + (result.status || "processed"));
            },
            onError: error => {
                show("Sandbox checkout failed. Check the order and try again.");
                console.error("PayPal Sandbox checkout error", error);
            }
        }).render("#paypal-button-container").catch(() => {
            show("Could not initialize PayPal checkout.");
        });
    })();
    </script>
{% else %}
    <script>
    document.getElementById("paypal-result").textContent =
        "Configure PAYPAL_CLIENT_ID to enable Sandbox checkout.";
    </script>
{% endif %}

    
    <footer class="demo-note">
        ROBERTSCIENCE &middot; QUANTPAY INTELLIGENCE<br>
        Prototipo local. Checkout PayPal Sandbox integrado; modelos cuantitativos avanzados, análisis con IA y huellas SHA-256 pendientes.
    </footer>

    </main>
</div>
<script src="/static/ai_insights.js"></script>
</body>
</html>
"""


@app.route("/api/paypal/order", methods=["POST"])
def paypal_create_order_route():
    try:
        order = paypal_create_order()
        return order, 201
    except Exception:
        return {"error": "No se pudo crear la orden de PayPal Sandbox."}, 502

@app.route("/api/paypal/order/<order_id>", methods=["GET"])
def paypal_order_status(order_id):
    try:
        order = paypal_get_order(order_id)
        unit = (order.get("purchase_units") or [{}])[0]
        amount = unit.get("amount") or {}
        return {
            "id": order.get("id"),
            "status": order.get("status"),
            "amount": amount.get("value"),
            "currency": amount.get("currency_code"),
        }, 200
    except Exception:
        return {"error": "No se pudo consultar la orden de PayPal Sandbox."}, 502


@app.route("/api/paypal/order/<order_id>/capture", methods=["POST"])
def paypal_capture_order_route(order_id):
    try:
        order = paypal_get_order(order_id)
        if order.get("status") != "APPROVED":
            return {"error": "La orden debe estar APPROVED antes de capturarla.", "status": order.get("status")}, 409
        result = paypal_capture_order(order_id)
        return result, 200
    except Exception:
        return {"error": "No se pudo completar la captura de PayPal Sandbox."}, 502


@app.route("/api/paypal/order/<order_id>/captures", methods=["GET"])
def paypal_order_captures(order_id):
    try:
        order = paypal_get_order(order_id)
        unit = (order.get("purchase_units") or [{}])[0]
        payments = unit.get("payments") or {}
        captures = payments.get("captures") or []
        return {
            "order_id": order.get("id"),
            "order_status": order.get("status"),
            "captures": [
                {
                    "id": capture.get("id"),
                    "status": capture.get("status"),
                    "amount": (capture.get("amount") or {}).get("value"),
                    "currency": (capture.get("amount") or {}).get("currency_code"),
                    "created": capture.get("create_time"),
                }
                for capture in captures
            ],
        }, 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": "La orden de PayPal Sandbox no existe.", "order_id": order_id}, 404
        return {"error": "No se pudieron consultar las capturas de PayPal Sandbox."}, 502
    except Exception:
        return {"error": "No se pudieron consultar las capturas de PayPal Sandbox."}, 502 

@app.route("/api/ai/insights", methods=["POST"])
def ai_insights_route():
    financial = quant_engine.analyze_financials(
        revenue="100000.00",
        costs="72000.00",
        cost_increase_pct=5,
        revenue_change_pct=-5,
    )

    financial_metrics = {
        "revenue": str(financial["revenue"]),
        "costs": str(financial["costs"]),
        "profit": str(financial["profit"]),
        "margin": str(financial["margin_pct"]),
        "costs_up_5": str(financial["profit_cost_scenario"]),
        "revenue_down_5": str(financial["profit_revenue_scenario"]),
    }

    result = generate_ai_insights(financial_metrics)
    return result, (200 if result.get("ok") else 503)


@app.route("/")
def index():
    
    transactions = [
        {
            "reference": "DEMO-001",
            "date": "2026-10-19",
            "amount": Decimal("245.00"),
            "status": "Prueba local",
        },
        {
            "reference": "DEMO-002",
            "date": "2026-10-20",
            "amount": Decimal("89.50"),
            "status": "Prueba local",
        },
        {
            "reference": "DEMO-003",
            "date": "2026-10-21",
            "amount": Decimal("510.00"),
            "status": "Prueba local",
        },
    ]

    volume = sum((tx["amount"] for tx in transactions), Decimal("0.00"))
    count = len(transactions)
    average = volume / count if count else Decimal("0.00")
    largest = max(transactions, key=lambda tx: tx["amount"]) if transactions else None
    smallest = min(transactions, key=lambda tx: tx["amount"]) if transactions else None
    concentration = (largest["amount"] / volume * Decimal("100")) if largest and volume else Decimal("0.00")
    signals = {
        "max_amount": f"${largest['amount']:,.2f}" if largest else "$0.00",
        "max_reference": largest["reference"] if largest else "N/A",
        "min_amount": f"${smallest['amount']:,.2f}" if smallest else "$0.00",
        "min_reference": smallest["reference"] if smallest else "N/A",
        "concentration": f"{concentration:.1f}%",
    }

    metrics = {
        "volume": f"${volume:,.2f}",
        "count": count,
        "average": f"${average:,.2f}",
    }

    financial = quant_engine.analyze_financials(
        revenue="100000.00",
        costs="72000.00",
        cost_increase_pct=5,
        revenue_change_pct=-5,
    )
    financial_metrics = {
        "revenue": f"${financial['revenue']:,.0f}",
        "costs": f"${financial['costs']:,.0f}",
        "profit": f"${financial['profit']:,.0f}",
        "margin": f"{financial['margin_pct']:.1f}",
        "cost_ratio": f"{financial['cost_ratio_pct']:.1f}",
        "costs_up_5": f"${financial['profit_cost_scenario']:,.0f}",
        "revenue_down_5": f"${financial['profit_revenue_scenario']:,.0f}",
    }

    for tx in transactions:
        tx["amount"] = f"${tx['amount']:,.2f}"

    return render_template_string(
        HTML, metrics=metrics, signals=signals, transactions=transactions, financial_metrics=financial_metrics, paypal_client_id=os.environ.get('PAYPAL_CLIENT_ID', '')
    )


if __name__ == "__main__":
    app.run(debug=True)



