import easyocr

def extract_text_from_image(image):
    reader = easyocr.Reader(['en'])

    result = reader.readtext(image,detail=0)
    text = "/n".join(result)
    return text