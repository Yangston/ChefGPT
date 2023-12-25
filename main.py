import base64
import requests
import gradio as gr
import numpy as np
from PIL import Image
from io import BytesIO

# OpenAI API Key
api_key = "sk-"

# ChatBot Gaslighting
messages = [{"role": "system",
             "content": "You are a masterchef that is here to suggest excellent cooking recipes"}]

# Default Prompt
default_prompt = "This is my fridge. Analyze the contents carefully, and suggest a recipe I could make"

# Function to encode the image


def encode_image(image):
    if isinstance(image, np.ndarray):
        # Convert NumPy array to PIL Image
        image = Image.fromarray(image.astype('uint8'))

    with BytesIO() as output:
        image.save(output, format="JPEG")
        return base64.b64encode(output.getvalue()).decode('utf-8')


# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Function to create payload based on selected cuisine


def imageInput(image, cuisine):
    base64_image = encode_image(image) if image is not None else None

    # Customize prompt based on the selected cuisine
    prompt = f"This is my fridge. Analyze the contents carefully, and suggest a {cuisine} recipe I could make"

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}" if base64_image else None
                        }
                    }
                ]
            }
        ],
        "max_tokens": 3000
    }
    return payload

# ChatGPT Function


def ChatGPT(image, Chinese, Western, Italian, Korean, Japanese):
    if Chinese:
        selected_cuisine = ["Chinese"]
    elif Western:
        selected_cuisine = ["Western"]
    elif Italian:
        selected_cuisine = ["Italian"]
    elif Korean:
        selected_cuisine = ["Korean"]
    elif Japanese:
        selected_cuisine = ["Japanese"]
    else:
        selected_cuisine = ["General"]

    payload = imageInput(image, ", ".join(selected_cuisine))

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    reply = response.json()['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": reply})

    return reply


# Gradio Interface Setup
webapp = gr.Interface(
    fn=ChatGPT,
    inputs=[
        "image",
        gr.Checkbox("Chinese"),
        gr.Checkbox("Western"),
        gr.Checkbox("Italian"),
        gr.Checkbox("Korean"),
        gr.Checkbox("Japanese")
    ],
    outputs="text",
    title="ChefGPT"
)

# Launch the Gradio Interface
webapp.launch(share=True)
