import os
import sys
import json
import requests
import pandas as pd
from pathlib import Path
import time
import base64
from apify_client import ApifyClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
ANKI_DECK = "English"
ANKI_MODEL = "Basic"
MEDIA_DIR = os.path.expanduser("~/Library/Application Support/Anki2/User 1/collection.media")
ANKICONNECT_URL = "http://127.0.0.1:8765"  # Using IP address instead of localhost

# API Configuration
RIME_API_KEY = os.getenv('RIME_API_KEY')
RIME_API_URL = "https://users.rime.ai/v1/rime-tts"
APIFY_TOKEN = os.getenv('APIFY_TOKEN')

def test_anki_connect():
    """Test AnkiConnect connection"""
    try:
        response = requests.post(ANKICONNECT_URL, json={
            "action": "version",
            "version": 6
        })
        result = response.json()
        print(f"AnkiConnect version: {result.get('result', 'Unknown')}")
        return True
    except Exception as e:
        print(f"AnkiConnect connection test failed: {str(e)}")
        print("Please ensure:")
        print("1. Anki is open")
        print("2. AnkiConnect plugin is installed")
        print("3. AnkiConnect plugin is enabled")
        return False

def generate_audio(text, output_file):
    """Generate audio file using Rime API"""
    if os.path.exists(output_file):
        print(f"Audio file already exists, skipping: {output_file}")
        return True

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {RIME_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "speaker": "Cove",
        "text": text,
        "modelId": "mistv2",
        "lang": "eng",
        "audioFormat": "mp3",
        "samplingRate": 22050,
        "speedAlpha": 1.0,
        "reduceLatency": False
    }
    
    try:
        response = requests.request("POST", RIME_API_URL, json=data, headers=headers)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "audioContent" in result:
                audio_data = base64.b64decode(result["audioContent"])
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"Audio file generated: {output_file}")
                return True
            else:
                print(f"API returned invalid data format: {result}")
                return False
        else:
            print(f"API request failed: {response.status_code}")
            print(f"Error message: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return False

def fetch_image(query, output_file):
    """Fetch image using APIFY"""
    if os.path.exists(output_file):
        print(f"Image file already exists, skipping: {output_file}")
        return True
        
    try:
        # Initialize Apify client
        client = ApifyClient(APIFY_TOKEN)
        
        # Prepare Actor input
        run_input = {
            "queries": [query],
            "maxResultsPerQuery": 10
        }
        
        print(f"Starting to fetch image: {query}")
        # Run Actor and wait for completion
        run = client.actor("tnudF2IxzORPhg4r8").call(run_input=run_input)
        
        # Wait and retry up to 3 times
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            # Get results
            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
            if not items:
                print(f"Waiting for image results... (attempt {retry_count + 1}/{max_retries})")
                time.sleep(5)  # Wait 5 seconds before retrying
                retry_count += 1
                continue
                
            print(f"Found {len(items)} results")
            for item in items:
                if "imageUrl" in item:
                    try:
                        # Download image
                        response = requests.get(item["imageUrl"], timeout=10)
                        if response.status_code == 200:
                            with open(output_file, "wb") as f:
                                f.write(response.content)
                            print(f"Image saved: {output_file}")
                            return True
                    except Exception as e:
                        print(f"Failed to download image, trying next one: {str(e)}")
                        continue
                    
            retry_count += 1
            if retry_count < max_retries:
                print(f"No suitable image found, retrying... (attempt {retry_count + 1}/{max_retries})")
                time.sleep(5)
                
        print(f"No suitable image found for: {query}")
        return False
        
    except Exception as e:
        print(f"Error fetching image: {str(e)}")
        return False

def add_notes_to_anki(notes):
    """Add notes to Anki in batch"""
    try:
        # First ensure deck exists
        response = requests.post(ANKICONNECT_URL, json={
            "action": "createDeck",
            "version": 6,
            "params": {
                "deck": ANKI_DECK
            }
        })
        
        if response.status_code != 200:
            print(f"Failed to create deck: {response.text}")
            return False
            
        # Add notes
        response = requests.post(ANKICONNECT_URL, json={
            "action": "addNotes",
            "version": 6,
            "params": {
                "notes": notes
            }
        })
        
        if response.status_code == 200:
            result = response.json()
            if "error" not in result:
                print(f"Successfully added {len(notes)} notes")
                return True
            else:
                print(f"Error adding notes: {result['error']}")
        else:
            print(f"Failed to add notes: {response.text}")
            
    except Exception as e:
        print(f"Error adding notes: {str(e)}")
    return False

def main():
    if not test_anki_connect():
        sys.exit(1)

    try:
        # Read CSV file
        df = pd.read_csv("Test.csv")
        print(f"Successfully read CSV file, {len(df)} rows")

        notes = []
        for _, row in df.iterrows():
            # Generate audio file
            audio_file = os.path.join(MEDIA_DIR, f"{row['Front']}.mp3")
            generate_audio(row['Front'], audio_file)
            
            # Fetch image
            image_file = os.path.join(MEDIA_DIR, f"{row['Front']}.jpg")
            fetch_image(row['Front'], image_file)
            
            # Prepare note
            note = {
                "deckName": ANKI_DECK,
                "modelName": ANKI_MODEL,
                "fields": {
                    "Front": row['Front'],
                    "Back": f"{row['Meaning']}<br><br>" \
                           f"Example: {row['Example']}<br><br>" \
                           f"Chinese: {row['Chinese Meaning']}<br><br>" \
                           f"Synonyms: {row['Synonyms']}<br><br>" \
                           f"Etymology: {row['Etymology']}<br><br>" \
                           f"Fun Fact: {row['Fun Fact']}<br><br>" \
                           f"[sound:{row['Front']}.mp3]<br>" \
                           f'<img src="{row["Front"]}.jpg">'
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": ["English"]
            }
            notes.append(note)
            
        # Add notes in batches of 10
        batch_size = 10
        for i in range(0, len(notes), batch_size):
            batch = notes[i:i + batch_size]
            if add_notes_to_anki(batch):
                print(f"Successfully added notes {i+1} to {i+len(batch)}")
                # Add a small delay between batches to avoid overwhelming Anki
                if i + batch_size < len(notes):
                    time.sleep(1)
                
        print("Processing complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
