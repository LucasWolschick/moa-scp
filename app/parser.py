from dataclasses import dataclass
from re import findall


def extrai_numeros(s: str) -> list[float]:
    return [float(x) for x in findall(r"[-+]?(?:\d*\.*\d+)", s)]


@dataclass
class Coluna:
    id: int
    custo: float
    elem: set[int]


def parse_coluna(l: str) -> Coluna:
    id, custo, *resto = l.split()
    return Coluna(int(id) - 1, float(custo), set(int(x) - 1 for x in resto))


@dataclass
class Instancia:
    n_linhas: int
    n_colunas: int
    densidade: float
    dados: list[Coluna]


def parse_problema(p: str) -> Instancia:
    linhas = p.splitlines()
    n_linhas = int(extrai_numeros(linhas[0])[0])
    n_colunas = int(extrai_numeros(linhas[1])[0])
    dados = [parse_coluna(l) for l in linhas[3:]]

    total = sum(len(d.elem) for d in dados)
    densidade = total / (n_linhas * n_colunas)

    return Instancia(n_linhas, n_colunas, densidade, dados)
