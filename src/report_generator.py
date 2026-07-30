from datetime import datetime
import re


class ReportGenerator:

    def __init__(
        self,
        template_path="templates/report_template.html",
        output_path="reports/report.html",
    ):
        self.template_path = template_path
        self.output_path = output_path

    def load_template(self):
        with open(self.template_path, "r", encoding="utf-8") as file:
            return file.read()

    def _format_value(self, value):
        """Formats raw numeric KPI values into clean string representations."""
        if isinstance(value, float):
            return f"${value:,.2f}" if value > 100 else f"{value:.2f}%"
        elif isinstance(value, int):
            return f"{value:,}"
        return str(value)

    def _clean_markdown(self, text):
        """Helper to convert simple Markdown bolding and inline syntax into HTML."""
        if not isinstance(text, str):
            return text
        # Convert **bold** to <strong>bold</strong>
        return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    def build_kpi_cards(self, kpis):
        html = ""

        # Keys to exclude from top KPI cards because they belong in chart views
        exclude = {
            "monthly_sales",
            "monthly_profit",
            "sales_by_category",
            "sales_by_region",
            "sales_by_segment",
            "top_products",
            "top_customers",
        }

        for key, value in kpis.items():
            if key in exclude:
                continue

            title = key.replace("_", " ").title()
            formatted_value = self._format_value(value)

            # Follows contract: .kpi-card > .kpi-title + .kpi-value
            html += f"""
        <div class="kpi-card">
          <div class="kpi-title">{title}</div>
          <div class="kpi-value">{formatted_value}</div>
        </div>"""

        return html

    def build_chart_gallery(self):
        # Configure chart components matching the provided HTML grid contract
        charts = [
            ("Monthly Sales Trend", "../charts/monthly_sales.png"),
            ("Monthly Profitability", "../charts/monthly_profit.png"),
            ("Sales Breakdown by Category", "../charts/sales_by_category.png"),
            ("Regional Sales Performance", "../charts/sales_by_region.png"),
            ("Customer Segment Distribution", "../charts/sales_by_segment.png"),
            ("Top Performing Products", "../charts/top_products.png"),
        ]

        html = ""

        for title, image_path in charts:
            # Follows contract: .chart-card > .chart-title + img/svg
            html += f"""
        <div class="chart-card">
          <h3 class="chart-title">{title}</h3>
          <img src="{image_path}" alt="{title}" loading="lazy">
        </div>"""

        return html

    def build_ai_sections(self, insights):
        html = ""

        for title, content in insights.items():
            if title == "executive_summary":
                continue

            heading = title.replace("_", " ").title()

            # Follows contract: .analysis-container > section > h3 + p/ul
            html += f"""
        <section>
          <h3>{heading}</h3>"""

            if isinstance(content, str):
                formatted_text = self._clean_markdown(content)
                html += f"\n          <p>{formatted_text}</p>"

            elif isinstance(content, list):
                html += "\n          <ul>"
                for item in content:
                    formatted_item = self._clean_markdown(str(item))
                    html += f"\n            <li>{formatted_item}</li>"
                html += "\n          </ul>"

            html += "\n        </section>"

        return html

    def generate_html(self, kpis, insights):
        html = self.load_template()

        # Handle Executive Summary formatting cleanly
        raw_summary = insights.get("executive_summary", "")
        if isinstance(raw_summary, list):
            formatted_summary = "".join(
                [f"<p>{self._clean_markdown(p)}</p>" for p in raw_summary]
            )
        else:
            formatted_summary = f"<p>{self._clean_markdown(str(raw_summary))}</p>"

        placeholders = {
            "{{REPORT_DATE}}": datetime.now().strftime("%d %B %Y"),
            "{{EXECUTIVE_SUMMARY}}": formatted_summary,
            "{{KPI_CARDS}}": self.build_kpi_cards(kpis),
            "{{CHARTS}}": self.build_chart_gallery(),
            "{{AI_SECTIONS}}": self.build_ai_sections(insights),
        }

        for placeholder, value in placeholders.items():
            html = html.replace(placeholder, str(value))

        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(html)

        print(f"Report generated and saved to {self.output_path}")
