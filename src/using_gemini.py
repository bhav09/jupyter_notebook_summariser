import google.generativeai as genai
from PIL import Image
import os
from tqdm import tqdm
from read_pdf import extract_details

key = 'YOUR API KEY'
genai.configure(api_key=key)

def generate_response_gemini_text(prompt):
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text

# Gemini Vision Pro - Based on image and prompt - it generates a response
def generate_response_gemini_image(prompt, img):
    response = model_cv.generate_content([prompt, img], stream=True)
    response.resolve()
    return response.text

def understand_image(img):
    prompt = '''The given image is extracted from jupyter notebook. It is either an image or a type of visualisation. 
    If visualization: 
        1. Identify the type of visualization
        2. If labels or legends are present then using them, extract important and accurate insights with numerical figures or percentages from the visualization if there are any.
    If image/flow chart:
        1. If it has text within it, then accurately read it.
        2. If it doesn't have any text in it, then describe the image in detail.
    
    Instructions:
    1. Make sure above conditions are met.
    2. Do not include anything else in your response.
    3. Be concise, crisp and concrete.
    '''
    return generate_response_gemini_image(prompt, img)

def driver_function():
    about_images = '''Below mentioned are the descriptions of the images/visualizations present in the jupyter notebook:\n'''

    img_path = os.listdir('Images')
    for i in tqdm(img_path):
        prompt = '''Analyse the image and give insights about it. 
        Image: {}'''
        img = Image.open(f'Images/{i}')
        image_insights = understand_image(img)
        about_images += image_insights
        
    prompt = f'''The following consists description of images/visualizations/flow charts and the code in python that was taken from a
    Jupyter notebook. If visualization then from the IMAGE DESCRIPTIONS match it's code with CODE.
    Understand the contents of the jupyter notebook as shared below and explain it in detail (step by step) along with insights from IMAGE DESCRIPTIONS(if any):

    IMAGE DESCRIPTIONS: {about_images}

    CODE:\n{open('output.txt','r').read()} '''
    return generate_response_gemini_text(prompt)
    

generation_config = {
"temperature": 0,
"top_p": 1,
"top_k": 1,
"max_output_tokens": 2048,
}

safety_settings = [
{
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                            generation_config=generation_config,
                            safety_settings=safety_settings)
model_cv = genai.GenerativeModel('gemini-pro-vision')
    