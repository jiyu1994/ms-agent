import requests
import time

# API配置
API_KEY = "apikey-dd675b2a3fcb4f1aa88b91503d87f730"
BASE_URL = "https://api.atlascloud.ai"

# Step 1: Start video generation
generate_url = f"{BASE_URL}/api/v1/model/generateVideo"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

data = {
    "model": "openai/sora-2/text-to-video-pro",
    "duration": 4,
    "prompt": "A beautiful sunset over the ocean with gentle waves",
    "size": "720*1280"
}

print("Starting video generation...")
generate_response = requests.post(generate_url, headers=headers, json=data)

print(f"Response status: {generate_response.status_code}")
print(f"Response text: {generate_response.text}")

if generate_response.status_code != 200:
    print(f"Error: Failed to start video generation. Status: {generate_response.status_code}")
    exit(1)

generate_result = generate_response.json()
prediction_id = generate_result["data"]["id"]

print(f"Prediction ID: {prediction_id}")

# Step 2: Poll for result
poll_url = f"{BASE_URL}/api/v1/model/prediction/{prediction_id}"

def check_status():
    while True:
        print("Checking status...")
        response = requests.get(poll_url, headers={"Authorization": f"Bearer {API_KEY}"})

        if response.status_code != 200:
            print(f"Error checking status: {response.status_code}")
            print(f"Response: {response.text}")
            return None

        result = response.json()
        status = result["data"]["status"]

        print(f"Current status: {status}")

        if status in ["completed", "succeeded"]:
            video_url = result["data"]["outputs"][0]
            print("Generated video:", video_url)
            return video_url
        elif status == "failed":
            error_msg = result["data"].get("error", "Generation failed")
            print(f"Generation failed: {error_msg}")
            return None
        else:
            # Still processing, wait 2 seconds
            print("Still processing, waiting 2 seconds...")
            time.sleep(2)

video_url = check_status()

if video_url:
    print(f"\nSuccess! Video URL: {video_url}")
else:
    print("\nFailed to generate video")
