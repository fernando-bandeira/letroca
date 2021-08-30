from banco import palavras
from msvcrt import getwch, kbhit
from os import name, system
from random import choice, shuffle
from unicodedata import normalize
from time import sleep


def limpa_tela():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def remove_acentos(x):
    x = normalize('NFD', x)
    x = x.encode('ascii', 'ignore')
    x = x.decode('utf-8')
    return x


def cenario(n):
    limpa_tela()
    print('-descubra o máximo de palavras possíveis com essas letras')
    print('-pressione ENTER para recombinar as letras')
    print('-insira * para finalizar e ver as respostas', end='\n\n')
    print('palavras restantes', f'({n}):')


while True:
    min = 4
    max = 8
    while True:
        original = choice(palavras)
        n = len(original)
        if n >= min and n <= max:
            break
    base = remove_acentos(original)
    letras = [letra.upper() for letra in base]
    shuffle(letras)
    possib_orig = []
    for palavra in palavras:
        apta = True
        for letra in palavra:
            letra = remove_acentos(letra)
            palav = remove_acentos(palavra)
            if letra not in base or palav.count(letra) > base.count(letra):
                apta = False
                break
        if apta:
            possib_orig.append(palavra)
    possib = [remove_acentos(p) for p in possib_orig]
    acertos, lista, parcial, errou = [], [], [], False
    while True:
        qtd = {n: [] for n in range(3, max + 1)}
        for palavra in possib:
            qtd[len(palavra)].append(palavra)
        cenario(len(possib))
        if len(parcial) > 0:
            letras_atuais = []
            for letra in set(letras):
                n = letras.count(letra) - parcial.count(letra.lower())
                for _ in range(n):
                    letras_atuais.append(letra)
        else:
            letras_atuais = letras.copy()
        t = [f'{q} letras: {len(qtd[q])}' for q in qtd.keys() if len(qtd[q])]
        print('\n' + ' ||| '.join(t))
        if len(acertos) > 0:
            print('\n' + f'acertos ({len(acertos)}):', ', '.join(acertos))
        if len(possib) == 0:
            break
        linha = '-' * (len(letras_atuais) * 2 - 1)
        print(linha)
        print(' '.join(letras_atuais))
        print(linha)
        if errou:
            print('-palavra não cadastrada!')
            errou = False
        print('digite: ')
        print(''.join(parcial))
        while True:
            if kbhit():
                entrada = getwch().lower()
                break
        if entrada == '\r' and len(parcial) > 0:
            entrada = ''.join(parcial)
            if '*' in entrada:
                break
            if entrada in lista:
                print('você já encontrou essa palavra!')
                sleep(2)
            else:
                if entrada in possib:
                    i = possib.index(entrada)
                    acertos.append(possib_orig[i])
                    possib.pop(i)
                    possib_orig.pop(i)
                    lista.append(entrada)
                else:
                    errou = True
            parcial.clear()
        else:
            cond1 = entrada.upper() in letras
            cond2 = parcial.count(entrada) < letras.count(entrada.upper())
            if (cond1 and cond2) or '*' in entrada:
                parcial.append(entrada)
            elif entrada == '\x08' and len(parcial) > 0:
                parcial.pop()
            elif entrada == '\r':
                shuffle(letras)
            entrada = ''

    if len(possib) == 0:
        print('\n' + 'você encontrou todas as palavras!')
    else:
        possib_orig.sort(key=len)
        print('\n' + 'palavras faltantes: ' + ', '.join(possib_orig) + '\n')
    comando = input('digite "s" para sair ou outro comando para reiniciar: ')
    if comando.strip().lower() == 's':
        break
