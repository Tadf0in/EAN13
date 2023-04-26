"""
TPE - Codes-barres & QR Codes
"""

import turtle as t

def inverse(bits:str) -> str:
    """ Inverse chaque bit, les 1 deviennent des 0 et inversement
    In : bits (str)
    Out: out (str)
    """
    out = bits
    out = out.replace('0', '2')
    out = out.replace('1', '0')
    out = out.replace('2', '1')
    return out

# Set A de la partie gauche
gauche_pair = [
    '0001101',
    '0011001',
    '0010011',
    '0111101',
    '0100011',
    '0110001',
    '0101111',
    '0111011',
    '0110111',
    '0001011',
    ]

# Set B de la partie gauche
gauche_impair = [
    '0100111',
    '0110011',
    '0011011',
    '0100001',
    '0011101',
    '0111001',
    '0000101',
    '0010001',
    '0001001',
    '0010111',
    ]

# Set C, partie droite (= set A inversé)
droite = [inverse(bits) for bits in gauche_pair]

# On regroupe les sets dans un dico
parite = {'A': gauche_pair, 'B': gauche_impair, 'C': droite}

# On déterminera quels sets utiliser grâce à ce tableau et au préfixe du code
table_parite = [
    'AAAAA',
    'ABABB',
    'ABBAB',
    'ABBBA',
    'BAABB',
    'BBAAB',
    'BBBAA',
    'BABAB',
    'BABBA',
    'BBABA',
]


def codage(prefixe:int, num:int, position:int) -> str:
    """ Encode la numéro
    In : prefixe (int) : 1er chiffre du code barre
         num (int) : chiffre à encoder
         position (int) : position du chiffre à encoder > 0
    Out: (str) : série de 7 bits correspondant au numéro encodé
    """
    if position == 1:
        set = 'A'

    # Partie gauche
    elif position < 7:
        set = table_parite[prefixe][position - 2]

    # Partie droite
    else:
        set = 'C'
    
    # On retourne alors la bonne série de 7 bits
    return parite[set][num] 


def modulo_check(num):
    """ Calcule le chiffre de vérification
    In : num (str) : 12 chiffres
    Out: (int) : Check digit
    """
    out = 0

    for i, e in enumerate(num):
        if i % 2 == 0:
            out += int(e)
        else:
            out += 3*int(e)

    ten = 10
    while out > ten:
        ten += 10
    return ten - out


def codebarre(num:str) -> str:
    """ Génére le codebarre correspondant au numéro
    In : num (str) : 12 chiffres
    Out: code (str) : chaîne remplie de 1 et de 0 (95 bits)
    """
    # Caractère de début
    code = '101'

    # Préfixe
    prefixe = num[0]

    # Partie gauche
    for i, n in enumerate(num[1:7]):
        code += codage(int(prefixe), int(n), int(i+1))

    # Séparateur central
    code += '01010'
    
    # Partie droite
    for n in num[7:]:
        code += droite[int(n)]
    
    # Chiffre de vérification
    code += droite[modulo_check(num)]
    
    # Caractère de fin
    code += '101'

    return code


def dessine(code:str) -> None:
    """ Dessine le codebarre à l'aide du module turtle
    In : code (str) : série de 95 bits
    """
    # Initialisation du stylo
    t.hideturtle()
    t.speed(200)
    t.pensize(5)
    t.pu()
    t.goto(-220, 100)
    t.pd()

    haut = True
    for i, bit in enumerate(code):

        # Si Caractère de début, de milieu ou de fin alors trait plus long
        if i in [0,1,2, 45,46,47,48,49, 92,93,94]:
            taille = 230
        else:
            taille = 200

        # Si c'est un 1 alors on fait un trait noir, sinon rien on laisse blanc
        if bit == '1':
            t.setheading(-90)
            t.fd(taille)
            t.fd(-taille)
        
        # On décale de 5 vers la droite
        t.pu()
        t.setheading(0)
        t.fd(5)
        t.pd()


if __name__ == '__main__':
    num = input("Entrez un numéro à 12 chiffres : ")
    while len(num) != 12:
        print("Ce numéro n'a pas 12 chiffres")
        num = input("Entrez un numéro à 12 chiffres : ")

    check_digit = modulo_check(num)
    print("Check digit : ", check_digit)

    code = codebarre(num)
    print(code)

    dessine(code)

    # Eciture sous le code
    t.pu()
    t.goto(-245, -140)
    t.pd()

    anum = num[0] + '   ' 
    for e in num[1:7]:
        anum += e + '  '
    anum += '  '
    for e in num[7:]:
        anum += e + '  '
    anum += str(check_digit)

    t.write(anum, font=("Arial", 25, "normal"))


    t.exitonclick()
