import cv2
from pytesseract import pytesseract

path_to_tesseract = r"C:\Users\Navata\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract


img = cv2.imread("ucmflyer3.jpg")

def extract(img):
    text = pytesseract.image_to_string(img)
    return text

def grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def denoise(img):
    return cv2.medianBlur(img,5)

def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

img = grayscale(img)
img = thresholding(img)
img = denoise(img)

#cv2.imshow('img',img)
#cv2.waitKey(0)

#print(extract(img))
with open('output.txt', 'w') as f:
    f.write(extract(img))