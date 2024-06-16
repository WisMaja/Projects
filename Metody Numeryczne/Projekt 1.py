import math
import numpy as np
import matplotlib.pyplot as plt

# Cel 1: Napisać funkcję do aproksymacji średniokwadratowej metodą najmniejszych kwadratów.
#        Deklaracja funkcji: def Nazwisko_Imie_Aproks_MNK(x,y,n)
# Uwagi:
#       x, y to wartości punktów,
#       n to stopień szukanego wielomianu,
#       funkcja ma zwracać współczynniki wielomianu aproksymacyjnego a = [a0, a1, a2, ..., an]

def Wiśniewska_Maja_Aproks_MNK(x,y,n):
    y = np.transpose(y)
    A = np.array([[x[j] ** i for i in range(n + 1)] for j in range(len(x))])
    AT = np.transpose(A)

    #AT*A*a = AT*y
    ATA = np.dot(AT,A)

    ATy = np.dot(AT,y)

    #ATA = L*LT
    L = ch(ATA)

    # Rozwiązanie L*z = A^T*y, szukam z
    z = rozw_dolnej(L, ATy)

    # Rozwiązanie L^T*a = z, szukam a
    a = rozw_gornej(np.transpose(L), z)
    wyswietl(x, y, a)
    return a

def ch(A):
    n = A.shape[0]
    L = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i+1):
            if i == j:
                suma = sum(L[i][k] * L[i][k] for k in range(j))
                L[i][j] = math.sqrt(A[i][i] - suma)
            else:
                suma = sum(L[i][k] * L[j][k] for k in range(j))
                L[i][j] = (A[i][j] - suma) / L[j][j]
    return L

def rozw_dolnej(A, b):
    n = len(b)
    x = [0.0 for _ in range(n)]
    for i in range(n):
        sum = 0.0
        for k in range(i):
            sum += A[i][k] * x[k]
        x[i] = (b[i] - sum) / A[i][i]
    return x

def rozw_gornej(A, b):
    n = len(b)
    x=[0.0 for _ in range(n)]
    for i in range(n-1,-1,-1):
        sum = 0.0
        for k in range(i+1, n):
            sum += A[i][k] * x[k]
        x[i] = (b[i] - sum) / A[i][i]

    return x

# Cel 2: Algorytm ma narysować wykres wyznaczonego wielomianu wraz z zaznaczeniem punktów,
#        do których wielomian został dopasowany.
# Uwagi do realizacji obliczeń.
#       stworzć macierz A,
#       stworzyć układ równań normalnych - macierz układu oraz wektor prawej strony układu,
#       zastosować rozkład macierzy układu równań metodą Choleskyego,
#       rozwiązać układ równań dwuetapowo.


def wyswietl(x, y, a):
    # Wykres punktów
    plt.scatter(x, y, color='red', label='Punkty')

    # Wykres wielomianu aproksymacyjnego
    x_values = np.linspace(min(x), max(x), 100)
    y_values = sum(a[i] * x_values**i for i in range(len(a)))
    plt.plot(x_values, y_values, label='Wielomian aproksymacyjny', color='blue')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Aproksymacja średniokwadratowa')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    
#EXEC
x = [-5, -8, 0 , 9,4]
y = [29.5, 18, 6, 9, 17]
n = 0

#a = Wiśniewska_Maja_Aproks_MNK(x,y,n)
#print(a)

Wiśniewska_Maja_Aproks_MNK(x,y,n)
