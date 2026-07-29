from google import genai
from dotenv import load_dotenv
from prompts import BUSINESS_PROMPT
import json
import os

load_dotenv()


class AIInsights:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate_insights(self, kpis):
        try:
            prompt = BUSINESS_PROMPT.format(kpis=kpis)

            response = self.client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )
            print(response.text)
            return json.loads(response.text)
        except Exception as error:
            return f"Error generating insights: {error}"

    def save_report(self, insights):
        with open("reports/report.md", "w", encoding="utf-8") as file:
            file.write(insights)
