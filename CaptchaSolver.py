import cv2
from pytesseract import pytesseract

CAPTCHA_IMAGE_FOLDER = "captcha_to_solve"
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def process_image(image_path):
    print(image_path)
    img = cv2.imread(image_path)
    # smoothing the image
    img = cv2.medianBlur(img, 5)
    cv2.imwrite('output.png', img)

    # Load the image and convert it to grayscale
    image = cv2.imread('output.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Add some extra padding around the image
    image = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_REPLICATE)

    # threshold the image (convert it to pure black and white)
    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imwrite('output1.png', thresh.copy())
    # print letters with pytesseract
    print(pytesseract.image_to_string(cv2.imread('output1.png')))
    # print letters with pytesseract
    return pytesseract.image_to_string(thresh.copy())
