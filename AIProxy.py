import os, httpx, json
#openai_api_base = os.getenv("OPENAI_API_BASE", "https://aiproxy.sanand.workers.dev/openai/v1")
#openai_api_base  = "https://api.openai.com/v1" # for testing
openai_api_base = "https://aiproxy.sanand.workers.dev/openai/v1"

openai_api_key = os.getenv("AIPROXY_TOKEN", "no-key")

headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json",
}

def get_completions(messages):
    #print(messages)
    #print(f"openai_api_base: {openai_api_base}")
    with httpx.Client(timeout=20) as client:
        response = client.post(
            f"{openai_api_base}/chat/completions",
            headers=headers,
            json=
                {"model": "gpt-4o-mini", 
                 "messages": messages
                },
        )
    return response.json()["choices"][0]["message"]["content"]

def get_tool_completions(json_data):
    #print(messages)
    #print(f"openai_api_base: {openai_api_base}")
    with httpx.Client(timeout=20) as client:
        response = client.post(
            f"{openai_api_base}/chat/completions",
            headers=headers,
            json= json_data
        )
    #print(response.json()["choices"][0]["message"]["tool_calls"][0]["function"])
    return response.json()["choices"][0]["message"]["tool_calls"][0]["function"]

def get_embeddings(input):
    with httpx.Client(timeout=20) as client:
        response = client.post(
            f"{openai_api_base}/embeddings",
            headers={"Authorization": f"Bearer {openai_api_key}"},
            json={"model": "text-embedding-3-small", "input": input},
        )
    return response.json()["data"]