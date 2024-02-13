# moa-scp

Sistema de geração de soluções para instâncias do problema de cobertura de conjuntos.

Lucas Wolschick, 2024.

Desenvolvido para a segunda avaliação de Modelagem e Otimização Algorítmica, do curso de
Bacharelado em Ciência da Computação da Universidade Estadual de Maringá.

## Execução

Certifique-se de que possui um intrepretador Python 3.10 ou superior instalado em sua
máquina.
Abra um terminal e execute o comando:

```bash
$ python3 main.py --semente 5 --construtivo F ./input/Teste_01.dat
```

Onde `--semente` é a semente para o gerador de números aleatórios, `--construtivo` especifica
o algoritmo construtivo a ser usado, podendo ser 'F' ou 'aleatorio' e `./input/Teste_01.dat` é
o caminho para o arquivo de entrada.

O arquivo de entrada deve conter no mínimo quatro linhas: a primeira deve conter um número
representando o número de linhas, a segunda, o número de colunas, e as linhas a partir da
quarta especificam as colunas da instância, devendo possuir o número da coluna, o custo
da coluna e a lista de linhas que a coluna cobre, todos separados por espaços.

## Testes

Todos os testes podem ser executados pelo arquivo `run.cmd`, que salva as saídas dos testes na pasta `output`.
Os testes são executados sequencialmente.
Note que o arquivo utiliza o comando `py` mas pode ser facilmente substituído por `python3` se necessário.

O script `plot.py` é capaz de gerar gráficos para séries temporais de melhoramento de cada instância.
A série deve ser inserida no interior do script.
O script requer a biblioteca `matplotlib` instalada no ambiente de execução para funcionar.
Alguns gráficos gerados se encontram na pasta `output`, como exemplo.

## Relatório

O relatório do trabalho se encontra no arquivo `Relatório.pdf`,disponível na pasta raiz.
