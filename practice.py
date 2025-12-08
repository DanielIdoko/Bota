from google import genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)
    
def main():
     while True:
        user_input = input('You: ')
        
        # Check for exit conditions
        if user_input.lower() in ['quit', 'exit']:
            print("Ending chat session.")
            break
        
        if not user_input.strip():
            continue # Skip empty inputs

        try:
            # 4. Send the prompt to the model and print the response
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=user_input
            )
            print(f"AI: {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")



if __name__ == "__main__":
    main()



