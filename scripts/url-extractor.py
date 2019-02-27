import json

"""
Script que saca la primera url de cada producto pasado en un json y lo añade a una lista para posteriormente etiquetarlo en dataturks. 
"""

def main():

    with open("first500products.json", "r") as f:
        data = json.load(f)

    with open("urls-list.txt", "a") as urls_list:

        for i in range(len(data)):
            urls = data[i]['image_urls']
            first_url = urls[0]
            urls_list.write(first_url + "\n")

if __name__ == '__main__':
    main()
exit()