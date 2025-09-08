# story_scripter.py
# A Hyper-MVP for the Nano Banana 48 Hour Challenge by Google DeepMind.
# This script demonstrates multi-turn, context-aware image editing with character consistency.

import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import google.generativeai as genai

# --- CONFIGURATION ---
# 1. Place your starting image in the same folder as this script.
# 2. Create a file named ".env" in this folder and add your API key:
#    GEMINI_API_KEY='YOUR_API_KEY_HERE'

# Load the API key from the.env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "API key not found. Please create a.env file and add your GEMINI_API_KEY."
    )

# Configure the Gemini client
genai.configure(api_key=API_KEY)
client = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest"
)  # Using a stable model name for robustness

# --- USER INPUTS ---
# Define the path to your starting image
STARTING_IMAGE_PATH = "start_image.png"

# --- FIX IS HERE: More direct and command-like prompts ---
# By explicitly telling the model to "Edit" or "Generate", we prevent it from
# just describing the scene in text.
PROMPT_SEQUENCE = [
    "**Edit the provided image.** Generate a new photorealistic, high-detail photo that places this exact character in a sunny, futuristic city.",
    "**Modify the image.** Now, change the time of day to night. Make sure neon lights from the city reflect realistically on the character's armor.",
    "**Alter the image again.** Make it start to rain heavily. Add visible raindrops in the air and make all surfaces look wet.",
    "**For the final image, edit it to show** the character looking up at a giant, glowing holographic banana sign in the sky. The sign must say the word 'NANO'.",
]


# Define the output directory
OUTPUT_DIR = "story_output"


# --- CORE LOGIC ---
def main():
    """
    Main function to run the StoryScripter AI narrative generation process.
    """
    print("--- Starting StoryScripter AI ---")

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # 1. Load the initial image
    try:
        current_image = Image.open(STARTING_IMAGE_PATH)
        print(f"Successfully loaded starting image: {STARTING_IMAGE_PATH}")
    except FileNotFoundError:
        print(
            f"ERROR: Starting image not found at '{STARTING_IMAGE_PATH}'. Please check the filename."
        )
        return

    # 2. Loop through the prompt sequence
    for i, prompt in enumerate(PROMPT_SEQUENCE):
        step_number = i + 1
        print(f"\n--- Applying Step {step_number}/{len(PROMPT_SEQUENCE)} ---")
        print(f'Prompt: "{prompt}"')

        try:
            # The core API call
            response = client.generate_content(
                [prompt, current_image],
                generation_config=genai.types.GenerationConfig(),
            )

            # Check if the response contains text instead of an image.
            if hasattr(response.parts[0], "text"):
                print(
                    f"API returned a text response instead of an image for Step {step_number}:"
                )
                print(f"--- API MESSAGE ---")
                print(response.parts[0].text)
                print(f"--------------------")
                print("Aborting sequence due to API error/rejection.")
                break  # Stop the loop

            # If we get here, the response should be an image.
            generated_image_data = response.parts[0].inline_data.data

            # Create a new PIL Image object from the raw image data
            new_image = Image.open(BytesIO(generated_image_data))

            # Save the newly generated image
            output_filename = f"step_{step_number:02d}_output.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            new_image.save(output_path)

            print(f"Successfully generated and saved: {output_path}")

            # Set the new image as the input for the next iteration
            current_image = new_image

        except Exception as e:
            print(f"An error occurred during API call for Step {step_number}: {e}")
            print(
                "This could be due to an invalid API key, quota limits, or an unexpected script error."
            )
            print("Aborting sequence.")
            break

    print("\n--- StoryScripter AI sequence complete! ---")
    print(f"Check the '{OUTPUT_DIR}' folder for your generated images.")


if __name__ == "__main__":
    main()
