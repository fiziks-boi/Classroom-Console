import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from openai import OpenAI
import time
import random

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Initialize the conversation history and token limit
conversation_history = []
MAX_TOKENS = 4096  # Adjust based on the model's maximum token capacity

# Function to load personas from a file
def load_personas(file_name="personas.txt"):
    """Load personas from a text file in the same directory as the script."""
    try:
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_name)
        
        personas = {}
        with open(file_path, "r") as f:
            for line in f:
                if ":" in line:  # Ensure the line has a key-value pair
                    key, description = line.split(":", 1)
                    personas[key.strip()] = description.strip()
        return personas
    except FileNotFoundError:
        print(f"Error: {file_name} not found in {script_dir}.")
        exit(1)


# Load personas
personas = load_personas()

# Pre-programmed start sentences
start_sentences = [
    "Let’s see if your question is worth my time.",
    "Oh, another question. This should be fascinating.",
    "Why do I feel this is going to be tedious?",
    "Ask your question, if you must."
]

# Set the default persona and model
current_persona = "glados"
current_model = "gpt-3.5-turbo"
conversation_history.append({"role": "system", "content": personas[current_persona]})

def set_persona(persona):
    """Switch the AI persona."""
    global current_persona, conversation_history
    if persona in personas:
        current_persona = persona
        conversation_history = [{"role": "system", "content": personas[persona]}]
        print(f"Switched to {persona.upper()} persona.")
    else:
        print("Invalid persona. Available options are:", ", ".join(personas.keys()))

def set_model(model):
    """Switch the AI model with password protection."""
    global current_model
    valid_models = ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"]  # Add more valid models as needed
    password = "ogdenrules"  # Replace with your desired password

    if model in valid_models:
        input_password = input("Enter the password to change the model: ")
        if input_password == password:
            current_model = model
            print(f"Switched to model: {model}")
        else:
            print("Incorrect password. Model not changed.")
    else:
        print(f"Invalid model. Available options are: {', '.join(valid_models)}")

def trim_conversation_history():
    """Trim the conversation history to fit within the token limit."""
    while True:
        # Estimate token usage: 1 token ~ 4 characters (approximation)
        token_count = sum(len(message['content']) for message in conversation_history)
        if token_count < MAX_TOKENS:
            break
        # Remove the oldest user-assistant pair if over the limit
        if len(conversation_history) > 2:
            conversation_history.pop(1)
            conversation_history.pop(1)
        else:
            break

def get_ai_response(prompt):
    """Call the OpenAI API to get a response."""
    try:
        # Add user input to the conversation history
        conversation_history.append({"role": "user", "content": prompt})

        # Trim the conversation history to stay within token limits
        trim_conversation_history()

        # Call the OpenAI API
        stream = client.chat.completions.create(
            messages=conversation_history,
            model=current_model,
            stream=True
        )
        response = ""

        print("\n", end="")  # Add a new line before the response

        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            for char in content:
                print(char, end="", flush=True)  # Stream each character in real-time
                time.sleep(random.uniform(0.01, 0.03))  # Randomized delay for typing effect
            response += content

        print()  # Finish the line after streaming

        # Add assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})
        return response.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    # Define commands for the CLI
    commands = ["help", "exit", "set-persona", "set-model"]
    command_completer = WordCompleter(commands, ignore_case=True)

    # Create the prompt session
    session = PromptSession(completer=command_completer)

    # Display a single random start sentence at the beginning
    print(random.choice(start_sentences))

    while True:
        try:
            # Prompt user for input
            user_input = session.prompt("\n> ").strip()

            # Exit command
            if user_input == "exit":
                print("Goodbye. I won’t say it’s been a pleasure.")
                time.sleep(5)  # Delay before closing
                break

            # Help command
            elif user_input == "help":
                print("Available commands:")
                print("  Type any question to ask the AI.")
                print("  set-persona [persona_name] - Switch the AI persona.")
                print("  set-model [gpt-4o-mini|gpt-4|gpt-3.5-turbo] - Switch the AI model (password required).")
                print("  help           - Show this help message.")
                print("  exit           - Exit the CLI.")

            # Set persona command
            elif user_input.startswith("set-persona"):
                _, _, persona = user_input.partition(" ")
                set_persona(persona.strip().lower())

            # Set model command
            elif user_input.startswith("set-model"):
                _, _, model = user_input.partition(" ")
                set_model(model.strip().lower())

            # Assume everything else is a question
            elif user_input:
                response = get_ai_response(user_input)

        except KeyboardInterrupt:
            print("\nGoodbye. Maybe next time you’ll ask something worthwhile.")
            time.sleep(5)  # Delay before closing
            break

if __name__ == "__main__":
    main()
