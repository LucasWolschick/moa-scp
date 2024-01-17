from random import choice
from typing import Iterable
from time import time

from dataclasses import dataclass
import app.lista_ordenada as lista_ordenada
from app.parser import Instancia

import math

# Vasco, Wilson (1984)
GULOSOS = [
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
    linhas: list[list[int]] = [[] for _ in range(instancia.n_linhas)]
    colunas: list[list[int]] = [[] for _ in range(instancia.n_colunas)]
    custos = [0.0] * instancia.n_colunas

    for coluna in instancia.dados:
        for linha in coluna.elem:
            colunas[coluna.id].append(linha)
            linhas[linha].append(coluna.id)
        custos[coluna.id] = coluna.custo

    for col in colunas:
        col.sort()

    for lin in linhas:
        lin.sort()

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


def remove_redundantes(entrada: Trabalho, solucao: list[int]) -> list[int]:
    l = solucao.copy()
    l.sort(key=lambda c: entrada.custos[c])
    for i in range(len(l) - 1, -1, -1):
        e = l.pop(i)
        if not solucao_valida(entrada, l):
            l.append(e)
    l.sort()
    return l


def constroi_solucao(entrada: Trabalho, f=GULOSOS[2]):
    linhas_faltando = list(range(entrada.n_linhas))
    solucao = []
    colunas_nao_usadas = set(range(entrada.n_colunas))

    # primeira passada
    while linhas_faltando:
        candidatos = []
        for coluna in colunas_nao_usadas:
            cj = entrada.custos[coluna]
            kj = len(lista_ordenada.inter(entrada.colunas[coluna], linhas_faltando))
            if kj > 0:
                candidatos.append((coluna, f(cj, kj)))
        col = min(candidatos, key=lambda x: x[1])[0]
        lista_ordenada.insere(solucao, col)
        colunas_nao_usadas.remove(col)
        linhas_faltando = lista_ordenada.sub(linhas_faltando, entrada.colunas[col])

    # segunda passada
    solucao = remove_redundantes(entrada, solucao)

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
    custo_sol = custo_solucao(entrada, solucao)
    print(solucao, custo_sol)

    now = time()
    best_rho1 = 0
    best_rho2 = 0

    old_sol = solucao
    custo_old_sol = custo_sol

    melhor = solucao
    custo_melhor_sol = custo_sol

    for rho1 in rrange(0.10, 1.00, 10):
        for rho2 in rrange(1.1, 3.0, 10):
            print(rho1, rho2)
            solucao = old_sol
            custo_sol = custo_old_sol
            for _ in range(100):
                nova_solucao = jacobs_brusco(
                    entrada,
                    rho1,
                    rho2,
                    solucao,
                    lista_ordenada.sub(list(range(entrada.n_colunas)), solucao),
                )
                custo_nova_solucao = custo_solucao(entrada, nova_solucao)

                if custo_nova_solucao <= custo_sol:
                    solucao = nova_solucao
                    custo_sol = custo_nova_solucao
                    if custo_sol < custo_melhor_sol:
                        melhor = solucao
                        custo_melhor_sol = custo_sol
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
