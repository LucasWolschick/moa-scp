import math
from random import choice

from app.problema_parser import Instancia
from app.resolve import solucao_valida

def jacobs_brusco(entrada: Instancia, rho1: float, rho2: float, S: list[int], Sl: list[int]):
    S = list(S)
    Sl = list(Sl)

    # 0
    d = 0
    D = math.ceil(rho1*len(S))
    E = math.ceil(rho2*max(col.custo for col in entrada.dados if col.id in S))
    w = [0] * entrada.n_linhas
    for col in S:
        for lin in entrada.dados[col].elem:
            w[lin] += 1
    
    while d != D:
        # 1
        k = choice(S)
        # 2
        S.remove(k)
        Sl.append(k)
        for lin in entrada.dados[k].elem:
            w[lin] -= 1
        d = d + 1
    
    # 3
    U = []
    for lin, count in enumerate(w):
        if count == 0:
            U.append(lin)
        
    while U:
        # 4
        SlE = []
        for col in Sl:
            if entrada.dados[col].custo < E:
                SlE.append(col)
        
        def alpha(i, j):
            # retorna 1 se a linha não está coberta mas pode ser coberta pela coluna j
            return w[i] == 0 and i in entrada.dados[j].elem
        def v(j):
            # soma alphas da coluna
            soma = 0
            for i in entrada.dados[j].elem:
                soma += alpha(i, j)
            return soma
        def beta_j(j):
            if (vj := v(j)) > 0:
                return entrada.dados[j].custo / vj
            else:
                return math.inf
        
        beta_min = min(beta_j(j) for j in SlE)
        K = [j for j in SlE if beta_j(j) == beta_min]

        # 5
        k = choice(K)
        Sl.remove(k)
        S.append(k)
        for lin in entrada.dados[k].elem:
            w[lin] += 1

        # 3
        U = []
        for lin, count in enumerate(w):
            if count == 0:
                U.append(lin)
    
    # 6
    l = list(S)
    l.sort(key=lambda c: entrada.dados[c].custo)
    for i in range(len(l) - 1, -1, -1):
        e = l.pop(i)
        if not solucao_valida(entrada, l):
            l.append(e)

    return S

