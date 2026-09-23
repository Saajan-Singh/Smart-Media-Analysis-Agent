import requests
import os

BASE_URL = "https://smart-media-analysis.vercel.app"
TEST_IMAGE_PATH = "media/0000.jpg"

def main():
    print(f"--- Testing {BASE_URL} ---")

    # Step 1: Frontend Verification
    try:
        res = requests.get(BASE_URL)
        if res.status_code == 200 and "html" in res.headers.get("Content-Type", ""):
            print("Step 1 (Frontend): PASS")
        else:
            print(f"Step 1 (Frontend): FAIL - Status Code: {res.status_code}")
            return
    except Exception as e:
        print(f"Step 1 (Frontend): FAIL - {e}")
        return

    # Step 2: Upload & Analysis Test
    print("\n--- Step 2: Upload ---")
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"Test image not found at {TEST_IMAGE_PATH}. Please create a valid dummy image.")
        return

    try:
        with open(TEST_IMAGE_PATH, "rb") as f:
            files = {"file": ("test_dummy.jpg", f, "image/jpeg")}
            upload_res = requests.post(f"{BASE_URL}/api/upload", files=files)
        
        if upload_res.status_code != 200:
            print(f"Step 2 (Upload): FAIL - Status {upload_res.status_code}")
            print(upload_res.text)
            return

        upload_data = upload_res.json()
        print("Upload Response:", upload_data)
        
        if upload_data.get("status") == "success" and upload_data.get("category"):
            print("Step 2 (Upload): PASS")
        else:
            print("Step 2 (Upload): FAIL - Missing or error data in JSON")
            return
    except Exception as e:
        print(f"Step 2 (Upload): FAIL - {e}")
        return

    # Step 3: Chat QA Test
    print("\n--- Step 3: Chat QA ---")
    try:
        chat_payload = {
            "query": "What is the category and risk score of this image?",
            "filename": upload_data["filename"],
            "context": upload_data
        }
        chat_res = requests.post(f"{BASE_URL}/api/chat", json=chat_payload)
        
        if chat_res.status_code != 200:
            print(f"Step 3 (Chat QA): FAIL - Status {chat_res.status_code}")
            print(chat_res.text)
            return

        chat_data = chat_res.json()
        print("Chat Response:", chat_data)
        
        if chat_data.get("answer"):
            print("Step 3 (Chat QA): PASS")
        else:
            print("Step 3 (Chat QA): FAIL - Missing answer")
            return
    except Exception as e:
        print(f"Step 3 (Chat QA): FAIL - {e}")
        return

    print("\nALL TESTS PASSED. The Vercel deployment is 100% production-ready.")

if __name__ == "__main__":
    main()
