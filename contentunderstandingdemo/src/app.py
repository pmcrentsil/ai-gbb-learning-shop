import os
from pathlib import Path
import sys
import logging
import requests
import time
import json
import uuid
import subprocess
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from content_understanding.content_understanding_client import AzureContentUnderstandingClient

logging.basicConfig(level=logging.INFO)

# The URL and Version for the Content Understanding API
AZURE_AI_ENDPOINT = "ENTER AZURE AI SERVICES ENDPOINT"
AZURE_AI_API_VERSION = "2024-12-01-preview"


def create_analyzer(cu_client, analyzer_id, analyzer_template_path):
    """Creates a new Content Understanding analyzer."""
    return cu_client.begin_create_analyzer(
        analyzer_id=analyzer_id,
        analyzer_template_path=analyzer_template_path
    )


def run_analyzer(cu_client, analyzer_id, file_location):
    """Analyzes the document using the specified analyzer."""
    try:
        analyze_file = cu_client.begin_analyze(
            analyzer_id=analyzer_id,
            file_location=file_location
        )
    except Exception as e:
        logging.error("Failed to analyze the document. Error message:\n %s", e)
        cu_client.delete_analyzer(analyzer_id=analyzer_id)
        sys.exit(1)
    return analyze_file


def save_extraction_results(result):
    """Extract itinerary details and save them to a JSON file."""
    extracted_data = {
        "TripName": "Unknown",
        "Destinations": "Unknown",
        "StartDate": "Unknown",
        "EndDate": "Unknown",
        "Recommendations": []
    }

    # Ensure the correct structure and check if fields exist in the extraction result
    if "result" in result and "contents" in result["result"]:
        content = result["result"]["contents"][0]  # Assuming the first content is relevant

        if "fields" in content:
            extracted_data["TripName"] = content["fields"].get("TripName", {}).get("valueString", "Unknown")
            extracted_data["Destinations"] = content["fields"].get("Destinations", {}).get("valueString", "Unknown")
            
            # Extract StartDate and EndDate, check for both string and date formats
            start_date = content["fields"].get("StartDate", {})
            end_date = content["fields"].get("EndDate", {})
            
            # Extract valueDate first, else fallback to valueString
            extracted_data["StartDate"] = start_date.get("valueDate", start_date.get("valueString", "Unknown"))
            extracted_data["EndDate"] = end_date.get("valueDate", end_date.get("valueString", "Unknown"))

            # Log extracted StartDate and EndDate for debugging
            logging.info(f"Extracted Start Date: {extracted_data['StartDate']}")
            logging.info(f"Extracted End Date: {extracted_data['EndDate']}")

    # Log extracted details
    logging.info("Extracted Trip Details:")
    logging.info(f"Trip Name: {extracted_data['TripName']}")
    logging.info(f"Destinations: {extracted_data['Destinations']}")
    logging.info(f"Start Date: {extracted_data['StartDate']}")
    logging.info(f"End Date: {extracted_data['EndDate']}")

    # Save to JSON file
    with open("extracted_itinerary.json", "w") as outfile:
        json.dump(extracted_data, outfile, indent=2)
    
    logging.info("✅ Extracted itinerary details saved to 'extracted_itinerary.json'.")


def trigger_agent_process():
    """Trigger the recommendation agent process, update itinerary, and generate a PDF."""
    try:
        logging.info("🚀 Starting recommendation agent process...")
        subprocess.run(["python", "recommendation_agent.py"], check=True)
        logging.info("✅ Recommendation agent process completed.")

        # Now call itinerary_updater.py
        logging.info("🔄 Updating finalized itinerary using itinerary_updater.py...")
        subprocess.run(["python", "itinerary_updater.py"], check=True)
        logging.info("✅ Finalized itinerary successfully updated!")

        # Generate the PDF after everything is finalized
        logging.info("📄 Generating itinerary PDF using generate_itinerary_pdf.py...")
        subprocess.run(["python", "generate_itinerary_pdf.py"], check=True)
        logging.info("✅ PDF successfully generated!")

    except subprocess.CalledProcessError as e:
        logging.error("❌ Process failed: %s", e)


def main():
    """Main execution flow."""
    ANALYZER_ID = "recipe_analyzer-" + str(uuid.uuid4().hex[:8])
    ANALYZER_TEMPLATE_PATH = Path("analyzer_templates/recipes.json").resolve()
    RECIPE_FILE = "https://cooking.blob.core.windows.net/travel/African_Safari_Itinerary.pdf"

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

    logging.info("Analyzer template path: %s", ANALYZER_TEMPLATE_PATH)

    cu_client = AzureContentUnderstandingClient(
        endpoint=AZURE_AI_ENDPOINT,
        api_version=AZURE_AI_API_VERSION,
        token_provider=token_provider,
    )

    analyzer = create_analyzer(cu_client, ANALYZER_ID, ANALYZER_TEMPLATE_PATH)
    result = cu_client.poll_result(analyzer)

    if result and "status" in result and result["status"] == "Succeeded":
        logging.info("✅ Analyzer '%s' created successfully!", result['result']['analyzerId'])
        logging.info(json.dumps(result, indent=2))
    else:
        logging.error("❌ Failed to create the analyzer.")
        logging.error(json.dumps(result, indent=2))
        sys.exit(1)

    analyze_file = run_analyzer(cu_client, ANALYZER_ID, RECIPE_FILE)
    result = cu_client.poll_result(analyze_file)

    logging.info("📊 Status of the analyze operation: %s", result["status"])
    logging.info("🔎 Analyze operation completed with the result:")
    logging.info(json.dumps(result, indent=2))

    # Save extraction results
    save_extraction_results(result)

    # Trigger the AI recommendation, itinerary update, and PDF generation
    trigger_agent_process()


if __name__ == "__main__":
    main()
