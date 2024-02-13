from dataclasses import dataclass
from re import findall


def extrai_numeros(s: str) -> list[float]:
    """Extrai todos os números de um texto *s* e retorna uma lista com eles."""
    return [float(x) for x in findall(r"[-+]?(?:\d*\.*\d+)", s)]


@dataclass
class Coluna:
    """Representa uma coluna da matriz de coberturas."""

    id: int
    """Identificador da coluna."""

    custo: float
    """Custo da coluna."""
    elem: set[int]
    """Linhas cobertas pela coluna."""


def parse_coluna(l: str) -> Coluna:
    """Converte uma linha de texto em uma coluna."""
    id, custo, *resto = l.split()
    return Coluna(int(id) - 1, float(custo), set(int(x) - 1 for x in resto))


@dataclass
class Instancia:
    """Representa uma instância do problema de cobertura de conjuntos."""

    n_linhas: int
    """Número de linhas do problema."""
    n_colunas: int
    """Número de colunas do problema."""
    densidade: float
    """Densidade da matriz de coberturas. Calculada dividindo o número total de linhas cobertas por todas as colunas por n_colunas * n_linhas."""
    dados: list[Coluna]
    """As colunas da instância."""


def parse_problema(p: str) -> Instancia:
    """Converte uma string *p* em uma instância do problema de cobertura de conjuntos."""
    linhas = p.splitlines()
    n_linhas = int(extrai_numeros(linhas[0])[0])
    n_colunas = int(extrai_numeros(linhas[1])[0])
    dados = [parse_coluna(l) for l in linhas[3:]]

    total = sum(len(d.elem) for d in dados)
    densidade = total / (n_linhas * n_colunas)

    return Instancia(n_linhas, n_colunas, densidade, dados)
