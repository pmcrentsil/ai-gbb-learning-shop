AI-Powered Travel Itinerary Setup Guide
 ## Prerequisites
 Before setting up the project, ensure you have the following:- Azure Subscription (Required to set up services)- Python 3.11+ installed on your local machine- Azure CLI installed and configured- Git installed (optional but recommended)
 ## 1. Azure Portal Setup
 ### 1.1 Create an Azure AI Services Resource
 1. Go to the Azure Portal.
 2. Search for Azure AI Services and create a new resource.
 3. Select the Pricing Tier that fits your needs.
 4. Copy the Endpoint and API Key after deployment.
 ### 1.2 Set Up Azure Blob Storage for PDF Templates
 1. In the Azure Portal, search for Storage Accounts.
 2. Click Create and set up the storage account.
 3. In Containers, create a new container named travel-itineraries.
 4. Upload the PDF template (travel_itinerary_template.pdf).
 5. Copy the Storage Account Connection String.
AI-Powered Travel Itinerary Setup Guide
 ### 1.3 Create an Azure AI Content Understanding Resource
 1. Navigate to Azure AI Content Understanding.
 2. Click Create and follow the setup process.
 3. Copy the Endpoint URL and Subscription Key.--
## 2. Environment Setup
 ### 2.1 Clone the Repository
 git clone https://github.com/your-repo/travel-itinerary-ai.git
 cd travel-itinerary-ai
 ### 2.2 Install Required Python Packages
 python -m venv venv
 source venv/bin/activate  # For macOS/Linux
 venv\Scripts\activate  # For Windows
 pip install -r requirements.txt
 ### 2.3 Configure Environment Variables
 Create a .env file in the root of your project and add the following:
 AZURE_AI_ENDPOINT=https://your-ai-service.cognitiveservices.azure.com/
 AZURE_AI_API_VERSION=2024-12-01-preview
 AZURE_STORAGE_CONNECTION_STRING="your-azure-storage-connection-string"
AI-Powered Travel Itinerary Setup Guide
 AZURE_BLOB_CONTAINER_NAME="travel-itineraries"--
## 3. Running the AI Pipeline
 ### 3.1 Step-by-Step Execution
 Run the following command to start the process:
 python app.py
 This will:- Extract itinerary details from the uploaded travel PDF.- Call Azure AI Content Understanding API to analyze the itinerary.- Generate AI-powered recommendations using recommendation_agent.py.- Update the structured itinerary JSON file (finalized_itinerary.json).- Generate a downloadable PDF itinerary (generate_itinerary_pdf.py).
 ### 3.2 Verify Output
 Check the following files after execution:- extracted_itinerary.json - Extracted trip details- finalized_itinerary.json - AI-enhanced structured itinerary- finalized_itinerary.pdf - Generated PDF itinerary--
AI-Powered Travel Itinerary Setup Guide
 ## 4. Automating with Azure Functions (Optional)
 To automate itinerary processing with Azure Functions:
 1. Deploy the project to Azure Functions.
 2. Configure it to trigger when a new PDF is uploaded to Azure Blob Storage.
 3. Connect it with the AI Services API to generate the itinerary automatically.--
## 5. Troubleshooting
 ### 5.1 Common Errors & Fixes
 Error: ModuleNotFoundError: No module named 'fpdf'
 Solution: Run pip install fpdf2
 Error: Invalid JSON format in extracted_itinerary.json
 Solution: Ensure proper API responses and valid JSON
 Error: FileNotFoundError: extracted_itinerary.json not found
 Solution: Verify app.py execution and check output logs--
AI-Powered Travel Itinerary Setup Guide
 ## 6. Conclusion
 Your AI-powered travel itinerary is now set up! You can now generate AI-enhanced itineraries,
 complete with recommendations and a professional PDF format.
 Run the pipeline anytime using:
 python app.p