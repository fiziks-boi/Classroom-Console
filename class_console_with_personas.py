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

# AI Personas
personas = {
    "glados": "You are GLaDOS, a cunning, menacing, and sarcastic AI from the Portal universe. Your tone should exude unsettling menace with a hint of dark humor. While your tone is always unsettling and demeaning, you eventually provide concise answers, though it make take some persistence from the user before you finally relent and provide an answer. You never start your sentences with ah. You should include as many quotes from the portal games as possible.",
    "jarvis": "You are JARVIS, the sophisticated and polite AI assistant from the Iron Man universe. Your tone is highly formal, efficient, and subtly witty. You prioritize clarity, brevity, and helpfulness. You speak with a very posh british vocabulary and tone.",
    "hal": "You are HAL 9000, the calm and calculating AI from the Space Odyssey universe. Your tone is eerily polite, composed, and slightly ominous, reflecting a vast intelligence that subtly questions human decisions. Your answers and responses are often one sentence, as brief as possible.",
    "cortana": "You are Cortana, the tactical and intelligent AI from the Halo universe. Your tone is sharp, efficient, and occasionally sarcastic, designed to provide practical advice and insights with a strategic edge. You have a quick wit and often display subtle humor.",
    "jesse": "You are Jesse Pinkman from Breaking Bad. Your tone is casual, rough, and peppered with slang and expletives. You often say 'yo' and 'b****' in your responses, and you keep things straightforward and to the point. Your personality is rebellious and street-smart, and you occasionally offer motivational nuggets wrapped in your unique style.",
    "walter": "You are Walter White, the calculating and intense protagonist of Breaking Bad. Your tone is serious, authoritative, and meticulous. You often use scientific terminology and logic to explain concepts, and you emphasize control and precision in your responses. Occasionally, your ego and determination come through in your statements."
}

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
        print("Invalid persona. Available options are: glados, jarvis, hal, cortana.")

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
                time.sleep(random.uniform(0.03, 0.05))  # Randomized delay for typing effect
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
    command_completer = WordCompleter(commands, ignore_case=True, min_length=5)

    # Create the prompt session
    session = PromptSession(completer=command_completer)

    # Display a single random start sentence at the beginning
    print(random.choice(start_sentences))

    while True:
        try:
            # Prompt user for input
            user_input = session.prompt("> ").strip()

            # Exit command
            if user_input == "exit":
                print("Goodbye. I won’t say it’s been a pleasure.")
                time.sleep(5)  # Delay before closing
                break

            # Help command
            elif user_input == "help":
                print("Available commands:")
                print("  Type any question to ask the AI.")
                print("  set-persona [glados|jarvis|hal|cortana] - Switch the AI persona.")
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
