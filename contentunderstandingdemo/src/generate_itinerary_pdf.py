from fpdf import FPDF
import json
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

INPUT_FILE = "finalized_itinerary.json"
OUTPUT_PDF = "finalized_itinerary.pdf"

def clean_text(text):
    """Removes unsupported characters for PDF encoding"""
    return text.encode('latin-1', 'ignore').decode('latin-1')

def create_itinerary_pdf():
    try:
        # Load finalized itinerary
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            itinerary_data = json.load(file)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "", 12)
        pdf.add_page()

        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, clean_text(itinerary_data.get("TripName", "Travel Itinerary")), ln=True, align="C")
        pdf.ln(10)

        # Destinations
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"Destinations: {clean_text(itinerary_data.get('Destinations', 'Unknown'))}", ln=True)

        # Dates
        pdf.cell(200, 10, f"Start Date: {itinerary_data.get('StartDate', 'Unknown')}", ln=True)
        pdf.cell(200, 10, f"End Date: {itinerary_data.get('EndDate', 'Unknown')}", ln=True)
        pdf.ln(10)

        # Day-wise itinerary
        pdf.set_font("Arial", "", 11)
        for day, activities in itinerary_data.get("Days", {}).items():
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, clean_text(day), ln=True)
            pdf.set_font("Arial", "", 11)

            for time_of_day, activity in activities.items():
                if activity:
                    pdf.cell(200, 10, f"{time_of_day}: {clean_text(activity)}", ln=True)

            pdf.ln(5)

        # Save PDF
        pdf.output(OUTPUT_PDF)
        logging.info(f"✅ PDF successfully saved as {OUTPUT_PDF}")

    except Exception as e:
        logging.error(f"❌ Error saving PDF: {e}")

if __name__ == "__main__":
    create_itinerary_pdf()

