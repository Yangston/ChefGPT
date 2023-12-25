import base64
import requests
import gradio
import numpy as np
from PIL import Image
from io import BytesIO

# OpenAI API Key
api_key = "sk-"

# ChatBot Gaslighting
messages = [{"role": "system",
             "content": "You are a masterchef that is here to suggest excellent cooking recipes"}]

# Prompt
prompt = "This is my fridge. Analyze the contents carefully, and suggest a recipe I could make."

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

# Payload


def imageInput(image):
    base64_image = encode_image(image) if image is not None else None


def imageInput(image):
    base64_image = encode_image(image) if image is not None else None

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


def ChatGPT(image):
    payload = imageInput(image)

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    reply = response.json()['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": reply})

    return reply


# Gradio Interface Setup
webapp = gradio.Interface(
    fn=ChatGPT,
    inputs="image",
    outputs="text",
    title="ChefGPT"
)

# Launch the Gradio Interface
webapp.launch(share=True)
