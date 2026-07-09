import easyocr
reader = easyocr.Reader(['en'])

def extract_text_from_image(image):
    uploaded_file = image.read()
    result = reader.readtext(uploaded_file,detail=0)
    text = "\n".join(result)
    return text