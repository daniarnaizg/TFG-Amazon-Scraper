import json, requests, os
from PIL import Image
from io import BytesIO

"""
Script que descarga imagenes dada su URL y las renombra en funcion de cómo han sido etiquetadas.
"""

def requestImg(image_name, url):
    r = requests.get(url)
    i = Image.open(BytesIO(r.content))
    
    if image_name[0] is 'C':
        i.save("D:\_TFG\TFG-Amazon-Scraper\datasets\dataset-cara/Cara/" + image_name)
    else:
        i.save("D:\_TFG\TFG-Amazon-Scraper\datasets\dataset-cara/SinCara/" + image_name)


def main():
    with open("../outputs/1K-Male-Female-Dataturks-FACE.json", "r") as f:
        data = json.load(f)

    for i in range(len(data) - 1):

        try:
            url = data[i]['content']
            label = data[i]['annotation']['labels'][0]
        except IndexError:
            print(str(i))

        image_name = label + '_' + str(i) + '.jpg'
        requestImg(image_name, url)


if __name__ == '__main__':
    main()
exit()
