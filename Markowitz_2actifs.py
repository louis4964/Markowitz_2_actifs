import numpy as np 
import matplotlib.pyplot as plt 

# actfi 1  R = 7,12%  Société Apple Inc. AAPL
# actif 2  R = 2,26%  Société ORANGE ORA.PA

#Rendements éspérés
R_1 = 0.0712
R_2 = 0.0226

# Liste des rendements annuels de 2025 (0) à 2016 (9)
R_1_a = [0.1248, 0.4846, -0.0539, 0.8895, 0.8231, 0.3465, -0.2640, 0.4901, 0.3071, -0.1497]
R_2_a = [-0.0331, 0.0478, 0.0252, -0.0267, -0.2146, 0.0291, 0.0543, 0.1832, 0.0018, 0.2458]

# Moyenne empirique
R1 = sum(R_1_a) / len(R_1_a)
R2 = sum(R_2_a) / len(R_2_a)

# Liste des pondérations et rendements interpolés
p = []
P=[]
for i in range(11):
    w1 = round(i / 10, 2)
    w2 = round(1 - w1, 2)
    rendement = round(R_1 * w1 + R_2 * w2, 4)
    p.append((w1, w2, rendement))
    P.append(rendement)

    # création de la liste des rendements des différents portefeuilles en fonction du poids des actifs.

M_cov = [] # Création de la matrice de covariance vide ( 10*10 )
for i in range(2):
    M_cov.append([(),()])

# Création des sommes  pour determiner les covariances
def ecart():
    ecart = 0
    for t in range(len(R_1_a)):
        ecart += (R_1_a[t] - R1)*(R_2_a[t] - R2)
    return ecart

def ecart_2 (x):
    ecar = 0 
    if x == 1 :
        for t in range(len(R_1_a)):
           ecar += (R_1_a[t] - R1)**2
        return ecar
    else:
        for t in range(len(R_1_a)):
           ecar += (R_2_a[t] - R2)**2
        return ecar

# Création de la matrice de covariance : Methode de Markowitz

for i in range(2):
    for j in range(2):
        if i != j :
           M_cov[i][j] = round((1/(len(R_1_a)-1)) * ecart(),4)
        elif i == j == 1 :
           M_cov[i][i] = round((1/(len(R_1_a)-1)) * ecart_2(1),4)
        else:
            M_cov[j][j] = round((1/(len(R_1_a)-1)) * ecart_2(2),4)


def ecart_type(x):  # Calcul de l'écart-type de chacune des serie 
    o = np.sqrt((1/(len(R_1_a)-1)) * ecart_2(x))
    return o 

corr = M_cov[0][1]/(ecart_type(1)*ecart_type(2))

# Calcul du risuqe du portefeuille selon le poids des actifs
r_p = []
for i in range(len(R_1_a)+1):
    r_p.append(round(float(np.sqrt((p[i][0]**2)*ecart_type(1)**2 +(p[i][1]**2)*ecart_type(2)**2 +2*p[i][1]*p[i][0]*corr*ecart_type(2)*ecart_type(1))),4))

# o_p = sqrt(w_1**2*o_1**2 + w_2**2*o_2**2 + 2*w_2*w_1*o_1*o_2*corr12)



"""
poids 1      poids 2        rendement (%)      risque (%)      avec corr = 0.72 forte corrélation entre orange et apple
0              1               2.26               12.42
0.1            0.9             2.75                9.73
0.2            0.8             3.23                8.88
0.3            0.7             3.72               10.33
0.4            0.6             4.2                13.34
0.5            0.5             4.69               17.12
0.6            0.4             5.18               21.25
0.7            0.3             5.66               25.57
0.8            0.2             6.15               29.99
0.9            0.1             6.63               34.48
1              0               7.12               39.01

MVP =>   risque = 8.88 % et rendement = 3.23 %
correlation à 0.72 = forte =>  les actifs bougent ensemble → moins de bénéfice de diversification
si correlation plus faible ou négative => la courbe serait plus plate au début → meilleure réduction du risque

"""


# Tracé du rendement en fonction du risque ( avec frontière efficiente )
plt.figure(1)
plt.plot(r_p,P,'r-')
plt.plot(r_p,P,'k.')
plt.plot(0.0888,0.0323,'g.',label='MVP')
plt.xlabel("Risque du portefeuille")
plt.ylabel("Rendement du portefeuille")
plt.title("frontière efficiente")
plt.legend()
plt.grid(True)
plt.xlim(0,0.4)
plt.ylim(0,0.08)
plt.show()


# Ratio de Sharpe - RS = (R(w)−rf)/σ(w)
rf = 0.015 # Livret A - taux sans risque
RS = []
for i in range(11):
    RS.append((p[i][2]-rf)/r_p[i])


# Tracé du bilan contenant Ratio de sharpe, Rendement et Risque des portefeuilles
n = np.linspace(1,11,11)
width = 0.35  # width of the bars
plt.figure(2)
plt.bar(n - width/2, P, width=width, label='Rendement')
plt.bar(n + width/2, r_p, width=width, label='Risque')
plt.plot(n, RS, 'g', label='Ratio de Sharpe')
plt.bar(3 - width/2, 0.0323, width=width, label='Rendement du MVP',color="green")
plt.bar(3 + width/2, 0.0888, width=width, label='Risque du MVP',color="red")
plt.plot(3, RS[2], 'k.', label='Ratio de Sharpe du MVP')
plt.xlabel("Portefeuilles")
plt.ylabel("grandeur %")
plt.title("Bilan des portefeuilles à deux actifs")
plt.grid(True)
plt.legend()
plt.show()

"""
Interprétation
Ratio élevé (plus grand que 1) :
Le portefeuille offre un bon rendement ajusté au risque. Autrement dit, tu es bien récompensé pour le risque que tu prends.

Ratio proche de zéro :
Le rendement n’est pas vraiment supérieur au taux sans risque, donc prendre ce risque n’apporte pas d’avantage.

Ratio négatif :
Le portefeuille performe moins bien que l’actif sans risque, donc tu prends un risque pour un rendement inférieur, ce qui n’est pas souhaitable.
"""