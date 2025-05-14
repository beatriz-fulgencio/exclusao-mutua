
# Relatório Técnico — Exclusão Mútua Distribuída

**Disciplina:** Computação Distribuída
**Universidade:** PUC Minas
**Professor:** Matheus Barros Pereira
**Autores:** Beatriz Fulgencio da Cunha Menezes

---

## 1. Introdução

Este relatório descreve a implementação de um sistema distribuído para controle de acesso a um recurso compartilhado (servidor de impressão), utilizando o algoritmo de **exclusão mútua distribuída de Ricart & Agrawala (1981)**. Cada nó do sistema simula um processo independente, que solicita e acessa o recurso de forma coordenada com os demais nós, sem a existência de um nó central.

---

##  2. Objetivo

O principal objetivo foi **garantir exclusão mútua** no acesso ao recurso de impressão, onde:

* Cada nó imprime uma sequência de `k` números, com 0.5 segundos entre cada número.
* A sequência começa a partir do timestamp da última mensagem recebida.
* Os acessos são decididos aleatoriamente a cada 2 segundos.
* Todos os nós se comunicam entre si usando TCP/IP.
* A comunicação utiliza mensagens do tipo `{timestamp, id}` e `{ok, id}`.

Além disso, foram implementadas melhorias extras como **tolerância a falhas via timeout**.

---

##  3. Implementação

A implementação foi realizada em **Python 3**, estruturada nos seguintes módulos:

| Arquivo               | Responsabilidade principal                              |
| --------------------- | ------------------------------------------------------- |
| `node.py`             | Inicializa o nó, controla o ciclo de acesso e impressão |
| `mutual_exclusion.py` | Algoritmo Ricart & Agrawala com controle de timeout     |
| `network.py`          | Comunicação TCP/IP entre os nós                         |
| `printer.py`          | Impressão sequencial de números com delay               |
| `utils.py`            | Funções auxiliares como geração aleatória de acesso     |
| `config.json`         | Lista de nós, IPs e portas                              |

---

##  4. Algoritmo de Exclusão Mútua

###  Ricart & Agrawala (1981)

Cada nó solicita acesso ao recurso compartilhado enviando uma mensagem `{timestamp, id}` para os demais. O acesso é concedido somente após receber `ok` de **todos os outros nós**. A decisão de prioridade é feita com base no par `(timestamp, id)`.

### Timeout e Tolerância a Falhas (Extra)
Como melhoria, foi adicionado um mecanismo de timeout:
Se um nó não receber ok de outro dentro de 3 segundos, ele assume que o outro nó falhou e prossegue normalmente com os oks restantes. Isso evita deadlocks e melhora a robustez do sistema em ambientes distribuídos reais.

---

##  5. Comunicação

A comunicação entre nós é feita por meio de **sockets TCP/IP**.
Cada nó possui seu próprio servidor TCP que escuta em uma porta específica (definida no `config.json`).

Mensagens trocadas:

* Solicitação: `{ "type": "request", "timestamp": <int>, "id": <int> }`
* Resposta: `{ "type": "ok", "id": <int> }`

---

##  6. Impressão

Ao acessar o recurso, o nó imprime uma sequência de números de tamanho `k ∈ [1, 10]`, com 0.5s entre cada valor. A sequência se inicia a partir do **timestamp da última mensagem recebida**.

Exemplo de saída:

```
[NODE 3] 42
[NODE 3] 43
[NODE 3] 44
```

---

## 7. Execução

### Requisitos:

* Python 3.8+
* Sistema com suporte a sockets (Linux, macOS, ou Windows com Git Bash)
* Adaptado para Linux e MacOS

### Instruções:

1. Iniciar todos os nós com:

```bash
./run_nodes.sh
```
2. Para visualizar os logs entre nos aquivos `node_{x}.log`

3. Para parar todos os nós:

```bash
./kill_nodes.sh all 
```
4. Para parar um nó:

```bash
./kill_nodes {node_to_kill}
```
---

##  8. Testes Realizados

* Teste com todos os nós operacionais → sincronização correta.
* Teste com queda simulada de 1 nó → sistema continua operando (timeout funcional).
* Teste com delays entre nós → algoritmo se adapta pela ordenação via timestamp.

---

## 9. Funcionalidades Extras Implementadas

| Funcionalidade              | Descrição                                                               |
| --------------------------- | ----------------------------------------------------------------------- |
| Tolerância a falhas         | Se um nó não responde em 3s, é considerado falho e ignorado             |
| Logs no terminal            | Todos os eventos são impressos com `flush=True` para facilitar rastreio |
| Detecção dinâmica de falhas | O sistema marca nós como inativos em tempo de execução sem travar       |

---

## 10. Conclusão

O sistema desenvolvido atende aos requisitos do trabalho, com uma implementação correta e funcional do algoritmo de Ricart & Agrawala. A adição de **tolerância a falhas via timeout** fortalece a robustez do sistema, permitindo que ele opere mesmo em cenários com nós falhos.

O trabalho explora conceitos importantes de sistemas distribuídos como **exclusão mútua, sincronização por relógios lógicos, comunicação TCP/IP** e **resiliência a falhas**.

---

## 11. Referências

* Ricart, G., & Agrawala, A. K. (1981). *An optimal algorithm for mutual exclusion in computer networks*.
* Tanenbaum, A. S., & van Steen, M. (2007). *Distributed Systems: Principles and Paradigms*.
* Notas de aula da disciplina "Computação Distribuída" - PUC Minas.