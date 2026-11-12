(() => {
    const form = document.getElementById("data-upload-form");
    const output = document.getElementById("data-upload-result");
    const charts = document.getElementById("quant-charts");

    const showInsight = (title, item) => {
        const section = document.createElement("section");
        section.style.cssText = "margin-top:16px;padding:14px;background:#202024;border-radius:8px";
        const heading = document.createElement("h3");
        heading.textContent = title;
        section.append(heading);
        if (item && Array.isArray(item.insights)) {
            item.insights.forEach(entry => {
                const row = document.createElement("p");
                row.className = "small";
                row.style.whiteSpace = "pre-wrap";
                row.textContent = (entry.title ? entry.title + ": " : "") + (entry.message || "");
                section.append(row);
            });
            if (item.limitations && item.limitations.length) {
                const note = document.createElement("p");
                note.className = "small";
                note.textContent = "Limitaciones: " + item.limitations.join("; ");
                section.append(note);
            }
            if (!item.insights.length) {
                const empty = document.createElement("p");
                empty.className = "small";
                empty.textContent = "No se detectaron hallazgos con las reglas actuales.";
                section.append(empty);
            }
        } else {
            const text = document.createElement("p");
            text.className = "small";
            text.style.whiteSpace = "pre-wrap";
            text.textContent = item && item.insight ? item.insight : "Resultado de IA no disponible: " + (item && item.ok === false ? item.insight : "respuesta vacía o formato inesperado.");
            section.append(text);
        }
        charts.append(section);
    };

    form.addEventListener("submit", async event => {
        event.preventDefault();
        const file = form.elements.file.files[0];
        if (!file) return;

        output.textContent = "Analizando archivo...";
        charts.style.display = "none";
        charts.replaceChildren();

        const body = new FormData();
        body.append("file", file);

        try {
            const response = await fetch("/api/data/upload", { method: "POST", body });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || "No se pudo analizar el archivo.");

            const analysis = result.quantitative_analysis || {};
            const financial = result.financial_analysis || {};
            const metrics = analysis.financials || {};
            const number = value => {
                const parsed = Number(value);
                return Number.isFinite(parsed) ? parsed : 0;
            };
            const money = value => new Intl.NumberFormat("es-MX", {
                style: "currency", currency: "USD", maximumFractionDigits: 2
            }).format(number(value));

            output.textContent = "Analizado: " + result.filename + " · " + result.rows +
                " filas · Columnas: " + (result.columns || []).join(", ") + ". " + (result.note || "");

            charts.style.display = "block";

            const heading = document.createElement("h2");
            heading.textContent = "Análisis del archivo cargado";
            charts.append(heading);

            const summary = document.createElement("p");
            summary.className = "small";
            summary.textContent = "Resultados exclusivos de este archivo; separados del escenario simulado y de PayPal.";
            charts.append(summary);

            const metricGrid = document.createElement("div");
            metricGrid.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0";
            [
                ["Ingresos", financial.revenue ?? metrics.revenue],
                ["Costos", financial.costs ?? metrics.costs],
                ["Utilidad", financial.profit ?? metrics.profit]
            ].forEach(([label, value]) => {
                const card = document.createElement("div");
                card.style.cssText = "padding:14px;background:#202024;border-radius:8px";
                const name = document.createElement("div");
                name.className = "small";
                name.textContent = label;
                const amount = document.createElement("strong");
                amount.textContent = money(value);
                card.append(name, amount);
                metricGrid.append(card);
            });
            charts.append(metricGrid);

            const plot = document.createElement("div");
            plot.style.cssText = "width:100%;min-height:320px";
            charts.append(plot);

            const plotValues = [
                number(financial.revenue ?? metrics.revenue),
                number(financial.costs ?? metrics.costs),
                number(financial.profit ?? metrics.profit)
            ];
            if (window.Plotly) {
                await Plotly.newPlot(plot, [{
                    x: ["Ingresos", "Costos", "Utilidad"],
                    y: plotValues,
                    type: "bar",
                    marker: { color: ["#C8A24C", "#8B8B91", "#6DAD83"] },
                    text: plotValues.map(money),
                    textposition: "auto",
                    hovertemplate: "%{x}: %{y:,.2f} USD<extra></extra>"
                }], {
                    paper_bgcolor: "rgba(0,0,0,0)",
                    plot_bgcolor: "rgba(0,0,0,0)",
                    font: { color: "#F5F2EA" },
                    margin: { t: 24, r: 20, b: 50, l: 65 },
                    yaxis: { title: "USD", gridcolor: "#38383D", zerolinecolor: "#55555A" },
                    xaxis: { fixedrange: true },
                    autosize: true
                }, { responsive: true, displaylogo: false });
            } else {
                plot.textContent = "Plotly no está disponible; se muestran los indicadores sin gráfica.";
            }

            const concentration = analysis.revenue_concentration || {};
            const indicators = document.createElement("p");
            indicators.className = "small";
            indicators.style.cssText = "margin-top:14px;line-height:1.8";
            indicators.textContent =
                "Margen: " + (financial.margin_pct ?? metrics.margin_pct ?? "N/D") + "% · " +
                "Proporción de costos: " + (financial.cost_ratio_pct ?? metrics.cost_ratio_pct ?? "N/D") + "% · " +
                "Participación de ingresos del grupo superior: " +
                (concentration.revenue_share_pct ?? "N/D") + "%.";
            charts.append(indicators);

            const temporal = analysis.temporal_analysis;
            if (Array.isArray(temporal) && temporal.length > 0 && window.Plotly) {
                const temporalTitle = document.createElement("h3");
                temporalTitle.textContent = "Evolución temporal del archivo";
                const temporalPlot = document.createElement("div");
                temporalPlot.style.cssText = "width:100%;min-height:320px";
                charts.append(temporalTitle, temporalPlot);
                await Plotly.newPlot(temporalPlot, [
                    { x: temporal.map(p => p.date), y: temporal.map(p => number(p.revenue)), name: "Ingresos", type: "scatter", mode: "lines+markers" },
                    { x: temporal.map(p => p.date), y: temporal.map(p => number(p.costs)), name: "Costos", type: "scatter", mode: "lines+markers" },
                    { x: temporal.map(p => p.date), y: temporal.map(p => number(p.profit)), name: "Utilidad", type: "scatter", mode: "lines+markers" }
                ], {
                    paper_bgcolor: "rgba(0,0,0,0)",
                    plot_bgcolor: "rgba(0,0,0,0)",
                    font: { color: "#F5F2EA" },
                    margin: { t: 24, r: 20, b: 50, l: 65 },
                    xaxis: { type: "date", gridcolor: "#38383D" },
                    yaxis: { title: "USD", gridcolor: "#38383D" },
                    legend: { orientation: "h" }
                }, { responsive: true, displaylogo: false });
            }

            showInsight("Insights cuantitativos", result.ai_insights);
            showInsight("Propuesta de Gemini", result.ai_proposal);
        } catch (error) {
            output.textContent = "Error: " + error.message;
        }
    });
})();
