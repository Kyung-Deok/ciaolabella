from PIL import Image
import pytesseract
import io


def ecopointtwo(image):

    img_pil = Image.open(io.BytesIO(image.read()))
    img_pytesseract = pytesseract.image_to_string(img_pil, lang='kor+eng').replace(' ', '')

    return img_pytesseract


