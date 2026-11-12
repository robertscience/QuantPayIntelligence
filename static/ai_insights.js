(() => {
    "use strict";

    const button = document.getElementById("generate-ai-insights");
    const status = document.getElementById("ai-insights-status");
    const result = document.getElementById("ai-insights-result");

    if (!button || !status || !result) {
        return;
    }

    button.addEventListener("click", async () => {
        button.disabled = true;
        status.textContent = "Generando análisis...";
        result.textContent = "";
        result.style.display = "none";

        try {
            const response = await fetch("/api/ai/insights", {
                method: "POST",
                headers: {
                    "Accept": "application/json"
                }
            });

            const data = await response.json();

            if (!response.ok || !data.ok) {
                throw new Error(
                    data.insight || data.error ||
                    "No fue posible generar el análisis."
                );
            }

            result.textContent = data.insight;
            result.style.display = "block";
            status.textContent = "Análisis generado correctamente.";
        } catch (error) {
            status.textContent =
                "No se pudo generar el análisis. Inténtalo más tarde.";
            console.error("AI Insights error:", error);
        } finally {
            button.disabled = false;
        }
    });
})();