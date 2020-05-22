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

def copyM(G:list) -> list:
    """
    una copia de una lista de listas
    se mama el python
    """
    M = []
    for x in G:
        M.append(x.copy())

    return M
            
def leGrafConT(G:list,T:list) -> list:
    """
    La subgrafica de G que representa el arbol T
    G es una lista de lista que repreenta la matriz
    de pesos.
    T es una lista de tuplas que representan aristas
    que es la lista de aristas que forman un arbol de G.
    Regresa la represntacion en matriz de T deacuerdo a G
    """
    Gt = copyM(G)
    n = len(Gt) #G debe de ser una matriz cuadrada
    noArc = -1 #debuger en visualizacion,
    #y en este contexto que no hay distancia

    #llenados de infinitosA
    for i in range(0,n):
        for j in range(0,n):
            if i != j:
                Gt[i][j] = noArc
            else:
                Gt[i][j] = 0

    #solo estas aristas permaneceran en su valor original
    for edge in T:
        u = edge[0]
        v = edge[1]
        Gt[u][v] = G[u][v]
        Gt[v][u] = G[v][u]
        
    #todo lo demas se a quedado igual segun G
    return Gt

def listConOddOfT(G:list) -> set:
    """
    Un lista con los vertices de grado impar
    """
    odds = set()
    n = len(G)
    for i in range(0,n):
        verTOdd = 0
        for j in range(0,n):
            if G[i][j] != -1 and (i != j):
                verTOdd += 1
        if verTOdd % 2 != 0: #impar entras
            odds.add(i)
    return odds

def constSubH(G:list,odds:set) -> list:
    """
    Construye la subgrafica inducida por
    un conjunto de vertices 'odds' sobre la
    grafica: matriz : lista de lista
    """
    #La grafica se queda igual excepto
    #por los vertices de G que no aparecieron en odds
    vertex = set()
    n = len(G)
    for i in range(0,n):
        vertex.add(i)

    excluidos = vertex.difference(odds)

    #una copia a modificar
    H = copyM(G)

    for v in excluidos:
        for i in range(0,n):
            if i != v: #sin el (v,v)
                H[i][v] = -1 #todo la columna
        for j in range(0,n):
            if j != v:
                H[v][j] = -1

    return H

#minimumWeightedPerfectMatching a la ñera
def mWPMn(H:list, odds:set) -> list:
    """
    Hasta este punto seguido en el algoritmo en
    general H tiene las siguiente propiedades importantes
    1) Provino desde un espacio metrico
    2) Se relaciono de la grafica G por su arbol minimo T
    3) El numero de vertices de grado impar del arbol es un numero par
    4) Con esto es posible un perfect matching
    5) H es la subgrafica de G inducida por esos nodos de grado impar
    6) Porque G es completa, H conserva las conecciones entre sus vertices

    Por todo esto se puede buscar el mWPM en H de forma voraz y proseguir
    delimitando sus obciones deacuerdo al peso de las aristas y las
    aristas ya emparejadas(con su chanvelan)
    """
    Todds = list(odds)
    cobert = set()
    #cobert.add(Todds[0]) #un elemento par iniciar
    n = len(H)

    visto = set() #control sobre vertices recorridos, evita compartir endpoints
    Mh = []

    while cobert != odds:
        #iteramos sobre H 
        for u in odds:
            vMin = 999999999
            a = 0 #recordara a u
            b = 0 #recordara a v
            if u not in cobert:
                for v in range(0,n):
                    if H[u][v] != 0 and H[u][v] != -1: #valor valido
                        if H[u][v] < vMin and v not in cobert:
                            vMin = H[u][v]
                            a = u #aunque u no cambiara mantiene la constistencia
                            b = v
                Mh.append((a,b))
                cobert.add(a)
                cobert.add(b) #como es un set los elementos ya existentes
                #no reflejan un cambio

    return Mh


