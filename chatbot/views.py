from django.shortcuts import render
from django.http import HttpResponse
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from .forms import GeminiProVisionForm
import markdown2
# from io import BytesIO
import cv2
import numpy as np

# Loading the environment variables
load_dotenv()

# Access the environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key is provided
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

# Configuring the generativeai module with API key
genai.configure(api_key=api_key)

# Choosing the model
model_name = 'gemini-pro'

# Creating the generative_model object
model = genai.GenerativeModel(model_name=model_name)

def home(request):
    return render(request,'home.html')

# Function for text_based chatbot by using gemini-pro model.
def chat_text(request):
    if request.method == 'POST' or request.method == 'GET':
        user_input = request.POST.get('user_input', '')

        if user_input.lower() == "stop":
            response = "Goodbye!!"
        elif user_input:
            try:
                generated_text = model.generate_content(user_input,
                    generation_config={
                    "max_output_tokens": 4096,
                    "temperature": 0,
                    "top_p": 1,
                    "top_k": 32
                },).text

                response = generated_text
                response = response.replace("*","")
                response = markdown2.markdown(response)
            except Exception as e:
                response = "An error occurred. Please try again."
        else:
            response = ""

        return render(request, 'index.html', {'user_input': user_input, 'response': response})
    else:
        return HttpResponse("Method not allowed", status=405)


## Function for Image based chatbot by using gemini-pro vision model.
model_name1 = "gemini-pro-vision"

model1 = genai.GenerativeModel(model_name=model_name1)


# def open_image(file):
#     image_data = file.read()
#     image_array = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
#     return image_array

# def chat_image(request):
#     if request.method == "POST":
#         form = GeminiProVisionForm(request.POST, request.FILES)
#         if form.is_valid():
#             input_text = form.cleaned_data['input_text']
#             uploaded_image = request.FILES['image']

#             # Opening the image using OpenCV
#             image_array = open_image(uploaded_image)

#             if input_text != "":
#                 response = model1.generate_content([input_text, image_array])
#             else:
#                 response = model1.generate_content(image_array)

#             response = response.text

#             return render(request, 'result.html', {'response': response})
#     else:
#         form = GeminiProVisionForm()

#     return render(request, 'gemini.html', {'form': form})

        
def open_image(file):
    image_data = file.read()
    image_array = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    return image_array

def convert_to_pil(image_array):
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    
    # Create a PIL Image from the NumPy array
    pil_image = Image.fromarray(image_rgb)
    return pil_image

def chat_image(request):
    if request.method == "POST":
        form = GeminiProVisionForm(request.POST, request.FILES)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            uploaded_image = request.FILES['image']

            # Opening the image using OpenCV
            image_array = open_image(uploaded_image)
            
            pil_image = convert_to_pil(image_array)
        
            if input_text != "":
                response = model1.generate_content([input_text, pil_image])
            else:
                response = model1.generate_content(pil_image)

            response = response.text
            response= response.replace('*',"")

            return render(request, 'result.html', {'response': response})
    else:
        form = GeminiProVisionForm()

    return render(request, 'gemini.html', {'form': form})

    