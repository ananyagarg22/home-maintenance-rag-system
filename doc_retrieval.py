import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import base64
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.environ['API_KEY']

CHROMA_PATH = "chromadb"

PROMPT_TEMPLATE = """
Based on the following conversation history and contexts:

{history}

---

Answer this question: {question}
"""

# Initialize the conversation history
conversation_history = []

MAX_HISTORY_TOKENS = 4096

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
  
def decode_image(image):
    # Read the binary content from the FileStorage object
    image_binary = image.read()

    # Encode the image in base64
    base64_image = base64.b64encode(image_binary).decode('utf-8')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is broken or needs fixing in this image with focus on tasks that require handyman services?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/*;base64,{base64_image}"
                    }
                }
            ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # print(response.json()['choices'])
    # print(response.json().choices)
    return response.json()['choices'][0]['message']['content']

def summarize_text(text):
    # Use the OpenAI API to summarize text
    summarizer = ChatOpenAI(api_key=API_KEY, model="gpt-4o-mini")
    summary = summarizer.invoke(f"Summarize this conversation within {MAX_HISTORY_TOKENS} tokens: {text}").content
    return summary

def provide_ans(query_text, image=None):

    global conversation_history
    
    if image == None:
        image_meaning = ""
    else:
        image_meaning = decode_image(image)

    # print(f"Meaning of the image: {image_meaning}")

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(api_key=API_KEY)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    if len(image_meaning):
        results = db.similarity_search_with_relevance_scores(query_text+" and in my image "+image_meaning, k=3)
    else:
        results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0:
        print(f"Unable to find any matching results.")
        return
    elif results[0][1] < 0.5:
        print(f"Unable to find suitable matching results.")
        print(f"The results were {results}")
        return

    context_text = "\n\n---\n\n".join([f"\"{doc.page_content}\"\nScore:{_score}" for doc, _score in results])
    
    # Create the current conversation entry
    current_entry = f"Question: {query_text}\nContext: {context_text}"

    # Update history by appending the new exchange
    conversation_history.append(current_entry)

    # If the token count is too high, summarize the history
    total_tokens = sum(len(entry.split()) for entry in conversation_history)
    if total_tokens > MAX_HISTORY_TOKENS:
        summarized_history = summarize_text("\n\n".join(conversation_history[:-1]))
        conversation_history = [summarized_history, conversation_history[-1]]

    # Combine all history into one string
    history_text = "\n\n".join(conversation_history)
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(history=history_text, question=query_text)
    # print(prompt)

    model = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=API_KEY,
    )
    response_text = model.invoke(prompt).content

    # Append the response to the conversation history
    conversation_history.append(f"Response: {response_text}")

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    if __name__ == "__main__":
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print(formatted_response)
    return prompt, response_text, sources

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    provide_ans(query_text)

if __name__ == "__main__":
    main()