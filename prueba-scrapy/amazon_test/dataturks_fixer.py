import re

"""
Script usado para arreglar el JSON generado por dataturks apra su correcto funcionamiento.
"""

def main():

    with open("first500products_tagged_dataturks.json", "r") as f:
        s = f.read()
    res = re.sub("\}\n\{", "},{", s)
    f.close()
    
    final = "[" + res + "]"

    output = open("first500tagged.json","w+")
    output.write(final)
    output.close()


if __name__ == '__main__':
    main()
exit()
