import os

from AIProxy import get_completions

def execute_task(filename: str, targetfile: str) -> str:
    print(f"filename: {filename}, targetfile: {targetfile}")
    return extract_sender_email(filename, targetfile)

def extract_sender_email(input_file, output_file):
    """
    Reads an email from input_file, extracts the sender's email using an LLM, 
    and writes just the email address to output_file.
    """
    # Read the email content
    with open(input_file, "r", encoding="utf-8") as f:
        email_content = f.read()

    # Prompt LLM to extract sender's email
    prompt = f"""
    Extract only the sender's email address from the following email message. 
    Return only the email address, nothing else.
    
    Email message:
    {email_content}
    """

    response = get_completions([{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}])
    print(response)
    sender_email = response.strip()

    # Write the extracted email to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sender_email)

    print(f"Extracted sender email: {sender_email}")
    return f"Extracted sender email: {sender_email}"