def eulerMultigrafConList(T:list,Mh:list) -> list:
    """
    A partir de este punto, la construccion de las graficas
    pasan a ser una multigrafica Euleriana
    """
    D = T + Mh #siguendo la literatura
    #la neta solo fue una lista de sumas pero
    #queda desacoplado por buenas tecnicas de prog
    # - XD lo dice el que esta sigueindo una estrategia funcional en python
    """
    Una matriz de adyacencias ya no es adecuada para la representacion
    ahora tenemos una lista de las aristas, sus pesos de las nuevas
    aristas que posiblente se repitas (u,v) son las dadas por G original
    i.e G[u][v] = peso de las aristas en la lista D
    """
    return D

def eulerianTour(D:list) -> list:
    """
    Es la interfaz para preparar la funcion para
    encontrar el tour
    G es la matriz
    D es la lista de vertices de una posible multigrafica
    """
    A = D.copy()

    e0 = D[0] #la primera arista
    u0 = e0[0] #el primer vertice
    tour = []

    return find_tour(u0,A,tour)

def list_vecinosA(v:int, E:list) -> list:
    """
    Una funcion auxiliar que regresa la lista de aristas
    a la cual es incidente v
    E es una lista de aristas, tuplas de la forma (u,v)
    Se regresa la lista de tuplas de la forma (u,v,k) o (v,u,k)
    que indica la ocurencia de aristas al estilo no dirigidas
    donde las primeras dos entradas es la lista, la entrada k
    es el indice en la lista donde esta originalmente la arista,
    k va a ser importante para borrar por indice
    """

    n = len(E)
    A2 = []
    for i in range(0,n):
        e = E[i]
        a = e[0]
        b = e[1]

        if a == v:
            edge = (a,b,i)
            A2.append(edge)

        if b == v:
            edge = (b,a,i)
            A2.append(edge)

    return A2

#https://algorithmist.com/wiki/Euler_tour
def find_tour(u:int,A:list,tour:list) -> list:
    """
    Si C es cualquier ciclo en una grafica Euleriana,
    despues de remover las aristas de C, la grafica resultante,
    sus componentes conexas tambien son graficas eulerianas
    """
    A2 = list_vecinosA(u,A)
    for superEdge in A2:
        #a = superEdge[0] #u
        b = superEdge[1] #v
        k = superEdge[2]

        A.pop(k)
        find_tour(b,A,tour)
        break #cuando se resuelven las llamadas recursivas
        #los elementos de la lista ya no existen, pero la secuencia
        #continua dentro del for, sus siguientes elementos ya no tiene
        #una referencia, debe terminar ahi mismo
    tour.append(u)

    return tour #con la pawa de la recursion

def shotKutes(W:list) -> list:
    """
    Regresa una lista, que conserva el orden
    de sus elementos y sin elementos repetidos
    """
    #Esta funcion es de las primeras cosas que estudie en Python, UwU
    P = []
    for i in W:
        if i not in P:
            P.append(i)

    return P

#estas funciones ya estan adecuadas a todo el contexto seguido
def pesoTour(P:list, G:list) -> int:
    """
    P es una lista que representa un tour de G,
    i.e una lista de vertices, que es una permutacion de
    los vertices de G
    G es matriz de pesos
    Regresa el peso del tour
    """
    s = 0 #suma
    n = len(P)
    for i in range(0,n):#pensando en indices
        if (i+1) != n:
            u = P[i]
            v = P[i+1]
            s += G[u][v]
    #el ultimo
    a = P[0]
    z = P[-1]
    s += G[z][a]

    return s

#Una grafica de prueba
G = [
    [0,1,1,2,1],
    [1,0,1,1,2],
    [1,1,0,1,1],
    [2,1,1,0,1],
    [1,2,1,1,0]
    ]

M = [
    [0, 12,10,9, 12,11,12],
    [12,0, 8, 12,10,11,12],
    [10,8, 0, 11,3, 8, 9],
    [9, 12,11,0, 11,10,12],
    [12,10,3, 11,0,  6,7],
    [11,11,8, 10,6, 0, 9],
    [12,12,9, 12,7, 9, 0]
    ]


def nota():
    #print('Para evitar tener que escribir y validar una matriz\n',
     #     'por la entrada estandar (que seria muy engoroso), se mostrara\n',
      #    'un ejemplo con una matriz de 5 vertices')
    print('Los -1 representa que no existe el arco o que no hay una conexion\n'
          +'entre los vertices de las matrices que se van creando')


