# Import necessary libraries
from google.cloud import vision
from dotenv import load_dotenv
import os

load_dotenv()

client = vision.ImageAnnotatorClient(client_options={"api_key": "AIzaSyAMq8RXMS3WD-UMRiWLMUOstAIN65SjsSI"})

with open("download.png", "rb") as image_file:
        content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

print("Texts:")
print(texts[0].description)