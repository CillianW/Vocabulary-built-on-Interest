// Load API keys from environment variables (injected by server)
const API_KEY = window.GEMINI_API_KEY;
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent';

let generatedWords = [];

document.getElementById('generate-btn').addEventListener('click', generateWords);
document.getElementById('create-anki-btn').addEventListener('click', createAnkiCSV);

// Add event listeners for topic buttons
document.querySelectorAll('.topic-btn').forEach(button => {
    button.addEventListener('click', () => {
        const topic = button.getAttribute('data-topic');
        document.getElementById('topic').value = topic;
        generateWords();
    });
});

async function generateWords() {
    const topic = document.getElementById('topic').value.trim();
    if (!topic) {
        alert('Please enter a topic');
        return;
    }

    // Show loading
    document.querySelector('.loading').style.display = 'block';
    document.querySelector('.results-section').style.display = 'none';

    try {
        const prompt = `Generate a list of 15 English words related to the topic "${topic}". 
            Format the response as a JSON array of objects, where each object has these properties:
            word, meaning, example, chinese_meaning, synonyms, etymology, fun_fact.
            
            Return ONLY the JSON array, no other text. Example format:
            [
                {
                    "word": "example",
                    "meaning": "a thing characteristic of its kind",
                    "example": "This is an example sentence.",
                    "chinese_meaning": "example",
                    "synonyms": "instance, sample",
                    "etymology": "from Latin exemplum",
                    "fun_fact": "Used since the 15th century"
                }
            ]`;

        console.log('Sending request to Gemini API...');
        const response = await fetch(GEMINI_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-goog-api-key': API_KEY
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: prompt
                    }]
                }],
                safetySettings: [{
                    category: "HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold: "BLOCK_NONE"
                }]
            })
        });

        console.log('Response received');
        const data = await response.json();
        console.log('API Response:', data);

        if (!data.candidates || !data.candidates[0] || !data.candidates[0].content || !data.candidates[0].content.parts || !data.candidates[0].content.parts[0].text) {
            throw new Error('Invalid response format from API: ' + JSON.stringify(data));
        }

        const content = data.candidates[0].content.parts[0].text;
        console.log('Raw content:', content);
        
        // Try to find and extract JSON from the response
        let jsonMatch = content.match(/\[[\s\S]*\]/);
        if (!jsonMatch) {
            throw new Error('No JSON array found in response');
        }

        // Parse the JSON response
        try {
            generatedWords = JSON.parse(jsonMatch[0]);
            console.log('Parsed words:', generatedWords);
        } catch (parseError) {
            console.error('JSON Parse Error:', parseError);
            throw new Error('Failed to parse JSON response');
        }
        
        // Display words
        displayWords(generatedWords);
        
        // Show results section
        document.querySelector('.loading').style.display = 'none';
        document.querySelector('.results-section').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + error.message + '\nCheck console for details.');
        document.querySelector('.loading').style.display = 'none';
    }
}

function displayWords(words) {
    const container = document.getElementById('words-container');
    container.innerHTML = '';
    
    words.forEach(word => {
        const wordElement = document.createElement('div');
        wordElement.className = 'word-item';
        wordElement.textContent = word.word;
        wordElement.title = `${word.meaning}\n\n${word.chinese_meaning}`;
        container.appendChild(wordElement);
    });
}

async function createAnkiCSV() {
    if (!generatedWords.length) {
        alert('Please generate words first');
        return;
    }

    try {
        // First save the CSV file
        const csvContent = [
            ['Front', 'Meaning', 'Example', 'Chinese Meaning', 'Synonyms', 'Etymology', 'Fun Fact', 'Audio', 'Image'].join(','),
            ...generatedWords.map(word => {
                const front = word.word;
                return [
                    front,
                    word.meaning,
                    word.example,
                    word.chinese_meaning,
                    word.synonyms,
                    word.etymology,
                    word.fun_fact,
                    `[sound:${front}.mp3]`,
                    `${front}.jpg`
                ].map(field => `"${(field || '').replace(/"/g, '""')}"`).join(',');
            })
        ].join('\n');

        // Save CSV file
        const saveResponse = await fetch('/save-csv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                csv_content: csvContent
            })
        });

        if (!saveResponse.ok) {
            throw new Error('Failed to save CSV file');
        }

        // Show saving message
        alert('CSV file saved! Please wait while we process the words...');

        // Wait for 3 seconds
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Run the Python script
        const runResponse = await fetch('/run-script', {
            method: 'POST'
        });

        if (!runResponse.ok) {
            const error = await runResponse.text();
            throw new Error('Failed to run Python script: ' + error);
        }

        const result = await runResponse.json();
        if (result.errors) {
            console.error('Script errors:', result.errors);
        }
        
        alert('Words have been successfully processed and added to Anki!');
    } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    }
} 