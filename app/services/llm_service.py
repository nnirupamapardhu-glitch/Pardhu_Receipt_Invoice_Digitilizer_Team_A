# import google.generativeai as genai
# import json
# import re
# from app.core.config import GEMINI_API_KEY

# # config gemini api
# genai.configure(api_key=GEMINI_API_KEY)

# # Intialise the llm model
# model = genai.GenerativeModel("gemini-2.5-flash")

# # Fucntion to raw data
# def extract_invoice_data(raw_text: str):

#     prompt = f"""
#     Extract the following fields from this invoice text.

#     Return ONLY valid JSON with:
#     invoice_number
#     vendor_name
#     date
#     total_amount

#     Invoice Text:
#     {raw_text}
#     """

#     response = model.generate_content(prompt)

#     text_response = response.text.strip()

#     # Remove markdown if Gemini wraps JSON in ```json
#     text_response = re.sub(r"```json|```", "", text_response).strip()


#     try:
#         structured_data = json.loads(text_response)
#         return structured_data
#     except:
#         return {"error": "Failed to parse JSON", "raw_output": text_response}


import google.generativeai as genai
import json
import re
from app.core.config import GEMINI_API_KEY


# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialise the LLM model
model = genai.GenerativeModel("gemini-2.5-flash")


# Function to clean numeric values coming from OCR/LLM
def clean_number(value):
    if not value:
        return 0

    text = str(value)

    # remove spaces between digits
    text = text.replace(" ", "")

    # remove all non numeric characters except decimal
    text = re.sub(r"[^\d.]", "", text)

    try:
        return float(text)
    except:
        return 0


def extract_invoice_data(raw_text: str):

    prompt = f"""
You are an AI that extracts structured information from receipts or invoices.

Extract the following fields from the text.

Return ONLY valid JSON in this format:

{{
  "invoice_number": "",
  "vendor_name": "",
  "date": "",
  "total_amount": "",
  "items": [
    {{
      "name": "",
      "quantity": "",
      "price": ""
    }}
  ]
}}

Rules:
- Extract all purchased items listed in the receipt.
- Quantity should be numeric if available.
- If quantity is missing assume 1.
- Prices must be numeric.
- Do not return explanations.
- Return JSON only.

Invoice Text:
{raw_text}
"""

    response = model.generate_content(prompt)

    text_response = response.text.strip()

    # Remove markdown formatting if Gemini wraps output
    text_response = re.sub(r"```json|```", "", text_response).strip()

    try:
        structured_data = json.loads(text_response)

        # Clean numbers
        structured_data["total_amount"] = clean_number(
            structured_data.get("total_amount")
        )

        if "items" in structured_data:
            for item in structured_data["items"]:

                item["quantity"] = clean_number(
                    item.get("quantity")
                ) or 1

                item["price"] = clean_number(
                    item.get("price")
                )

                # calculate total
                item["total"] = item["quantity"] * item["price"]

        return structured_data

    except Exception as e:
        return {
            "error": "Failed to parse JSON",
            "raw_output": text_response
        }
