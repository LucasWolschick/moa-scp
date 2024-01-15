from random import choice
from typing import Iterable
from time import time
from app.problema_parser import Instancia

import math

# Vasco, Wilson (1984)
GULOSOS = [
    lambda cj, kj: -kj,
    lambda cj, kj: cj,
    lambda cj, kj: cj / kj,
    lambda cj, kj: cj / kj**2,
    lambda cj, kj: cj**0.5 / kj**2,
    lambda cj, kj: cj / math.log2(kj),
    lambda cj, kj: cj / (kj * math.log2(kj)),
    lambda cj, kj: cj / (kj * math.log(kj)),
]


def solucao_valida(entrada: Instancia, solucao: Iterable[int]) -> bool:
    linhas_faltando = set(range(entrada.n_linhas))
    for coluna in solucao:
        linhas_faltando -= entrada.dados[coluna].elem
    return len(linhas_faltando) == 0


def constroi_solucao(entrada: Instancia, f=GULOSOS[2]):
    linhas_faltando = set(range(entrada.n_linhas))
    solucao = set()
    colunas_nao_usadas = set(range(entrada.n_colunas))

    # primeira passada
    while linhas_faltando:
        candidatos = []
        for coluna in colunas_nao_usadas:
            col = entrada.dados[coluna]
            cj = col.custo
            kj = len(col.elem.intersection(linhas_faltando))
            if kj > 0:
                candidatos.append((col, f(cj, kj)))
        col = min(candidatos, key=lambda x: x[1])[0]
        solucao.add(col.id)
        colunas_nao_usadas.remove(col.id)
        linhas_faltando -= col.elem

    # segunda passada
    l = list(solucao)
    l.sort(key=lambda c: entrada.dados[c].custo)
    for i in range(len(l) - 1, -1, -1):
        e = l.pop(i)
        if not solucao_valida(entrada, l):
            l.append(e)

    solucao = set(l)

    return solucao

def custo_solucao(entrada: Instancia, solucao: set[int]) -> float:
    return sum(entrada.dados[x].custo for x in solucao)

def encontra_solucao(entrada: Instancia):
    from app.jacobs_brusco import jacobs_brusco

    print("Encontrada solucao inicial...")
    solucao = constroi_solucao(entrada, lambda cj, kj: choice(GULOSOS)(cj, kj) if kj > 1 else choice(GULOSOS[:5])(cj, kj))
    print(solucao, custo_solucao(entrada, solucao))

    now = time()
    for i in range(100):
        print(f"[{i+1}/100] Melhorando...")
        nova_solucao = set(jacobs_brusco(entrada, 0.8, 1.1, list(solucao), list(set(range(entrada.n_colunas)) - solucao)))
        if custo_solucao(entrada, nova_solucao) <= custo_solucao(entrada, solucao):
            print("Melhorou")
            solucao = nova_solucao
    print(f"Levou {time()-now}")

    print(f"Solução valida: {solucao_valida(entrada, solucao)}")

    return solucao


def resolve(entrada: Instancia):
    solucao = encontra_solucao(entrada)
    custo = sum(entrada.dados[x].custo for x in solucao)
    solucao = {x + 1 for x in solucao}

    return solucao, custo
