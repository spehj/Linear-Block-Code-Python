from itertools import product
from operator import xor
import numpy as np
import math
import sys



class BlockCode:
    "Linear block code"

    def __init__(self, M) -> None:
        self.m = M


def xorOfArr(arr):
    xor_arr = 0

    for i in range(len(arr)):
        xor_arr = xor_arr ^ arr[i]

    return xor_arr


def calcXor(dependable_arr, x_arr):
    result_xor = 0
    for i in range(len(dependable_arr)):
        result_xor = result_xor ^ dependable_arr[i]*x_arr[i]
    return result_xor


def kodneZamenjave(H, D, m_d):

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
            X[ind_str][ind_x]=int(x)
    
    return X



def izpisNapak(M, n, k):
    res = 0
    results = []
    e_s = 0
    # Stevilo kodnih zamenjav num_kod
    num_kod = len(M)

    # n je dolzina kodnih zamenjav (n=k+m)
    # e je stevilo napak, ki jih lahko dekodiramo
    # Izracunamo argmax Hammingovega pogoja
    i= 0
    for e in range(num_kod):
        e_s += math.comb(n, i)
        i+=1
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

def izracunajKodne(X, H):
    M = []
    for index, x in enumerate(X):
        rez = np.matmul(H, x) %2
        if np.amax(rez) == 0:
            M.append(x)
    
    M = np.array(M)
    
    return M



    


def odkrivajPopravi(M, H):
    while True:
        print(f"\nProgram za odkrivanje in popravljanje enkratnih napak. Uporabite q+enter za izhod.")
        zaporedje_bitov = input(
            f"Vnesi poljubno zaporedje binarnih simbolov (dolzina = {len(M[0])} bitov):\n ")

        if zaporedje_bitov == "q":
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

    m = 3
    e = 1

    # Izracunaj n
    for i in range(m, ):
        pass





    # TODO
    # Izpiši vse kodne zamenjave

    # Izpiši kolikokratne napake je sposoben popravljati

    # Sprejemaj poljubno zaporedje binarnih simbolov (dolzina kot so kodne zamenjave)
    # Popravljaj napake v vhodnem zaporedju
    # Izpisi veljavne kodne zamenjave


