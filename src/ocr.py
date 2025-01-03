from PIL import Image
import pytesseract

image_path = 'resources/ocr.png'

text = pytesseract.image_to_string(Image.open(image_path), lang='eng')

print("Extracted Text:")
print(text)
