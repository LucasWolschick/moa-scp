import math
from random import choice, randrange
from app.lista_ordenada import insere_olista, inter_olista, remove_olista

from app.resolve import solucao_valida, Trabalho


def jacobs_brusco(
    entrada: Trabalho, rho1: float, rho2: float, S: list[int], Sl: list[int]
):
    S = list(S)
    Sl = list(Sl)

    # 0
    d = 0
    D = math.ceil(rho1 * len(S))
    E = math.ceil(rho2 * max(custo for i, custo in enumerate(entrada.custos) if i in S))
    w = [0] * entrada.n_linhas
    for col in S:
        for lin in entrada.colunas[col]:
            w[lin] += 1

    while d != D:
        # 1
        ik = randrange(len(S))
        # 2
        k = S.pop(ik)
        insere_olista(Sl, k)
        for lin in entrada.colunas[k]:
            w[lin] -= 1
        d = d + 1

    # 3
    U = []
    for lin, count in enumerate(w):
        if count == 0:
            U.append(lin)

    # cobre_U[j] = quantas linhas de U j cobre
    cobre_U = [0] * entrada.n_colunas
    for icol, col in enumerate(entrada.colunas):
        for lin in col:
            if w[lin] == 0:  # está em U
                cobre_U[icol] += 1

    # toda vez que U é modificado, temos que modificar cobre_U.

    while U:
        # 4
        SlE = []
        for col in Sl:
            if entrada.custos[col] < E:
                # SlE será ordenado
                SlE.append(col)

        # def alpha(i, j):
        #     # retorna 1 se a linha não está coberta mas pode ser coberta pela coluna j
        #     return w[i] == 0 and i in entrada.dados[j].elem

        # def v(j):
        #     # soma alphas da coluna
        #     soma = 0
        #     for i in entrada.dados[j].elem:
        #         soma += alpha(i, j)
        #     return soma

        def beta_j(j):
            # quantas linhas de U j cobre?
            vj = cobre_U[j]  # len(inter_olista(entrada.colunas[j], U))
            if vj > 0:
                return entrada.custos[j] / vj
            else:
                return math.inf

        cols_betas = [(j, beta_j(j)) for j in SlE]
        beta_min = min(e[1] for e in cols_betas)
        K = [e[0] for e in cols_betas if e[1] == beta_min]

        # 5
        k = choice(K)
        remove_olista(Sl, k)
        insere_olista(S, k)
        for lin in entrada.colunas[k]:
            w[lin] += 1

            # lin agora não está mais em U
            # as colunas que cobriam essa linha não a cobrem mais
            for col_cobria_lin in entrada.linhas[lin]:
                cobre_U[col_cobria_lin] -= 1

        # 3
        U = []
        for lin, count in enumerate(w):
            if count == 0:
                U.append(lin)

    # 6
    l = list(S)
    l.sort(key=lambda c: entrada.custos[c])
    for i in range(len(l) - 1, -1, -1):
        e = l.pop(i)
        if not solucao_valida(entrada, l):
            l.append(e)

    return S
