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