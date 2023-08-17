import gradio as gr
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def user(user_message, history):
    return "", history + [[user_message, None]]

def bot(history):
    input_messages = [entry[0] for entry in history if entry[1] is None]
    generated_responses = [entry[1] for entry in history if entry[1] is not None]

    response = query({
        "inputs": {
            "past_user_inputs": input_messages,
            "generated_responses": generated_responses,
            "text": input_messages[-1] if input_messages else ""
        },
    })


    bot_message = response["generated_text"]
    history[-1][1] = bot_message

    

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch(debug=True, share=True)

