from itertools import product
from typing import final
import numpy as np
import math
import sys


class BlockCode:
    "Linear block code"

    def __init__(self, M) -> None:
        self.m = M


def kodne_zamenjave(H, D, m_d):

    z = []
    # Izdelamo seznam s stolpci od m-tega naprej
    for ind, j in enumerate(H):
        z.append(j[m:])
    z = np.array(z)

    # Izracunamo matriko E prvih m vrednosti
    E = np.zeros((m_d, m))
    for i, x in enumerate(D):
        # Za x4, x5, x6 in x7 izberemo poljubne dvojiske vrednosti
        for l in range(m):
            # we calculate first m elements
            E[i][l] = calcXor(z[l], x)
    # Vse zamenjave dobimo tako, da zdruzimo matriki E in D
    M = np.concatenate((E, D), axis=1)

    # Test: should return [0,0,0]
    # for element in M:
    #     ele = np.matmul(H, element) %2

    return M


def generiraj_binarne(n):
    """
    generiraj binarne nize z n-znakov.
    """
    bin_str = [''.join(p) for p in product('10', repeat=n)]

    bin_str.reverse()

    X = [list(x) for x in bin_str]

    for ind_str, x_str in enumerate(X):
        for ind_x, x in enumerate(x_str):
            X[ind_str][ind_x] = int(x)

    return X


def izpis_napak(M, n, k):
    res = 0
    results = []
    e_s = 0
    # Stevilo kodnih zamenjav num_kod
    num_kod = len(M)

    # n je dolzina kodnih zamenjav (n=k+m)
    # e je stevilo napak, ki jih lahko dekodiramo
    # Izracunamo argmax Hammingovega pogoja
    i = 0
    for e in range(num_kod):
        e_s += math.comb(n, i)
        i += 1
        #print(f"Suma e({e}): {e_s}")

        res = (2**n)/e_s
        #print(f"Rez e({e}): {res}")

        if res >= num_kod:
            results.append(e)
        elif res < num_kod:
            break

    print(results)
    e_max = np.argmax(np.array(results))

    return e_max


def izracunaj_kodne(X, H):
    M = []
    for index, x in enumerate(X):
        rez = np.matmul(H, x) % 2
        if np.amax(rez) == 0:
            M.append(x)

    M = np.array(M)

    return M


def odkrivaj_popravi(M, H):
    print(f"\nProgram za odkrivanje in popravljanje enkratnih napak.")
    print(f"Uporabite q+enter za izhod.\n")
    while True:
        
        zaporedje_bitov = input(
            f"Vnesite poljubno zaporedje binarnih simbolov (dolzina = {len(M[0])} bitov):\n ")

        if zaporedje_bitov == "q":
            print()
            break
        elif len(zaporedje_bitov) == len(M[0]):

            # string to array
            arr = list(zaporedje_bitov)
            arr = [int(x) for x in arr]
            arr = np.array(arr)
            arr_stari = arr.copy()

            # for i in arr:
            #     if i != "0" or i != "1":
            #         continue

            # Izracunamo produkt po modulu 2
            rez = np.matmul(H, arr) % 2
            #print(f"Rezultat (za niz {zaporedje_bitov}): {rez}")
            if np.amax(rez) == 0:
                print(f"Niz {zaporedje_bitov} je ze veljavna kodna zamenjava.")
            else:
                h = []
                # odkrij napako
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

        elif len(zaporedje_bitov) != len(M[0]):
            print(
                f"Napacna dolzina. Vnesli ste niz dolzine: {len(zaporedje_bitov)}\n")

def decimal_to_bin(num):
    if num >= 1:
        decimal_to_bin(num // 2)
    return num%2


def create_H(n_max):
    n_list = []
    for n in range(1, n_max+1):
        n_list.append(n)

    n_list_bin = []
    #bin_places = len(n_list[-1])

    for dec_num in n_list:
        bin_num = bin(dec_num)[2:]
        n_list_bin.append(bin_num)

    bin_places = len(n_list_bin[-1])

    final_bin_list = []
    for bin_str in n_list_bin:
        if len(bin_str) < bin_places:
            bin_str = (bin_places-len(bin_str))*"0" + str(bin_str)
        final_bin_list.append(bin_str)
    #print(final_bin_list)
    h_matrix = np.zeros((len(final_bin_list[0]), len(final_bin_list)))
    # zapisi vrstice v stolpce
    for ind_i, final_str in enumerate(final_bin_list):
        for ind_j, final_char in enumerate(final_str):
            #print(final_char)
            h_matrix[ind_j][ind_i] = final_char
    #print(h_matrix)
    return h_matrix


if __name__ == "__main__":
    try:
        # Pass the file name, number of iterations and learning rate as an arguments
        ctrl_bits = sys.argv[1]
    except IndexError:
        print("Usage of the script: python vaja5c.py <number of control bits>")
        sys.exit(1)

    print(ctrl_bits)

    # m = stevilo kontrolnih dvojiskih znakov
    # k = dolzina informacijskih blokov
    # n = dolzina kodnih zamenjav (n>k)

    # m = stevilo vrstic v H
    # n = stevilo stolpcev v H
    # k = n-m
    # n = k+m

    # TODO
    # Program sam tvori matriko za preverjanje sodosti Hammingovega koda za odpravljanje vseh enkratnih napak
    # Vhod v program je število kontrolnih bitov

    m = int(ctrl_bits)
    n = 2**m - 1 # matrix dimension if m>=2
    k = n -m
    
    X = generiraj_binarne(n)
    H = create_H(n)
    M = izracunaj_kodne(X, H)
    print("\nVse mozne kodne zamenjave:\n")
    print(M)
    e = izpis_napak(M, n, k)
    print(
        f"\nProgram je sposoben popravljati se vse {e}-kratne napake (e_max={e}).")
    print("\n"+40*"-")

    odkrivaj_popravi(M,H)




    # TODO
    # Izpiši vse kodne zamenjave

    # Izpiši kolikokratne napake je sposoben popravljati

    # Sprejemaj poljubno zaporedje binarnih simbolov (dolzina kot so kodne zamenjave)
    # Popravljaj napake v vhodnem zaporedju
    # Izpisi veljavne kodne zamenjave
