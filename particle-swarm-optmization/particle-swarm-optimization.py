#Generic Particle Swarm Optmization (PSO) Algorithm
#Bruno Sampaio Leite - UNIFESP

import math

if __name__ == "__main__":

    funcPower = int(input("Input optimization function power: \n"))
    funcCoef = []
    for term in range(funcPower+1):
        funcCoef.append(int(input(f"Input x^{term} coefficient : \n")))
    
    w, c1, c2, r1, r2 = [float(x) for x in (input("Input w, c1, c2, r1 and r2: \n").split())]
    
    n = int(input("Input array size: \n"))
    iterations = int(input("Input number of iterations: \n"))

    X = [10*(float(x)-0.5) for x in (input("Input position array: \n").split())]
    V = [(float(x)-0.5) for x in (input("Input speed array: \n").split())]

    F = []
    LBP = [-math.inf]*n

    for i in range(iterations):
        print(f"\nIteration {i+1}: ")

        F = [sum((X[k]**j)*funcCoef[j] for j in range(funcPower+1)) for k in range(n)]

        #Update Local Best Positions for every F(x), x in X
        LBP = [X[k]\
             if (F[k] > \
                    sum((LBP[k]**j)*funcCoef[j] for j in range(funcPower+1)))\
                      else (LBP[k]) for k in range(n)]
        #Global Best Fit is max LBP
        GBF = max(F)
        #Global Best Position is x where F(x) is max
        GBP = X[F.index(max(F))]

        print("LBP: ", [f"{x:.4f}" for x in LBP], f"\nGBF: {GBF:.4f}\nGBP: {GBP:.4f}")
        print("X: ", [f"{x:.4f}" for x in X])
        print("V: ", [f"{x:.4f}" for x in V])

        #Update speeds
        V = [w*V[j]+c1*r1*(LBP[j]-X[j])+c2*r2*(GBP-X[j]) for j in range(n)]
        #Update positions
        X = [X[j]+V[j] for j in range(n)]



    