def main(G:list):
    #https://en.wikipedia.org/wiki/Christofides_algorithm
    print('Problema Metric TSP')
    print('Christofides algorithm')
    try:
        if isMetric(G):
            nota()
            print('La grafica G, es una grafrica en un espacio metrico')
            displayM(G)
            #print(isMetric(G)) #cumple las propiedades del espacio metrico
            print('El arbol de peso minimo T de la grafica G')
            T = leTreeMin(G)
            print(T)
            print('T (su grafo), en forma de matriz')
            Gt = leGrafConT(G,T)
            displayM(Gt)
            print('Conjunto de vertices de grado impar de T')
            oddV = listConOddOfT(Gt)
            print(oddV)
            print('Subgrafica H, inducida por esos vertices (de la origal)')
            H = constSubH(G,oddV)
            displayM(H)
            print('Mh, match perfecto minimo de H')
            Mh = mWPMn(H,oddV)
            print(Mh)
            print('MultiGrafo Euleriano D = T + Mh')
            D = eulerMultigrafConList(T,Mh)
            print(D)
            print('W un tour Euleriano de D')
            W = eulerianTour(D)
            print(W)
            print('Usando atajos (shortcuts), el tour del agente viajero (salesman tour)')
            print('(Ciclo Hamiltoniano de la grafica G)')
            P = shotKutes(W)
            s = pesoTour(P,G)
            print(P,'coste = ',s)
        else:
            raise ValueError
    except ValueError:
        print('Lastima, la matriz no representa un espacio metrico\n,'
              +'sobre el cual aplicar el algoritmo.')

#main(M)

def menu():
    print('Elige alguna matriz de prueva o ingreasa la tuya')
    print('G =')
    displayM(G)
    print()
    print('M =')
    displayM(M)
    print()
    print('Elije G|M, o presiona x para escribir tu propia matriz')
    while True:
        op = input('Tu opcion:')
        if op.upper() == 'G':
            main(G)
            break
        elif op.upper() == 'M':
            main(M)
            break
        elif op.lower() == 'x':
            X = constM()
            main(X)
            break
        else:
            print('Entrada invalida, intentalo de nuevo')
        

def constM():
    """
    Ingresa y construye una matriz cuadrada completa
    solo necesita los valores de la diagonal superior
    """
    n = constMpt2()

    X = [] #una lista
    for i in range(0,n):
        X.append([])#una lista de listas = matriz

    #llena la matrix para trabajar por posiciones
    for i in range(0,n):
        for j in range(0,n):
            X[i].append(-1)

    X = constMpt3(X,n)
    return finalConf(X)

def constMpt2(x=-1):
    """
    Para que devuelva un n valido
    n entero y n > 0, por defaut
    y adecuada a un numero que le pasen
    """
    while True:
        try:
            if x == -1:
                n = int(input('Escribe la dimension (n) de la matriz cuadrada: '))
                if n > 1:
                    return n
                else:
                    raise ValueError
            else:
                z = int(input())
                if z > 0:
                    return z
                else:
                    raise ValueError
        except ValueError:
            print('Valor invalido, intentalo de nuevo')

def constMpt3(X:list,n:int) -> list:
    """
    Llena por la diagonal superior
    y rellena simetricamente, los valores de la diagonal son 0
    """
    
    for i in range(0,n):
        for j in range(0,n):
            if i == j:
                X[i][j] = (0)
            elif i < j:
                print('Escribe el valor de A['+str(i)+']['+str(j)+']:', end=' ')
                w = constMpt2(1)
                X[i][j] = w
                X[j][i] = w
    return X

def finalConf(X:list):
    """
    Confirama si quieres continuar con esta lista o
    eligir otra
    """
    print('Esta es la matriz resultante, ¿quieres continuar? [S/N]')
    displayM(X)
    while not False:
        op = input()
        if op.upper() == 'S':
            return X
        elif op.upper() == 'N':
            print('Se construira otra matriz')
            constM()
        else:
            print('Valor invalido, intentalo de nuevo')

menu()
