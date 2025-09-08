# StoryScripter AI 🎨

An AI-powered visual storyteller that uses the Gemini API to generate and sequentially edit images, creating a narrative from a single starting picture.

## Features

-   **Sequential Image Editing:** Takes a starting image and a series of text prompts.
-   **Story Generation:** Each prompt modifies the result of the previous step, creating a coherent visual story.
-   **Powered by Gemini:** Utilizes Google's `gemini-1.5-flash-latest` model for fast and high-quality image generation.
-   **Simple & Extendable:** A single, easy-to-understand Python script that can be customized.

## Setup & Installation

Follow these steps to get the project running on your local machine.

**1. Clone the repository:**
```bash
git clone [https://github.com/aayush-0131/story-scripter-ai.git](https://github.com/aayush-0131/story-scripter-ai.git)
cd story-scripter-ai
2. Install dependencies:
It's recommended to use a virtual environment.

Bash

# Create and activate a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install the required packages
pip install -r requirements.txt
3. Configure your API Key:
You will need a Gemini API key.

Create a file named .env in the root of the project directory.

Add your API key to this file:

GEMINI_API_KEY="YOUR_API_KEY_HERE"
This project uses python-dotenv to load the key, and the .env file is included in .gitignore to keep your key private.

Usage
Place your starting image in the root directory and name it start_image.png.

Modify the PROMPT_SEQUENCE list in the story_scripter.py file to tell your desired story.

Run the script from your terminal:

Bash

python story_scripter.py
Check the story_output/ folder for the generated images.
