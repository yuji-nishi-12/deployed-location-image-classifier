import streamlit as st
import torch
from torchvision.transforms import transforms
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from model import ImageClassifier

st.title("Location Image Classifier...")
st.text("Provide URL of Location Image for image classification")

classes = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']

@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ImageClassifier(num_classes=len(classes))
    model.load_state_dict(torch.load("/app/models/image_intel_model_0.pth", map_location=device))
    model.eval()
    return model, device

with st.spinner("Loading model..."):
    model, device = load_model()

def process_img(image):
    transform = transforms.Compose([
        transforms.Resize((150, 150)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(BytesIO(image)).convert("RGB")
    return transform(image).unsqueeze(0).to(device)

default_url = "https://storage.googleapis.com/image_classication_2026/Glacier-Argentina-South-America-blue-ice.JPEG"
path = st.text_input("Enter image URL to classify:", default_url)

if path:
    try:
        response = requests.get(path)
        content = response.content

        st.write("# Predicted Class:")
        with st.spinner("Classifying image..."):
            img_tensor = process_img(content)

            with torch.inference_mode():
                output = model(img_tensor)
                prob = torch.softmax(output, dim=1)
                label_index = torch.argmax(prob, dim=1).item()
                confidence = prob[0][label_index].item()

            st.success(f"{classes[label_index].upper()} (Confidence: {confidence:.2f})")

        image = Image.open(BytesIO(content))
        st.image(image, caption='Input Image')

    except Exception as e:
        st.error(f"Error processing image: {e}")