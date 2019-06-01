import re

"""
Script usado para arreglar el JSON generado por dataturks apra su correcto funcionamiento.
"""

def main():

    with open("../outputs/1K-Male-Female-Dataturks-FACE.json", "r") as f:
        s = f.read()
    res = re.sub("\}\n\{", "},{", s)
    f.close()
    
    final = "[" + res + "]"

    output = open("1K-Male-Female-Dataturks-FACE-fixed.json","w+")
    output.write(final)
    output.close()


if __name__ == '__main__':
    main()
exit()
