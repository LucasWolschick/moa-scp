from itertools import combinations
from random import randrange
from app.resolve import GULOSOS, Trabalho, custo_solucao, remove_redundantes
import app.lista_ordenada as lista_ordenada


def swap_k_opt(
    entrada: Trabalho,
    S: list[int],
    k: int = 1,
    func=GULOSOS[1],
):
    """
    Encontra todas as soluções vizinhas de *S* obtidas removendo-se k colunas de *S* e
    as substituindo pelas colunas de menor custo que cobrem as linhas que não estão
    cobertas por *S*, segundo a heurística *func*, que retorna um valor numérico para
    um custo e um número de linhas cobertas.

    Retorna a melhor solução encontrada.
    """
    # remove redundâncias da solução
    S_original = list(S)
    custo_original = custo_solucao(entrada, set(S_original))

    best_sol = S_original
    best_cost = custo_original

    for removed_cols_t in combinations(S_original, k):
        S = lista_ordenada.sub(S_original, list(removed_cols_t))
        removed_cols = set(removed_cols_t)
        w = [0] * entrada.n_linhas  # número de colunas que cobrem cada linha
        for colu in S:
            for lin in entrada.colunas[colu]:
                w[lin] += 1

        # cobre_U[j] = quantas linhas de U j cobre
        cobre_U = [0] * entrada.n_colunas
        for icol, col in enumerate(entrada.colunas):
            for lin in col:
                if w[lin] == 0:  # está em U
                    cobre_U[icol] += 1

        U_count = sum(count > 0 for count in w)

        # candidatos que ajudam a preencher as linhas
        candidatos = [
            icol
            for icol, count in enumerate(cobre_U)
            if count > 0 and icol not in removed_cols
        ]

        while candidatos and U_count:
            min_cost_column_i = randrange(len(candidatos))  # min(
            #     range(len(candidatos)),
            #     key=lambda candidato_i: func(
            #         entrada.instancia.dados[candidatos[candidato_i]].custo,
            #         cobre_U[candidatos[candidato_i]],
            #     ),
            # )
            min_cost_column = candidatos.pop(min_cost_column_i)
            lista_ordenada.insere(S, min_cost_column)
            for lin in entrada.colunas[min_cost_column]:
                w[lin] += 1

                for col_cobria_lin in entrada.linhas[lin]:
                    cobre_U[col_cobria_lin] -= 1

            U_count = sum(count > 0 for count in w)

            # candidatos que ajudam a preencher as linhas
            candidatos = [
                icol
                for icol, count in enumerate(cobre_U)
                if count > 0 and icol not in removed_cols
            ]

            S = remove_redundantes(entrada, S)

        if U_count == 0 and (S_cost := custo_solucao(entrada, set(S))) < best_cost:
            # todas as linhas cobertas e a solução é melhor
            best_sol = list(S)
            best_cost = S_cost

    return remove_redundantes(entrada, best_sol)
