import subprocess
import ollama

# --- CONFIGURATION ---
# The local AI model you want to use (e.g., 'llama3', 'phi3', 'mistral')
# Make sure you have pulled it with 'ollama pull <model_name>'
AI_MODEL = 'phi3' 
# ---------------------

def get_staged_changes() -> str:
    """
    Gets the changes staged for commit using 'git diff --staged'.
    Returns the diff as a string or an empty string if there's an error or no changes.
    """
    try:
        # The '--' is a good practice to separate flags from file paths
        result = subprocess.run(
            ["git", "diff", "--staged", "--"],
            capture_output=True,
            text=True,
            check=True # This will raise a CalledProcessError if git returns a non-zero exit code
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: 'git' command not found. Is Git installed and in your PATH?")
        return ""
    except subprocess.CalledProcessError:
        # This can happen if the command fails for other reasons, but for 'diff', it's usually fine
        print("No staged changes found. Use 'git add' to stage your files.")
        return ""

def generate_commit_message(diff: str) -> str:
    """
    Uses a local LLM via Ollama to generate a commit message based on the diff.
    """
    if not diff.strip():
        return "No changes to generate a message for."

    # This prompt is designed to guide the AI to give a high-quality commit message
    prompt = f"""
    Based on the following 'git diff', please generate a concise and professional commit message.
    The message must follow the Conventional Commits specification.
    The format should be: <type>[optional scope]: <description>
    
    Common types include: feat, fix, docs, style, refactor, test, chore.
    
    The description should be in the present tense, e.g., "add feature" not "added feature".
    Do not include any explanations, just the raw commit message itself.

    Diff:
    ---
    {diff}
    ---
    """
    
    try:
        print(f"🤖 Contacting model '{AI_MODEL}' to generate commit message...")
        response = ollama.chat(
            model=AI_MODEL,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        # This will catch errors if Ollama isn't running or the model isn't found
        return f"Error generating message: {e}\nIs the Ollama server running and the model '{AI_MODEL}' pulled?"

def main():
    """
    Main function to orchestrate getting the diff and generating the message.
    """
    staged_diff = get_staged_changes()
    
    if staged_diff:
        commit_message = generate_commit_message(staged_diff)
        print("\n--- Suggested Commit Message ---")
        print(commit_message)
        print("------------------------------\n")
        
        # Ask the user if they want to use this message
        # use_it = input("Do you want to use this message for your commit? (y/n): ").lower()
        # if use_it == 'y':
        #     subprocess.run(["git", "commit", "-m", commit_message])
        #     print("✅ Commit created successfully.")

if __name__ == "__main__":
    main()
