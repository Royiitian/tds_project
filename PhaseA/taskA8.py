import os, base64
import re

from AIProxy import get_completions

def execute_task(filename: str, targetfile: str) -> str:
    print(f"filename: {filename}, targetfile: {targetfile}")
    
    for i in range(3): # Retry once if no credit card number is detected, because OpenAI Vision may not be 100% accurate
        extracted_text = extract_text_from_image(filename)
        extracted_number = extract_credit_card_number(extracted_text, True)
        if extracted_number != "Retry":
            break
    
    if os.path.exists(targetfile):
        os.remove(targetfile)
        
    # Write the extracted number to the output file
    with open(targetfile, "w", encoding="utf-8") as f:
        f.write(extracted_number)

    print(f"Extracted credit card number: {extracted_number}")
    return f"Extracted credit card number: {extracted_number}"

# Read the image file and encode it as base64
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
# Extract text using OpenAI Vision model
def extract_text_from_image(image_path):
    image_data = encode_image(image_path)

    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all readable text from the image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ],
            }
        ]
    response = get_completions(messages)
    print(response)
    return response

def extract_credit_card_number(text, firstTry):
    """
    Extracts a 16-digit credit card number from the given OCR text using regex.
    Returns the number without spaces or dashes.
    """
    pattern = r'\b(?:\d[ -]*){15}\d\b'  # Matches 16-digit numbers with spaces/dashes
    match = re.search(pattern, text)
    if match:
        return re.sub(r'[^\d]', '', match.group())  # Remove non-digit characters
    elif firstTry:
        return "Retry"
    return "No credit card number detected"