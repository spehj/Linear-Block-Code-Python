import enum
from operator import xor
import numpy as np

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

    # Kodne zamenjave
    E = np.zeros((m_d, m))
    
    #print(E)
    # for i,_ in enumerate(D):
    #     print(i)
    #     E[i][0] = D[i][1] ^ D[i][2] ^ D[i][3]
    #     E[i][1] = D[i][0] ^ D[i][2] ^ D[i][3]
    #     E[i][2] = D[i][0] ^ D[i][1] ^ D[i][3]
    z = []
    for ind, j in enumerate(H):
        z.append(j[m:])
    
    z = np.array(z)
    print(z)
    print()
    for i,x in enumerate(D):
        #z1 = H[i]

        for l in range(m):
            #E[i][l] = z[l][0]*x[0] ^ z[l][1]*x[1] ^ z[l][2]*x[2]^ z[l][3]*x[3]
            E[i][l] = calcXor(z[l], x)

        #E[i][0] =0*x[0] ^ 1*x[1] ^ 1*x[2] ^ 1*x[3]
        #E[i][1] = x[0] ^ x[2] ^ x[3]
        #E[i][2] = x[0] ^ x[1] ^ x[3]
    
    print(E)


    

    



    


    # TODO
    # Sestavite program, ki bo določil in izpisal vse možne kodne zamenjave M={xi}



    # TODO
    # Izpiše naj še vse kolikokratne napake je s podano matriko sposoben poravljati

    # TODO
    # Na vhodu sprejema na vhodu poljubno zaporedje binarnih simbolov, enake dolžine, kot so kodne zamenjave.

    # TODO
    # S pomočjo podane matrike za preverjanje sodosti odkriva in popravlja napake v vhodnem zaporedju in izpisuje na izhodu veljavne kodne zamenjave.


    
