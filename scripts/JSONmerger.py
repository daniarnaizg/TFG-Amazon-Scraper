import json
from copy import deepcopy

"""
Scripts que hace un merge de dos archivos JSON usando el campo URL como elemento común.
"""

def main():

    new_dict = {}

    with open("../outputs/first500products.json", "r") as f:
        fdata = json.load(f)

    for i in range(len(fdata)):
        fdict = {}
        fdict['ASIN'] = fdata[i]['asin']
        fdict['RATING'] = fdata[i]["rating"]
        fdict['URL'] = fdata[i]["image_urls"][0]
        new_dict[i] = fdict

    with open("first500tagged.json", "r") as j:
        jdata = json.load(j)

    dictcopy = deepcopy(new_dict)

    for i in range(len(jdata)):
        url = jdata[i]['content']
        label = jdata[i]["annotation"]["labels"][0]
        for key, value in dictcopy.items():
            for n, v in value.items(): 
                if url in v:
                    new_dict[i]['LABEL'] = label
    
    f.close()
    j.close()

    with open('first500final.json', 'w') as fp:
        json.dump(new_dict, fp)

if __name__ == '__main__':
    main()
exit()
