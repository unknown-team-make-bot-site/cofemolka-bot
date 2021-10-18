from PIL import Image
import pytesseract
import cv2
import os
import json
import string
# url: https://www.severcart.ru/blog/all/tesseract_ocr_python/

pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract\\tesseract.exe'
preprocess = "thresh"
additional_letters = ['(', ')','/', ' ']

def process_text(name, cost_and_volume):
    json = []
    cur = ""
    json_dict = {}
    is_first = True
    for prev, current, next in zip(name, name[1:], name[2:]):
        if (current == " " and next == " "):
            continue
        elif (current.isalpha() or current in additional_letters or (current in additional_letters and prev == "\n")):
            if (is_first):
                cur += prev + current
                is_first = False
            else:
                cur += current
        elif (current == "\n" and cur != ""):
            if (prev not in additional_letters):
                json_dict["name"] = cur
                json.append(json_dict)
                json_dict = {}
                cur = ""

    cur = ""
    json2 = []
    json_dict = {}
    step = "cost"
    for el in cost_and_volume:
        if (el.isdigit()):
            cur += el
        elif (cur != ""):
            # if image have only cost
            json_dict["cost"] = int(cur)
            step = "volume"
            cur = ""
            json2.append(json_dict)
            json_dict = {}
            # if image have cost and volume
            '''
            if (step == "cost"):
                json_dict["cost"] = int(cur)
                step = "volume"
                cur = ""
            else:
                json_dict["volume"] = int(cur)
                step = "cost"
                cur = ""
                json2.append(json_dict)
                json_dict = {}
            '''
    json3 = []
    for dict, dict1 in zip(json, json2):
        json3.append(dict|dict1)
    return json3

def process_image(image):
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # перевести в градации серого
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


    filename = f"{os.getpid()}.png"
    cv2.imwrite(filename, gray)

    # преобразование из картинки в строку
    text = pytesseract.image_to_string(Image.open(filename), lang='rus')
    os.remove(filename)
    cv2.imshow("Image", image)
    cv2.imshow("Output", gray)
    return text



image = "images_for_json/menu2_cost.jpg"
image_1 = "images_for_json/menu2_names.png"
#print(process_image(image))
text_from_image = process_text(process_image(image_1), process_image(image))
print(json.dumps(text_from_image, indent=4, ensure_ascii=False))


# print(process_text(text))
'''
cur = ""
key_counter = 0
json_dict = {}
if index == 0:
    continue
elif index == text.length - 1:
    pass
elif element[index] is capital and element[index + 1] capital
    continue
elif element[index - 1] == \n && element[index + 1] is not capital
    if (key_counter => 1 and isDigit(element[index])):
        cur += element[index]
elif element[index] == " ":
    match key_counter:
        case(0):
            key_counter += 1
            json_dict['name'] = cur
            cur = ""
        case(1):
            key_counter += 1
            json_dict['cost'] = int(cur)
            cur = ""
        case(2):
            key_counter = 0
            json_dict['volume'] = int(cur)
            cur = ""
            
SO FUCK THIS. Just divide image into 2 pieces. Now algorithm will be:

add dish_name:

cur = ""
json_dict = {}
json = []
for element in text
    if element is \n then
        if (cur != "")
            json_dict['name'] = cur
            json.append(json_dict)
            json_dict = {}
            cur = ""
    if element == " " and element + 1 == " "
            continue
    else
        if isAlphabetical(element)
            cur += element
    
add cost and volume:

cur = ""
step = "cost"
json_dict = {}
json_array initialize yet
for element in text:
    if element is digital:
        cur += element
    else:
        if (step == "cost"):
            json_dict['cost'] = int(cur)
            step = "volume"
        else:
            json_dict['volume'] = int(cur)
            step = "cost"
            json_array.append(json_dict)
            json_dict = {}
     
'''
