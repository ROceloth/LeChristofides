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

G = [
    [0,1,1,2,1],
    [1,0,1,1,2],
    [1,1,0,1,1],
    [2,1,1,0,1],
    [1,2,1,1,0]
    ]

#print(M) esta M mantiene un espacio metrico

def displayM(M:list):
    """
    osea imprimir una matriz
    """
    for i in M:
        print(i) #la neta lo mantengo simple

#displayM(M)

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

#print(isMetric(M))

#displayM(Z)
#print(isMetric(Z))
#que las matrix no sean vacias

def leTreeMin(G:list) -> list:
    """
    El ya tu sabhe arbol generador de peso
    minimo para las graficas -> matrices -> listas de listas,
    en especial que cumplan isMetric.
    algoritmo de Prim, version del libro Estructura de datos de Joyanes
    de la pagina 479, adaptado a este contexto y a Python 3
    """
    T = [] #la lista de las aristas del arbol
    V = set() #metele pawa, con un set
    for i in range(0,len(G)):
        V.add(i) #considerare los vertices como del 0 a len de la matriz
        #como la etiqueta de los vertices
    u = 0 #como primer vertice
    W = {u}# segun el libro

    while W != V:
        temp = V.difference(W)
        vMin = 999999999 #un numerote para empezar la busqueda por el minimo
        a = 0 #recordara a u
        b = 0 #recordara a v
        for u in W:
            for v in temp:
                if G[u][v] < vMin:
                    a = u
                    b = v
                    vMin = G[u][b]

        W.add(b)
        T.append((a,b))

    return T
            
displayM(G)
print(isMetric(G))
print('Le arbol')
T = leTreeMin(G)
print(T)

            
            
