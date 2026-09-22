import os
import sys
import json
from unittest.mock import patch
from azure.identity import DefaultAzureCredential

def mock_cred():
    return DefaultAzureCredential()

with patch("azure.identity.InteractiveBrowserCredential", mock_cred):
    from src.pipeline import index_image
    from src.search_agent import generate_moderation_report

    def main():
        image_path = os.path.abspath("media/test_yelling.jpg")
        
        print("Indexing image...")
        data = index_image(image_path)
        print("Unified Text Extracted:")
        print(data['unified_text'])

        print("\nGenerating Moderation Report...")
        report = generate_moderation_report("test_yelling.jpg")
        print("\nFinal Moderation Report:")
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
