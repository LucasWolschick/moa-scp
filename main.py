import random
import time
from app.parser import parse_problema
from app.resolve import resolve

import argparse

parser = argparse.ArgumentParser(
    description="Obtém uma solução aproximada para o problema de cobertura de conjuntos usando algoritmos heurísticos."
)
parser.add_argument("entrada", type=open, help="O problema SCP a ser resolvido.")
parser.add_argument(
    "--semente",
    type=int,
    help="A semente para o gerador de números aleatórios.",
    default=time.time_ns(),
)
parser.add_argument(
    "--construtivo",
    type=str,
    help="O algoritmo construtivo a ser usado. Pode ser 'F' ou 'aleatorio'",
    default="F",
    choices=["F", "aleatorio"],
)


def main():
    args = parser.parse_args()
    print(f"Semente: {args.semente}")
    print(f"Algoritmo construtivo: {args.construtivo}")
    random.seed(args.semente)
    problema = parse_problema(args.entrada.read())
    print(resolve(problema, args.construtivo))


if __name__ == "__main__":
    main()
