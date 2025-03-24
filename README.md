<img width="911" alt=" Remember Words Tailored to Your" src="https://github.com/user-attachments/assets/8d4e8fd6-b11f-42bc-a464-370b52aba2d3" />

<img width="1065" alt="image" src="https://github.com/user-attachments/assets/15e713fe-2d4c-4ac8-921e-10f986cd35f1" />


# Doyouremember - Your Personal Vocabulary Assistant

A web application that helps you learn new vocabulary by generating word cards with meanings, examples, audio pronunciations, and images, then automatically adding them to Anki.

## Features

- Generate vocabulary words based on any topic
- Each word card includes:
  - Definition
  - Example sentence
  - Chinese translation
  - Synonyms
  - Etymology
  - Fun fact
  - Audio pronunciation
  - Related image

## Prerequisites

1. Python 3.11 or higher
2. Anki with AnkiConnect add-on installed
3. API keys for:
   - Google Gemini API
   - Rime TTS API
   - Apify

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Doyouremember.git
cd Doyouremember
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Then edit `.env` and add your API keys.

## Anki Setup

1. Install Anki from https://apps.ankiweb.net/
2. Install the AnkiConnect add-on:
   - Open Anki
   - Go to Tools > Add-ons > Get Add-ons
   - Enter code: `2055492159`
   - Restart Anki

3. Configure AnkiConnect:
   - Go to Tools > Add-ons > AnkiConnect > Config
   - Replace the configuration with:
```json
{
    "apiKey": null,
    "apiLogPath": null,
    "ignoreOriginList": [],
    "webBindAddress": "127.0.0.1",
    "webBindPort": 8765,
    "webCorsOriginList": [
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:8765",
        "http://localhost:8765",
        "https://127.0.0.1",
        "https://localhost",
        "https://127.0.0.1:8765",
        "https://localhost:8765",
        "*"
    ]
}
```

## Usage

1. Start Anki and keep it running in the background
2. Start the web server:
```bash
python server.py
```
3. Open your browser and visit http://localhost:8000
4. Enter a topic and click "Generate Words"
5. Click "Add to Anki" to create flashcards

## License

This project is licensed under the Non-Commercial Public License (NCPL). This means:

✅ You can:
- Use this software for personal purposes
- Modify the software
- Share the software with others
- Contribute to the project

❌ You cannot:
- Use this software for commercial purposes
- Sell this software or any modifications of it
- Remove or modify this license notice

All API keys and services used in this project require separate licenses and terms of service agreements. 


