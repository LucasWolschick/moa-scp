import math
from random import choice, randrange
import app.lista_ordenada as lista_ordenada

from app.resolve import GULOSOS, solucao_valida, remove_redundantes, Trabalho


def jacobs_brusco(
    entrada: Trabalho,
    rho1: float,
    rho2: float,
    S: list[int],
    Sl: list[int],
    func=GULOSOS[1],
):
    """
    Encontra uma solução vizinha de *S* usando a proposta de Jacobs e Brusco.

    *S* é a solução atual.

    *Sl* é a lista de colunas que não estão em *S*.

    *rho1* é a porcentagem de colunas de *S* que serão removidas.

    *rho2* é a porcentagem do custo máximo das colunas em *S* abaixo da qual uma coluna
    de *Sl* deverá ter para ser uma candidata a ser adicionada a *S*.

    *func* é a função gulosa usada para escolher as colunas de *Sl* que serão adicionadas
     a *S*.

    A função *func* deve receber dois parâmetros: o custo da coluna e quantas linhas ela
    cobre, e retornar um valor númerico.
    """
    S = list(S)
    Sl = list(Sl)

    # 0
    d = 0
    D = math.ceil(rho1 * len(S))
    E = math.ceil(rho2 * max(custo for i, custo in enumerate(entrada.custos) if i in S))
    w = [0] * entrada.n_linhas
    for colu in S:
        for lin in entrada.colunas[colu]:
            w[lin] += 1

    while d != D:
        # 1
        ik = randrange(len(S))
        # 2
        k = S.pop(ik)
        lista_ordenada.insere(Sl, k)
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
        for colun in Sl:
            if entrada.custos[colun] < E:
                # SlE será ordenado
                SlE.append(colun)

        def beta_j(j):
            vj = cobre_U[j]
            if vj > 0:
                return func(entrada.custos[j], vj)
            else:
                return math.inf

        cols_betas = [(j, beta_j(j)) for j in SlE]
        beta_min = min(e[1] for e in cols_betas)
        K = [e[0] for e in cols_betas if e[1] == beta_min]

        # 5
        k = choice(K)
        lista_ordenada.remove(Sl, k)
        lista_ordenada.insere(S, k)
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
    l = remove_redundantes(entrada, S)

    return l
