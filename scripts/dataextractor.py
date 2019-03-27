import json, requests
from PIL import Image
from io import BytesIO

"""
Script que descarga imagenes dada su URL y las renombra en funcion de cómo han sido etiquetadas.
"""

def requestImg(image_name, url):
    r = requests.get(url)

    i = Image.open(BytesIO(r.content))
    i.save(image_name)
    # i.save("dataset/" + image_name)


def main():
    with open("../outputs/first500final.json", "r") as f:
        data = json.load(f)

    for i in range(len(data)):
        # url = data[i]['content']
        # label = data[0]["annotation"]["labels"][0]

        url = data[str(i)]['URL']
        label = data[str(i)]['LABEL']
        image_name = str(i) + "_" + label + ".jpg"
        requestImg(image_name, url)


if __name__ == '__main__':
    main()
exit()
