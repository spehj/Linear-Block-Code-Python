import enum
from itertools import count
from operator import xor
import numpy as np
import math

class BlockCode:
    "Linear block code"


    def __init__(self, M) -> None:
        self.m = M


def xorOfArr(arr):
    xor_arr = 0

    for i in range(len(arr)):
        xor_arr = xor_arr ^arr[i]
    
    return xor_arr

def calcXor(dependable_arr, x_arr):
        result_xor=0
        for i in range(len(dependable_arr)):
            result_xor = result_xor ^ dependable_arr[i]*x_arr[i]
        return result_xor


if __name__ == "__main__":


    H = [[1,0,0,0,1,1,1],[0,1,0,1,0,1,1],[0,0,1,1,1,0,1]]
    H = np.array(H)
    D = [[0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,0,1],[0,1,1,0],[0,1,1,1],[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1],[1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]
    D=np.array(D)
    #print(h)

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

    x = np.zeros((1,3),)
    ab = np.zeros((1,3))

    c = np.linalg.solve(H,ab)
    print(c)
    print()
    print(D[0])
    np.reshape(H, (3,7))
    #x = np.matmul(H, np.transpose(D[0]))
    #M = np.zeros
    print(x)
    # for index_d, d in enumerate(D):
    #     x = np.matmul(np.linalg.inv(H), np.transpose(d))
    #     print(x)
    # Kodne zamenjave
    E = np.zeros((m_d, m))
    z = []
    for ind, j in enumerate(H):
        z.append(j[m:])
    
    z = np.array(z)
    #print(z)
    #print()
    for i,x in enumerate(D):
        for l in range(m):
            # we calculate first m elements
            E[i][l] = calcXor(z[l], x)

    # M is matrix of all possible codewords
    M = np.concatenate((E,D), axis=1)
    #print("Vse mozne kodne zamenjave:")
    #print(M)

    # Kolikokratne napake je sposoben popravljati
    counter_arr =[]
    for n_M in M:
        counter = 0
        for h in n_M:
            if h ==1:
                counter+=1
        counter_arr.append(counter)
    counter_arr.sort()
    counter_arr.remove(0)
    #print(counter_arr)
    d_min = counter_arr[0]

    # Error detection capability
    # d_min >= s+1
    s = d_min-1
    #print(f"Minimum distance: {d_min}")
    #print(f"Minimum distance: {s}")

    
    # How many error can we correct?
    # e_max = 0
    # e = 0
    # while True:
    #     if e == 0:
    #         e_popravek = 2*e+1
    #     else:
    #         e_max = 2*e
    #     e+=1

    #     if d_min >= e_max:
    #         break   
    #print(e_max)

    #print(math.comb(12,5))

    e_s = 0
    # Stevilo kodnih zamenjav num_kod
    num_kod = 16
    # n je dolzina kodnih zamenjav (n=k+m)
    for e in range(k):
        e_s += math.comb(e,n)
        print(f"Suma e({e}): {e_s}")
        if e_s != 0:
            res = (2**n)/e_s
        else:
            res = 0
        print(f"Res e({e}): {res}")
        
        if res<num_kod:
            break
    
    print(e)



    # # DELUJOCA
    # def izpisNapak(M, n, k):
    #     res = 0
    #     e_s = 0
    #     # Stevilo kodnih zamenjav num_kod
    #     num_kod = len(M)

    #     # n je dolzina kodnih zamenjav (n=k+m)
    #     # e je stevilo napak, ki jih lahko dekodiramo
    #     # Izracunamo argmax Hammingovega pogoja
    #     for e in range(num_kod):
    #         e_s += math.comb(n,e)
    #         #print(f"Suma e({e}): {e_s}")
    #         if e_s != 0:
    #             res = (2**n)/e_s
    #         else:
    #             res = 0
    #         #print(f"Res e({e}): {res}")
            
    #         if res<num_kod:
    #             break
        
    #     return e




    

    



    


    # TODO
    # Sestavite program, ki bo določil in izpisal vse možne kodne zamenjave M={xi}



    # TODO
    # Izpiše naj še vse kolikokratne napake je s podano matriko sposoben poravljati

    # TODO
    # Na vhodu sprejema na vhodu poljubno zaporedje binarnih simbolov, enake dolžine, kot so kodne zamenjave.

    # TODO
    # S pomočjo podane matrike za preverjanje sodosti odkriva in popravlja napake v vhodnem zaporedju in izpisuje na izhodu veljavne kodne zamenjave.


    
