import json
from pathlib import Path

# --- CONFIGURATION ---
JSON_FILE_PATH = Path("resume_data.json")
OUTPUT_MARKDOWN_PATH = Path("generated_resume.md")
# ---------------------

def generate_resume_md(resume_data: dict) -> str:
    """
    Generates the full resume content in Markdown format from a dictionary.
    """
    
    # --- Header with Personal Info ---
    name = resume_data.get("name", "Your Name")
    title = resume_data.get("title", "Your Title")
    contact = resume_data.get("contact", {})
    
    md_content = f"# {name}\n"
    md_content += f"## {title}\n\n"
    
    contact_info = []
    if "email" in contact:
        contact_info.append(f"**Email:** {contact['email']}")
    if "linkedin" in contact:
        contact_info.append(f"**LinkedIn:** {contact['linkedin']}")
    if "github" in contact:
        contact_info.append(f"**GitHub:** {contact['github']}")
    
    md_content += " | ".join(contact_info) + "\n\n"
    
    # --- Summary Section ---
    if "summary" in resume_data:
        md_content += f"## Summary\n"
        md_content += f"{resume_data['summary']}\n\n"

    # --- Work Experience Section ---
    md_content += "## Work Experience\n"
    for job in resume_data.get("experience", []):
        md_content += f"### {job.get('title')} at {job.get('company')}\n"
        md_content += f"*{job.get('dates')}*\n\n"
        for accomplishment in job.get("accomplishments", []):
            md_content += f"- {accomplishment}\n"
        md_content += "\n"
        
    # --- Skills Section ---
    if "skills" in resume_data:
        md_content += "## Skills\n"
        md_content += ", ".join(resume_data.get("skills", [])) + "\n"

    return md_content

def main():
    """
    Main function to read JSON data and write the Markdown resume.
    """
    if not JSON_FILE_PATH.exists():
        print(f"Error: The file '{JSON_FILE_PATH}' was not found.")
        print("Please create it based on the 'resume_example.json' structure.")
        return

    try:
        with JSON_FILE_PATH.open("r", encoding="utf-8") as f:
            cv_data = json.load(f)
        
        markdown_resume = generate_resume_md(cv_data)
        
        with OUTPUT_MARKDOWN_PATH.open("w", encoding="utf-8") as f:
            f.write(markdown_resume)
            
        print(f"✅ Resume successfully generated at '{OUTPUT_MARKDOWN_PATH}'")

    except json.JSONDecodeError:
        print(f"Error: The file '{JSON_FILE_PATH}' contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
