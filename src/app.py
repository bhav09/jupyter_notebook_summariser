import streamlit as st
from read_pdf import extract_details
from using_gemini import driver_function
import time
import shutil, os

st.title('Notebook Summarizer')
changes = '''
<style>
[data-testid = "stAppViewContainer"]
    {
    background-image:url('https://i.ibb.co/Rj46gPk/image.png');
    background-size:cover;
    }
    
    div.esravye2 > iframe {
        background-color: transparent;
    }
</style>
'''

st.markdown(changes, unsafe_allow_html=True)
st.write('Studies visualization and code to give accurate summary along with the insights from Jupyter Notebook')
file_upload = st.file_uploader('Choose a file', type=['pdf'])

summary_button = st.button('Summarize')
if summary_button:
    if file_upload:
        if os.path.exists('Images/'):
            shutil.rmtree('Images/')
        extract_details(file_upload)
        lines_of_code = len(open(f'output_{str(file_upload.name).split(".")[0]}.txt').readlines())
        total_images = len(os.listdir('Images'))
        st.markdown(f'''**Extraction results**\n
        Lines of code/text:  {lines_of_code}\n\tImages/visualizations:  {total_images} 
        ''')
        with st.spinner():
            response = driver_function()
            response = response.replace('*','')
            st.text_area('Code Summary',response, height= 250, label_visibility='collapsed')

    else: st.write('Please upload a file!')

