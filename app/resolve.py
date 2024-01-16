from random import choice
from typing import Iterable
from time import time

from dataclasses import dataclass
from app.lista_ordenada import inter_olista, sub_olista
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


@dataclass
class Trabalho:
    instancia: Instancia

    n_linhas: int
    n_colunas: int

    linhas: list[list[int]]
    """Colunas cobertas por cada linha"""

    colunas: list[list[int]]
    """Linhas cobertas por cada coluna"""

    custos: list[float]
    """Custo de cada coluna"""


def trabalho_from_instancia(instancia: Instancia) -> Trabalho:
    linhas = [[] for _ in range(instancia.n_linhas)]
    colunas = [[] for _ in range(instancia.n_colunas)]
    custos = [0.0] * instancia.n_colunas

    for coluna in instancia.dados:
        for linha in coluna.elem:
            colunas[coluna.id].append(linha)
            linhas[linha].append(coluna.id)
        custos[coluna.id] = coluna.custo

    for coluna in colunas:
        coluna.sort()

    for linha in linhas:
        linha.sort()

    return Trabalho(
        instancia=instancia,
        n_linhas=instancia.n_linhas,
        n_colunas=instancia.n_colunas,
        linhas=linhas,
        colunas=colunas,
        custos=custos,
    )


def solucao_valida(entrada: Trabalho, solucao: Iterable[int]) -> bool:
    linhas_faltando = set(range(entrada.n_linhas))
    for coluna in solucao:
        for elem in entrada.colunas[coluna]:
            linhas_faltando.discard(elem)
    return len(linhas_faltando) == 0


def constroi_solucao(entrada: Trabalho, f=GULOSOS[2]):
    linhas_faltando = list(range(entrada.n_linhas))
    solucao = set()
    colunas_nao_usadas = set(range(entrada.n_colunas))

    # primeira passada
    while linhas_faltando:
        candidatos = []
        for coluna in colunas_nao_usadas:
            cj = entrada.custos[coluna]
            kj = len(inter_olista(entrada.colunas[coluna], linhas_faltando))
            if kj > 0:
                candidatos.append((coluna, f(cj, kj)))
        col = min(candidatos, key=lambda x: x[1])[0]
        solucao.add(col)
        colunas_nao_usadas.remove(col)
        linhas_faltando = sub_olista(linhas_faltando, entrada.colunas[col])

    # segunda passada
    l = list(solucao)
    l.sort(key=lambda c: entrada.custos[c])
    for i in range(len(l) - 1, -1, -1):
        e = l.pop(i)
        if not solucao_valida(entrada, l):
            l.append(e)

    solucao = set(l)

    return solucao


def custo_solucao(entrada: Trabalho, solucao: set[int]) -> float:
    return sum(entrada.custos[x] for x in solucao)


def rrange(start, stop, steps):
    for i in range(steps):
        yield (1 - i / (steps - 1)) * start + i / (steps - 1) * stop


def encontra_solucao(entrada: Trabalho):
    from app.jacobs_brusco import jacobs_brusco

    print("Encontrada solucao inicial...")
    solucao = constroi_solucao(
        entrada,
        lambda cj, kj: choice(GULOSOS)(cj, kj)
        if kj > 1
        else choice(GULOSOS[:5])(cj, kj),
    )
    print(solucao, custo_solucao(entrada, solucao))

    now = time()
    best_rho1 = 0
    best_rho2 = 0
    old_sol = solucao
    melhor = solucao
    for rho1 in rrange(0.10, 1.00, 10):
        for rho2 in rrange(1.1, 2.0, 10):
            print(rho1, rho2)
            solucao = old_sol
            for i in range(100):
                # if i % 20 == 0:
                #    print(f"[{i+1}/100] Melhorando...")
                nova_solucao = set(
                    jacobs_brusco(
                        entrada,
                        rho1,
                        rho2,
                        list(solucao),
                        list(set(range(entrada.n_colunas)) - solucao),
                    )
                )
                if custo_solucao(entrada, nova_solucao) <= custo_solucao(
                    entrada, solucao
                ):
                    # print("Melhorou")
                    solucao = nova_solucao
                    if custo_solucao(entrada, solucao) < custo_solucao(entrada, melhor):
                        melhor = solucao
                        best_rho1 = rho1
                        best_rho2 = rho2
    print(f"Melhores parâmetros: rho1={best_rho1}, rho2={best_rho2}")
    print(f"Levou {time()-now}")

    print(f"Solução valida: {solucao_valida(entrada, melhor)}")

    return melhor


def resolve(entrada: Instancia):
    trabalho = trabalho_from_instancia(entrada)
    solucao = encontra_solucao(trabalho)
    custo = custo_solucao(trabalho, solucao)
    solucao = {x + 1 for x in solucao}

    return solucao, custo
