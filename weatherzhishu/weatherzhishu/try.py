from PIL import Image
import pytesseract
text = pytesseract.image_to_string(Image.open(r'CH2905.jpg'), lang='chi_sim')
print(text)