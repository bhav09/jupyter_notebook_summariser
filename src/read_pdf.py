import fitz
import os

def extract_details(filename):
    doc = fitz.open(filename)
    open(f'output.txt', 'w')

    # Iterate through the pages in the PDF file
    for page_num, page in enumerate(doc):

        text = f'PAGE {page_num+1}\n'

        # Extract the text from the page
        text += page.get_text()

        # Extract the images from the page
        images = page.get_images()

        # Save the text to a file
        
        with open(f'output.txt', 'a') as f:
            f.write(text)

    # Save each image to a separate PNG file
    if not os.path.exists('Images/'): 
        os.mkdir('Images/')
    for i, image in enumerate(images):
        xref = image[0]

        # extract the image bytes 
        
        base_image = doc.extract_image(xref)
        image_data = base_image["image"]

        # get the image extension 
        ext = base_image["ext"]
        # Generate unique filename based on page and image number
        img_file = f'Images/output_page_image{i + 1}.{ext}'
        
        # Save the image
        with open(img_file, 'wb') as f:
            f.write(image_data)

    # Close the PDF file
    doc.close()