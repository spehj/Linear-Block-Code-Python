import enum
from itertools import count
from operator import xor
from unittest import result
import numpy as np
import math


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


def kodneZamenjave(H, D):

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

def izpisNapak(M, n, k):
    res = 0
    results = []
    e_s = 0
    # Stevilo kodnih zamenjav num_kod
    num_kod = len(M)

    # n je dolzina kodnih zamenjav (n=k+m)
    # e je stevilo napak, ki jih lahko dekodiramo
    # Izracunamo argmax Hammingovega pogoja
    for e in range(num_kod):
        e_s += math.comb(n,e)
        #print(f"Suma e({e}): {e_s}")
        
        res = (2**n)/e_s
        
        if res >= num_kod:
            results.append(e)
        elif res < num_kod:
            break
    
    #print(results)
    e_max = np.argmax(np.array(results))
    
    return e_max



if __name__ == "__main__":

    H = [[1, 0, 0, 0, 1, 1, 1], [0, 1, 0, 1, 0, 1, 1], [0, 0, 1, 1, 1, 0, 1]]
    H = np.array(H)
    D = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [
        1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]
    D = np.array(D)
    # print(h)

    # m = stevilo kontrolnih dvojiskih znakov
    # k = dolzina informacijskih blokov
    # n = dolzina kodnih zamenjav (n>k)

    # m = stevilo vrstic v H
    # n = stevilo stolpcev v H
    # k = n-m

    # rows = m, columns = n
    m, n = H.shape
    m_d, n_d = D.shape
    k = n-m

    # TODO
    # Sestavite program, ki bo določil in izpisal vse možne kodne zamenjave M={xi}

    M = kodneZamenjave(H,D)
    
    print("\nVse mozne kodne zamenjave:\n")
    print(M)
    
    print("\n"+40*"-")

    # TODO
    # Izpiše naj še vse kolikokratne napake je s podano matriko sposoben poravljati

    e = izpisNapak(M, n, k)
    
    print(f"\nProgram je sposoben popravljati se vse {e}-kratne napake (e_max={e}).")
    print("\n"+40*"-")
    

    # TODO
    # Na vhodu sprejema na vhodu poljubno zaporedje binarnih simbolov, enake dolžine, kot so kodne zamenjave.
    while True:
        zaporedje_bitov = input(f"Vnesi poljubno zaporedje binarnih simbolov (dolzina = {len(M[0])}): \n")
        
        if zaporedje_bitov == "q":
            break
        elif len(zaporedje_bitov) == len(M[0]):
            print(f"Zaporedje bitov: {zaporedje_bitov}, type: {type(zaporedje_bitov)}")
            # string to array
            arr = list(zaporedje_bitov)
            arr = [int(x) for x in arr]
            arr = np.array(arr)
            
            # Izracunamo produkt po modulu 2
            rez = np.matmul(H, arr) %2
            print(f"Rezultat (za niz {zaporedje_bitov}): {rez}")
            if np.amax(rez)==0:
                print(f"Niz {zaporedje_bitov} je veljavna kodna zamenjava.")
            else:
                h = []
                # odkrij napako
                for col in range(H.shape[1]):
                    h.append(H[:, col])

                #print(h)
                h = [x.tolist() for x in h]
                #print(h)
                if rez.tolist() in h:
                    rez_list = rez.tolist()
                    #print(f"Found: {rez_list} : {h}")
                    err_index = h.index(rez_list)
                    print(f"Found in column: {(h.index(rez_list))+1}\n")
                    zap_list = zaporedje_bitov.tolist()
                    zap_list[err_index] = not int(zaporedje_bitov[err_index])
                    print(f"Zaporedje bitov: {zap_list}\n")
                # popravi napako

                # Izpisi veljavno zamenjavo
                pass


        elif len(zaporedje_bitov) != len(M[0]):
            print(f"Napacna dolzina. Vnesli ste niz dolzine: {len(zaporedje_bitov)}\n")
        

    # Sprejmi userjev input

    # Preveri ali je dolzine 8

    # Izracunaj H+x

    # Preveri ali so rezultat same 0


    # TODO
    # S pomočjo podane matrike za preverjanje sodosti odkriva in popravlja napake v vhodnem zaporedju in izpisuje na izhodu veljavne kodne zamenjave.


    
