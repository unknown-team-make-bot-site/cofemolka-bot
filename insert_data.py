import json
import string
import os

from models.tables. type_dish_table import TypeDish
from models.tables.menu_table import MenuTable

types = {
    1:  "coffee",

    2:  "eat_something",

    3:  "deserts",

    4:  "tea",

    5:  "milkshakes",

    6:  "other"
}

data = ["data/coffee.json", "data/deserts.json", "data/eat_something.json",
        "data/other.json", "data/tea.json", "data/milkshakes.json","data/dish_types.json"]

def insert_data(name):
    if ("types" in name):
        with open(name, encoding="utf-8", errors="ignore") as json_file:
            data = json.load(json_file)
            for types in data:
                TypeDish.add_types(**types)
    else:
        with open(name, encoding="utf-8", errors="ignore") as json_file:
            data = json.load(json_file)
            for coffee in data:
                MenuTable.add_dishes(**coffee)


def add_type(id, filename):
    with open(filename, encoding="utf-8", errors="ignore") as json_file:
        data = json.load(json_file)
        for content in data:
            content["type_id"] = id
        return json.dumps(data, indent=6, ensure_ascii=False)

def add_one_image(image, filename):
    with open(filename, encoding="utf-8", errors="ignore") as json_file:
        data = json.load(json_file)
        for content in data:
            content["image"] = image
        return json.dumps(data, indent=6, ensure_ascii=False)

# to get full path of file_name os.path.join(dirpath, name).
def add_images(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for dirname in dirnames:
            for (dirpath, dirnames, filenames) in os.walk(f"{path}\{dirname}"):
                if (dirname.lower() in types.values()):
                    for file in data:
                        with open(file, encoding="utf-8", errors="ignore") as json_file:
                            contents = json.load(json_file)
                            for content in contents:
                                for name in filenames:
                                    product_name = os.path.splitext(name)[0]
                                    if product_name.lower() in content['name'].lower():
                                        content['image'] = name
                                print(json.dumps(contents, indent=6, ensure_ascii=False))
                            write_content(f"processing_data/{file}", json.dumps(contents, indent=6, ensure_ascii=False))


'''
'a' is mode that is short for "appending"
if something add/delete to file then need to use the mode
'''

def delete_content(filename):
    file = open(filename, "a")
    file.seek(0)
    file.truncate(0)
    file.close()

def write_content(filename, text):
    file = open(filename, "a+", encoding="utf-8")
    file.write(text)
    file.close()


#print(add_images("product_images"))
#print(add_type(1, coffee))

for name in data:
    insert_data(name)

'''
for content in data:
    insert_data(content)
MenuTable.get_dishes()
TypeDish.get_types()

algorithm for adding images:

walking through directories 
if dir_name == "any type":
    go to directory
    for content in json_file:
        walking trough filenames
            if filename in content['name']:
                content['image'] = filename
                

problems with generating gson with images:
1. some images cannot have name like 'Орех/шоколад'
    it is reason why any images does not adding to json file
    image name != content['name']
2. generate a lot of unnecessary dictionaries without adding images inside json-files
    how to write only one dictionary that needed? 
'''

