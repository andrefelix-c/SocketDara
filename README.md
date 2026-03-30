# 🕹️ SocketDara

Implementação do jogo de tabuleiro africano **Dara** para dois jogadores, com comunicação em tempo real via **sockets TCP** e interface gráfica construída com **[Flet](https://flet.dev/)** (Python).

---

## 📖 Sobre o Jogo

O **Dara** é um jogo tradicional africano, originário da Nigéria, jogado em um tabuleiro de **6 colunas × 5 linhas (30 células)**. O objetivo é reduzir as peças do adversário a **2 ou menos**, removendo-as ao formar linhas de 3.

### Regras

O jogo é dividido em duas fases:

**Fase 1 — Colocação**
- Cada jogador possui **12 peças**.
- Os jogadores se alternam colocando uma peça por turno no tabuleiro.
- **É proibido formar uma linha de 3 peças** durante esta fase.
- A fase termina quando todas as 24 peças estiverem no tabuleiro.

**Fase 2 — Movimentação**
- Os jogadores se alternam movendo uma peça por turno para uma **célula adjacente vazia** (cima, baixo, esquerda ou direita — sem diagonais).
- Ao formar uma **linha de 3 peças**, o jogador pode **comer (remover)** uma peça do adversário.
- Vence quem deixar o adversário com **2 ou menos peças**.

---

## 🗂️ Estrutura do Projeto

```
SocketDara/
├── main.py                        # Entrada da aplicação e roteamento
├── views/
│   ├── init.py                    # Tela inicial (configuração de conexão)
│   └── game.py                    # Tela do jogo (tabuleiro e chat)
└── functions/
    ├── game_logic_func.py         # Lógica do jogo (cliques, validações)
    ├── socket_func.py             # Conexão e comunicação via socket TCP
    └── utils_func.py              # Inicialização de variáveis e utilitários de UI
```

---

## 🔌 Protocolo de Comunicação

A comunicação entre os jogadores é feita via **socket TCP**, com mensagens de texto delimitadas por `\n`:

| Mensagem                        | Descrição                                              |
|---------------------------------|--------------------------------------------------------|
| `MSG:<texto>\n`                 | Mensagem de chat                                       |
| `ADD:<idx>\n`                   | Colocou uma peça na célula `idx` (fase 1)              |
| `MOVE:<origem>-<destino>\n`     | Moveu uma peça (fase 2, sem comer)                     |
| `MOVEAT:<origem>-<destino>-<comida>\n` | Moveu e comeu a peça em `comida` (fase 2)     |
| `EXIT\n`                        | Jogador abandonou a partida                            |

---

## 🚀 Como Executar

### Opção 1 — Executável (recomendado)

Baixe o executável pré-compilado diretamente na aba **[Releases](https://github.com/andrefelix-c/SocketDara/releases)** do repositório. O arquivo está disponível na pasta `build/` do release. Basta baixar, extrair e executar — sem precisar instalar Python ou dependências.

---

### Opção 2 — Rodando pelo código-fonte

**Pré-requisitos:**
- Python 3.8+
- [Flet](https://flet.dev/)

**Instalação:**

```bash
git clone https://github.com/andrefelix-c/SocketDara.git
cd SocketDara
pip install -r requirements.txt
```

**Como rodar:**

Como aplicativo desktop:
```bash
flet run main.py
```

Como aplicativo web (abre no navegador):
```bash
flet run main.py --web
```

---

### Iniciando uma partida

O jogo requer dois jogadores conectados na mesma rede local (ou na mesma máquina via `127.0.0.1`).

**Jogador 1 — Servidor:**
1. Abra o aplicativo
2. Selecione **Servidor**
3. Informe o IP da sua máquina (ou `0.0.0.0` para aceitar qualquer conexão)
4. Defina uma porta (padrão: `8080`)
5. Clique em **Play!** e aguarde o oponente

**Jogador 2 — Cliente:**
1. Abra o aplicativo
2. Selecione **Cliente**
3. Informe o **IP do servidor**
4. Informe a mesma porta usada pelo servidor
5. Clique em **Play!**

---

## 🧩 Estado da Sessão

O estado do jogo é gerenciado via `page.session.store`. As principais variáveis são:

| Chave             | Tipo           | Descrição                                                        |
|-------------------|----------------|------------------------------------------------------------------|
| `sou_servidor`    | `int`          | Papel do jogador: `0` = Servidor, `1` = Cliente                 |
| `socket_ativo`    | `socket`       | Socket TCP da conexão ativa                                      |
| `tabuleiro_logico`| `list[int]`    | Estado das 30 células: `0` vazio, `1` meu, `2` oponente         |
| `pecas_colocadas` | `list[int]`    | `[minhas_peças, peças_oponente]`                                 |
| `meu_turno`       | `list[bool]`   | `[True]` se é a vez do jogador local                            |
| `fase`            | `int`          | Fase atual: `1` colocação, `2` movimentação                     |
| `idx_antigo`      | `int`          | Índice da peça selecionada para mover (`-1` se nenhuma)         |
| `comer_peça`      | `bool`         | `True` quando o jogador deve escolher uma peça para remover     |

---

## 🛠️ Tecnologias

- **[Python](https://www.python.org/)** — Linguagem principal
- **[Flet](https://flet.dev/)** — Framework para interface gráfica multiplataforma
- **`socket`** — Comunicação TCP entre os jogadores
- **`threading`** — Recebimento de mensagens em background sem bloquear a UI
