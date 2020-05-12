M = [
    [0, 12,10,9, 12,11,12],
    [12,0, 8, 12,10,11,12],
    [10,8, 0, 11,3, 8, 9],
    [9, 12,11,0, 11,10,12],
    [12,10,3, 11,0,  6,7],
    [11,11,8, 10,6, 0, 9],
    [12,12,9, 12,7, 9, 0]
    ]

Z = [
    [0,5,1],
    [5,0,1],
    [1,1,0]
    ]

#print(M) esta M mantiene un espacio metrico

def displayM(M:list):
    """
    osea imprimir una matriz
    """
    for i in M:
        print(i) #la neta lo mantengo simple

displayM(M)

def isMetric(M:list) -> bool:
    """
    metric space
    (1) w(i,j) = 0 sii i = j, osea la diagonal es 0
    (2) w(i,j) = w(j,i), osea que es simetrica -> grafo no dirigido
    (3) w(i,j) <= w(i,k) + w(k,j) a.k.a la desigualdad del triangulo
    """
    n = len(M) #num de filas
    #print(n)
    #usando indices
    for i in range(0,n):
        m = len(M[i]) #tendra que ser cuadrada
        #print(m)

        if n != m:
            return False
        else:
            for j in range(0,m):
                #dale las 3 condiciones
                for k in range(0,n): #k -> [0,n]
                    if i == j and M[i][j] != 0:
                        #print(M[i][j])
                        return False
                    elif M[i][j] != M[j][i]:
                        #print(M[i][j])
                        return False
                    else:
                        if M[i][j] > M[i][k] + M[k][j]: #con el contrario
                            #print(i)
                            #print(j)
                            #print(k)
                            return False

    #si no fallo todo eso
    return True

print(isMetric(M))

displayM(Z)
print(isMetric(Z))
                        

            
            
