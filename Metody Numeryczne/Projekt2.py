import numpy as np
# Przykładowa macierz
A = np.array([[2, -3, 1], [-3, -4, -2], [1, -2, 4]])
A2 = np.array([[2,1,0],[1,4,1],[0,1,2]])

def gauss_elimination(A, b):
    n = len(b)
    M = A.copy()

    # Augment the matrix A with vector b
    Ab = np.hstack([M, b.reshape(-1, 1)])

    for i in range(n):
        # Find the pivot element
        max_row = i + np.argmax(np.abs(Ab[i:, i]))
        if i != max_row:
            Ab[[i, max_row]] = Ab[[max_row, i]]
        
        # Normalize the pivot row
        Ab[i] = Ab[i] / Ab[i, i]

        # Eliminate the current column
        for j in range(i + 1, n):
            Ab[j] = Ab[j] - Ab[j, i] * Ab[i]

    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = Ab[i, -1] - np.sum(Ab[i, i + 1:n] * x[i + 1:n])

    return x

#Metody
def el_gaussaU(a,b):
    n = len(a)
    for i in range(n-1):
        for j in range(i+1,n):
            l: float = a[j][i] /a[i][i]
            b[j] -= l* b[i]
            for k in range(i,n):
                a[j][k] -= l*a[i][k]
    return a,b


def rozw_gornej(a,b):
    n = len(b)
    x=[0.0 for _ in range(n)]
    for i in range(n-1,-1,-1):
        sum = 0.0
        for k in range(i+1, n):
            sum += a[i][k] * x[k]
        x[i] = (b[i] - sum) / a[i][i]

    return x

def met_siecznych(f, x0 , x1):
    #1. w kroku k znajdujemy pierwiastek równania charakterystycznego λk przy pomocy metody siecznych
    for i in range(1000):
        fx0 = f(x0)
        fx1 = f(x1)
        if fx0 ==0:
            return x0
        if fx1 == 0:
            return x1
        if fx0 - fx1 == 0:
            break
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        x0, x1 = x1, x2
    return x1

def deflacja(w,n, x):
    """
    Deflacja wielomianu przez jego pierwiastek.
    
    Parameters:
    w (list): lista wspołczynników iwelomianu
    x (float): Pierwiastek wielomianu.
    n (int): stopien wielomianu

    Returns:
    numpy.poly1d: Nowy wielomian po deflacji.
    """
    #2. przy pomocy algorytmu Hornera dzielimy wA(λ) przez dwumian (λ−λk) usyskując wielomian w'A(λ) stopnia n − 1
    new_w = np.zeros(n)
    new_w[0] = w[0]
    for i in range(1, n):
        new_w[i] = w[i] + x * new_w[i - 1]
        
    return new_w



# Cel 1: Napisać funkcję do znajdowania wartości i wektorów własnych macierzy
# Deklaracja funkcji: def Nazwisko_Imie_(A)
    # Uwagi:
    #   A to macierz kwadratowa n × n (testować dla macierzy symetrycznych i z wartościami rzeczywistymi - mają
    #   rzeczywiste wartości i wektory własne).
def Wiśniewska_Maja_(A):
    n = len(A[0])
    #korzystamy z metody Kryłowa by znaleźć postać równania charakterystycznego macierzy:
        #wA(λ) = det(A−λI) = a0λ^3 + a1λ^2 + a2λ + a3
        #0 = a0A^3 + a1A^2 + a2A + a3   |:a0
        #0 = A^3 + c1A^2 + c2A + c3
        # -A^3 = c1A^2 + c2A + c3       |*b
        # -bA^3 = bc1A^2 + bc2A + bc3
        #   [A^2b,Ab,b]*[c1,c2,c3]T = -bA^3
        #   [b,Ab,A^b]*[c3,c2,c1] = -bA^3

    #wybieramy niezerowy wektor i tworzymy układ równań,
    b = np.zeros(n)
    b[0] = 1

    M = np.zeros((n, n))
    M[:,0] =b

    for i in range(1, n):
        M[:, i] = np.dot(A, M[:, i-1])
    
    M3b = np.dot(A, M[:, n-1])
    M3b = - M3b
    
    #rozwiązujemy układ równań przy pomocy eliminacji Gaussa,
    M_rozw, M3b_rozw = el_gaussaU(M,M3b)
    c = rozw_gornej(M_rozw, M3b_rozw)
    c.append(1)
    c = c[::-1]

    #otrzymujemy równanie wA(λ) = 0, gdzie wielomian jest stopnia n
    w = np.poly1d(list(c))
    print(f"wielomian charakterystyczny:")
    print(w)
    print()

    #znajdujemy kolejne pierwiastki równania charakterystycznego przy pomocy metody siecznych 
    #(nie wymaga znajomości wzoru pochodnej) oraz metody deflacji:
    met_siecznych(w,0,1)

    w_wlasne = []
    #powtarzamy kroki 1 i 2 aż do obliczenia wszystkich warto±ci własnych
    for i in range(n):
        if len(w_wlasne) == 0:
            x0, x1 = 0, 1
        else:
            x0, x1 = w_wlasne[-1], w_wlasne[-1] + 1
        #krok 1
        w_wlasna = met_siecznych(w, x0, x1)
        w_wlasne.append(np.round(w_wlasna, 4))
        #krok 2
        c = deflacja(c,n-i, w_wlasna)
        w = np.poly1d(list(c))
        

    wektory_wlasne = []
    for w_wlasna in w_wlasne:
        # Tworzymy kopię macierzy A i odejmujemy (lambda * I)
        Macierz = A - (np.eye(n) * w_wlasna)

        # SVD macierzy (A - lambda * I)
        _, _, vh = np.linalg.svd(Macierz)

        # Wybieramy ostatni wiersz z vh, który odpowiada zerowej wartości osobliwej
        eigenvector = vh[-1, :]

        # Normalizujemy wektor własny
        eigenvector = eigenvector / np.linalg.norm(eigenvector)
        
        # Dodajemy wektor własny do listy
        wektory_wlasne.append(eigenvector)

    print("Wartości własne:")
    print(w_wlasne)
    print()
    print("Wektory własne:")
    print(np.array(wektory_wlasne).T)

    return w_wlasne, np.array(wektory_wlasne).T
    




# DLA CHĘTNYCH (NIEBOWIąZKOWE): znając wartości własne, korzystając z definicji, 
# wyznaczyć odpowiadające im wektory własne - jak??



Wiśniewska_Maja_(A2)