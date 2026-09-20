import os
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

load_dotenv()

# Load credentials from .env
endpoint = os.getenv("AZURE_VISION_ENDPOINT")
key = os.getenv("AZURE_VISION_KEY")

# Authenticate the client
client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))

# Load your test image
image_path = "test.png"
with open(image_path, "rb") as f:
    image_data = f.read()

print("Sending image to Azure AI Vision...\n")

# Request both Tags (Description) and OCR (Text) extraction
result = client.analyze(
    image_data=image_data,
    visual_features=[VisualFeatures.TAGS, VisualFeatures.READ]
)

# Print the AI's description of the image
if result.tags is not None and len(result.tags.list) > 0:
    print("--- Image Description ---")
    tags = [tag.name for tag in result.tags.list]
    print(f"Tags: {', '.join(tags)}")

# Print any text the AI found written inside the image
if result.read is not None and len(result.read.blocks) > 0:
    print("\n--- Extracted Text (OCR) ---")
    for line in result.read.blocks[0].lines:
        print(f"- {line.text}")
else:
    print("\n--- Extracted Text (OCR) ---")
    print("No text found in the image.")