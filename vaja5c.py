from itertools import product
from typing import final
import numpy as np
import math
import sys


def generiraj_binarne(n):
    """
    Generiraj binarne nize z n-znakov. Funkcija kot vhod sprejme dolzino binarnega
    niza in vrne seznam binarnih nizov dolocene dolzine n v obliki seznama seznamov.
    """
    bin_str = [''.join(p) for p in product('10', repeat=n)]

    bin_str.reverse()

    # Pretvori posamezen string v seznam
    X = [list(x) for x in bin_str]

    for ind_str, x_str in enumerate(X):
        for ind_x, x in enumerate(x_str):
            X[ind_str][ind_x] = int(x)

    return X


def izpis_napak(M, n):
    """
    Funkcija kot argument sprejme matriko vseh možnih kodnih zamenjav M in dolzino kodnih zamenjav n ter
    vrne maksimalno stevilo odkritih in popravljenih napak na izhodu.
    """
    res = 0
    results = []
    e_s = 0

    # Stevilo kodnih zamenjav num_kod
    num_kod = len(M)

    # Izracunamo argmax Hammingovega pogoja
    i = 0
    for e in range(num_kod):
        e_s += math.comb(n, i)
        i += 1

        res = (2**n)/e_s

        if res >= num_kod:
            results.append(e)
        elif res < num_kod:
            break
    
    e_max = np.argmax(np.array(results))

    return e_max


def izracunaj_kodne(X, H):
    """
    Funkcija kot argument sprejme matriko vseh binarnih kodov X in matriko za preverjanje sodosti H ter vrne 
    matriko vseh možnih kodnih zamenjav M.
    """

    M = []
    for index, x in enumerate(X):
        # Matricno mnozenje z vsakim izmed vektorjev v X
        rez = np.matmul(H, x) % 2
        # Iscemo rezultat v obliki npr. [0,0,0]
        if np.amax(rez) == 0:
            M.append(x)

    M = np.array(M)

    return M


def odkrivaj_popravi(M, H):
    """
    Funkcija kot argument sprejme matriko vseh možnih kodnih zamenjav M in matriko za preverjanje sodosti H. 
    Uporabnik v neskončni zanki vnaša kodne nize, funkcija pa detektira napako in jo odpravi.
    """
    print(f"\nProgram za odkrivanje in popravljanje enkratnih napak.")
    print(f"Uporabite q+enter za izhod.")
    print(f"Vnesite poljubno zaporedje binarnih simbolov (dolzina = {len(M[0])} bitov)\n")

    # Neskoncna zanka, kjer uporabnik vnasa nize binarnih simbolov
    while True:

        zaporedje_bitov = input(
            f"\nVhodno zaporedje: ")

        if zaporedje_bitov == "q":
            print()
            break
        elif len(zaporedje_bitov) == len(M[0]):

            # Pretvori niz v array
            arr = list(zaporedje_bitov)
            arr = [int(x) for x in arr]

            # Preveri ali so vnesene samo 0 in 1
            check_input = all((el==1 or el == 0) for el in arr)

            if check_input:

                arr = np.array(arr)
                arr_stari = arr.copy()

                # Izracunamo produkt po modulu 2
                rez = np.matmul(H, arr) % 2
                #print(f"Rezultat (za niz {zaporedje_bitov}): {rez}")
                if np.amax(rez) == 0:
                    print(f"Niz {zaporedje_bitov} je ze veljavna kodna zamenjava.")
                else:
                    h = []
                    # Odkrij napako
                    # Zapisi H stolpce v listo arrayev
                    for col in range(H.shape[1]):
                        h.append(H[:, col])

                    # Spremeni listo arrayev v listo list
                    h = [x.tolist() for x in h]

                    # Popravi napako
                    # Poisci ce se sindrom pojavi med H stolpci
                    if rez.tolist() in h:
                        rez_list = rez.tolist()
                        # Poiscemo na katerem indexu pride do napake
                        err_index = h.index(rez_list)
                        # Popravimo napako
                        arr[err_index] = not int(zaporedje_bitov[err_index])

                        # Izpisi veljavno zamenjavo
                        print(f"\nZaporedje bitov:\t{arr_stari}")
                        print(f"Popravljeno na:\t\t{arr}")
            else:
                print(
                f"***** NAPAKA: Napacni znaki v vhodnem nizu. Pojavila se je stevilka razlicna od 0 in 1. *****\n")

        elif len(zaporedje_bitov) != len(M[0]):
            print(
                f"***** NAPAKA: Napacna dolzina. Vnesli ste niz dolzine: {len(zaporedje_bitov)} *****\n")


def create_H(n_max):
    """
    Funkcija kot vhod sprejme dolzino kodnih zamenjav in na izhodu vrne matriko za preverjanje sodosti Hammingovega koda za odpravljanje vseh
    enkratnih napak.
    """
    n_list = []
    for n in range(1, n_max+1):
        n_list.append(n)

    n_list_bin = []

    for dec_num in n_list:
        bin_num = bin(dec_num)[2:]
        n_list_bin.append(bin_num)

    bin_places = len(n_list_bin[-1])

    final_bin_list = []
    for bin_str in n_list_bin:
        if len(bin_str) < bin_places:
            bin_str = (bin_places-len(bin_str))*"0" + str(bin_str)
        final_bin_list.append(bin_str)
    # print(final_bin_list)
    h_matrix = np.zeros((len(final_bin_list[0]), len(final_bin_list)))
    # zapisi vrstice v stolpce
    for ind_i, final_str in enumerate(final_bin_list):
        for ind_j, final_char in enumerate(final_str):
            # print(final_char)
            h_matrix[ind_j][ind_i] = final_char
    # print(h_matrix)
    return h_matrix


if __name__ == "__main__":
    try:
        # Pass the file name, number of iterations and learning rate as an arguments
        ctrl_bits = sys.argv[1]
    except IndexError:
        print("Usage of the script: python vaja5c.py <number of control bits>")
        sys.exit(1)

    # m = stevilo kontrolnih dvojiskih znakov
    # k = dolzina informacijskih blokov
    # n = dolzina kodnih zamenjav (n>k)

    # Stevilo kontrolnih bitov koda
    m = int(ctrl_bits)
    n = 2**m - 1  # matrix dimension if m>=2
    k = n - m

    # Izdelaj matriko vseh binarnih nizov dolzine n
    X = generiraj_binarne(n)
    # Tvori matriko H
    H = create_H(n)
    # Izracunaj vse mozne kodne zamenjave
    M = izracunaj_kodne(X, H)
    print("\nVse mozne kodne zamenjave:\n")
    print(M)

    # Izpisi kolikokratne napake je program sposoben popravljati
    e = izpis_napak(M, n)
    print(
        f"\nProgram je sposoben popravljati se vse {e}-kratne napake (e_max={e}).")
    print("\n"+40*"-")

    # Funkcija za odkrivanje in popravljanje napak
    odkrivaj_popravi(M, H)
