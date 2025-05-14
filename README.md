# Distributed Print System - Exclusão Mútua
Relatório em [Relatório Técnico](relatorio.md)

## Requisitos
- Python 3.8+
- TCP/IP habilitado (localhost)
- Adaptado para Linux e MacOS

## Execução
Para rodar, abra o terminal e execute
```sh
./run_nodes.sh
```
 -> Os logs estarão nos arquivos node_x.log para cada nó


Para matar os processos, abra o terminal e rode 
````sh
./kill_nodes.sh
````

## Configurações
O arquivo `config.json` lista os nós e suas portas.

## Comportamento
Cada nó tenta acessar o recurso a cada 2s. Se for bem-sucedido, imprime `k` números com 0.5s de intervalo.

## Algoritmo
Implementação baseada em Ricart & Agrawala (1981), com controle de acesso distribuído e ordenação por timestamp lógico.
