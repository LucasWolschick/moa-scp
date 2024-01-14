from app.problema_parser import parse_problema
from app.resolve import resolve

import argparse

parser = argparse.ArgumentParser(
    description="Obtém uma solução aproximada para o problema de cobertura de conjuntos usando algoritmos heurísticos."
)
parser.add_argument("entrada", type=open, help="O problema SCP a ser resolvido.")


def main():
    args = parser.parse_args()
    problema = parse_problema(args.entrada.read())
    print(resolve(problema))


if __name__ == "__main__":
    main()
