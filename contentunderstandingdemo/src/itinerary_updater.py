import os
import json
import logging
from datetime import datetime, timedelta

# Logging setup
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

# File paths
EXTRACTED_FILE = "extracted_itinerary.json"
OUTPUT_FILE = "finalized_itinerary.json"

def generate_daywise_schedule(start_date, end_date, recommendations):
    """Organizes recommendations into a structured itinerary with morning, day, and night activities."""
    itinerary = {}

    try:
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        logging.error(f"Invalid date format: {e}")
        return {}

    while current_date <= end_date:
        formatted_date = current_date.strftime("%B %d, %Y")
        itinerary[formatted_date] = {"Morning": None, "Day": None, "Night": None}
        current_date += timedelta(days=1)

    # Assign recommendations to time slots
    time_slots = ["Morning", "Day", "Night"]
    slot_index = 0

    if recommendations:
        for recommendation in recommendations:
            content = recommendation.get("content", "").split("\n")

            for line in content:
                if not line.strip():
                    continue  # Skip empty lines

                for date in itinerary:
                    if itinerary[date][time_slots[slot_index]] is None:
                        itinerary[date][time_slots[slot_index]] = line.strip()
                        slot_index = (slot_index + 1) % 3  # Cycle through Morning, Day, Night
                        break

    return itinerary

def save_day_by_day_itinerary(extracted_data):
    """Processes extracted itinerary data and structures the trip day by day."""
    try:
        trip_name = extracted_data.get("TripName", "Unknown Trip")
        destinations = extracted_data.get("Destinations", "Unknown Destinations")
        start_date = extracted_data.get("StartDate")
        end_date = extracted_data.get("EndDate")

        # Extract AI-generated recommendations
        recommendations = extracted_data.get("Here are your AI agentic recommendations:", [])

        if not start_date or not end_date:
            logging.error("❌ Start date or end date missing in extracted data.")
            return

        logging.info(f"Trip Name: {trip_name}")
        logging.info(f"Destinations: {destinations}")
        logging.info(f"Start Date: {start_date}")
        logging.info(f"End Date: {end_date}")
        logging.info(f"Processing {len(recommendations)} AI-enhanced recommendations...")

        # Debug recommendations content
        if recommendations:
            logging.debug(f"AI-enhanced recommendations: {json.dumps(recommendations, indent=2)}")
        else:
            logging.warning("⚠️ No AI recommendations found!")

        # Generate structured itinerary using AI-enhanced recommendations
        structured_itinerary = generate_daywise_schedule(start_date, end_date, recommendations)

        # Debug itinerary structure
        logging.debug(f"Generated structured itinerary: {json.dumps(structured_itinerary, indent=2)}")

        # Finalized itinerary structure
        finalized_itinerary = {
            "TripName": trip_name,
            "Destinations": destinations,
            "StartDate": start_date,
            "EndDate": end_date,
            "Days": structured_itinerary,
            "Status": "Finalized with AI-enhanced recommendations"
        }

        # Debug before writing file
        logging.debug(f"Saving finalized itinerary to {OUTPUT_FILE}...")

        # Save to JSON
        with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
            json.dump(finalized_itinerary, outfile, indent=2, ensure_ascii=False)

        logging.info(f"✅ Finalized itinerary successfully saved to {OUTPUT_FILE}")

        # Verify if file was saved correctly
        if os.path.exists(OUTPUT_FILE):
            logging.info(f"✅ Verified: {OUTPUT_FILE} exists!")
            with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
                content = file.read()
                logging.debug(f"Finalized itinerary content:\n{content}")
        else:
            logging.error(f"❌ Error: {OUTPUT_FILE} was not created!")

    except Exception as e:
        logging.error(f"❌ Error saving finalized itinerary: {e}")

def main():
    """Loads extracted itinerary data and creates a structured travel plan."""
    if not os.path.exists(EXTRACTED_FILE):
        logging.error(f"❌ No extracted itinerary found! Ensure this file exists: {EXTRACTED_FILE}")
        return

    try:
        with open(EXTRACTED_FILE, "r", encoding="utf-8") as file:
            extracted_data = json.load(file)

        logging.info("✅ Extracted itinerary loaded successfully.")
        logging.debug(f"Extracted data content: {json.dumps(extracted_data, indent=2)}")  # Debug log

        # Save finalized itinerary
        save_day_by_day_itinerary(extracted_data)

    except json.JSONDecodeError as e:
        logging.error(f"❌ Error parsing JSON from {EXTRACTED_FILE}: {e}")
        return
    except Exception as e:
        logging.error(f"❌ Error loading extracted itinerary: {e}")
        return

if __name__ == "__main__":
    main()
