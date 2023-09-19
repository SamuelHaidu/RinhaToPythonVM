# Rinha Compiler

O **Rinha Compiler** é um projeto que tem como objetivo converter a linguagem exótica "Rinha" em Bytecode Python VM. É parte de uma competição de compiladores onde os participantes devem criar um interpretador ou compilador que funcione em uma máquina com 2 núcleos e 2GB de RAM.

O desafio central é trabalhar com algo chamado "árvore sintática abstrata" representada no formato JSON. Essa árvore sintática abstrata é gerada pelos organizadores da competição e contém as informações necessárias para interpretar ou compilar o programa.

## Estrutura do Código

O projeto é dividido em várias partes essenciais, cada uma com sua função específica. Algumas das partes principais incluem:

- `ast`: Contém a definição da árvore sintática abstrata e seus elementos.
- `compiler.py`: Implementa a lógica de compilação do Rinha para Bytecode da Python VM.
- `symbol_table.py`: Cria e lida com a tabela de símbolos para o compilador.

## Detalhes da implementação

Primeiro é feito o parse do json e convertido em objetos de python, mais leves e faceis de trabalhar. Depois é construido a tabela de simbolos e onde se checa se as variaveis existem quando chamadas. Depois é feito a compilação para bytecode de python a partir da arvore sintatica abstrata. Com o bytecode salvamos em um arquivo .pyc e executamos com o python.

## Como usar o CLI

O Rinha Compiler (CLI) é uma ferramenta que permite compilar a linguagem exótica "Rinha" em Bytecode Python VM. Abaixo estão as instruções para utilizar o CLI:

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado em seu sistema.

### Instalação

Não é necessário instalar o Rinha Compiler, pois é um script Python autônomo.

### Uso

1. Clone este repositório e navegue até a raiz em que o modulo `rinhac` está localizado.

2. Abra um terminal no diretório mencionado.

3. Para compilar um arquivo AST Rinha em bytecode Python (`.pyc`), execute o seguinte comando:

    ```bash
    python -m rinhac [-b] <caminho-para-arquivo-ast> [-o <caminho-de-saida.pyc>]
    ```
    `[...]` = opcional

    Substitua `<caminho-para-arquivo-ast>` pelo caminho para o arquivo AST Rinha que deseja compilar.

    Se desejar, você pode especificar um caminho de saída personalizado para o arquivo `.pyc` usando a opção `-o`.

4. Para imprimir a árvore sintática abstrata (AST) do arquivo Rinha, execute o seguinte comando:

    ```bash
    python -m rinhac -a <caminho-para-arquivo-ast>
    ```

    Substitua `<caminho-para-arquivo-ast>` pelo caminho para o arquivo AST Rinha que deseja imprimir.

5. Para imprimir a tabela de símbolos do arquivo Rinha, execute o seguinte comando:

    ```bash
    python -m rinhac -s <caminho-para-arquivo-ast>
    ```

    Substitua `<caminho-para-arquivo-ast>` pelo caminho para o arquivo AST Rinha que deseja usar para imprimir a tabela de símbolos.

6. Sinta-se à vontade para explorar outras opções e funcionalidades executando `python -m rinhac --help`.
