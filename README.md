# Triangle Agency Discord Bot

Bot para rolagem de dados do sistema Triangle Agency no Discord, com suporte a comandos de barra (/rolar), cálculo de caos, Triscêndencia, burnout e uso de Quality Assurances (QA) por meio de interações em interface gráfica do Discord.

## Visão geral

Este projeto foi criado para automatizar a mecânica de dados do sistema Triangle Agency dentro de um servidor Discord. Em vez de jogadores terem que contar manualmente a rolagem, o bot:

- gera 6 dados de 1 a 4;
- calcula o caos final;
- detecta a Triscêndencia;
- aplica regras de burnout;
- oferece um botão para gastar QA em uma rolagem;
- envia o resultado em um embed visual, com emojis personalizados.

O bot foi escrito em Python usando a biblioteca discord.py e está pronto para ser executado localmente ou em qualquer ambiente com acesso a um token do Discord.

## Funcionalidades

### 1. Funcionalidade principal

Comando disponível no Discord:

- /rolar
- parâmetro opcional: burnout

Exemplo:

- /rolar
- /rolar burnout:2

A rolagem gera 6 dados com valores de 1 a 4 e aplica a lógica de simulação do sistema.

### 2. Cálculo de caos

A lógica central do projeto calcula:

- os dados resultantes;
- a quantidade de caos gerado;
- se a rolagem atingiu Triscêndencia;
- se a rolagem formou exatamente três 3s (estabilidade/resultado especial).

### 3. Triscêndencia

Quando três dados saem com valor 3, o sistema identifica a condição especial de Triscêndencia e zera o caos, caso a rolagem não tenha sido modificada por burnout ou QA.

### 4. Burnout

O parâmetro burnout transforma a rolagem substituindo 3s por dados queimados. Esse ajuste altera o cálculo e pode produzir caos extra.

### 5. QA (Quality Assurance)

Depois da rolagem, o usuário pode clicar no botão "Gastar QA", que abre um modal. A partir dele, o bot recalcula a rolagem convertendo dados não 3 em 3 de acordo com a quantidade informada.

### 6. Interface visual

Os resultados são enviados em um embed Discord com:

- título do bot;
- emojis de dados;
- mensagem de Triscêndencia;
- campo com caos gerado;
- rodapé informativo para burnout ou QA gasto.

---

## Tecnologias e técnicas utilizadas

### Python

O projeto é construído em Python 3, aproveitando o paradigma orientado a objetos e a programação assíncrona.

### discord.py

A biblioteca principal usada para comunicação com a API do Discord.

Principais usos:

- criação do cliente do bot;
- definição do `commands.Bot` customizado;
- uso de `app_commands` para slash commands;
- criação de embeds com `discord.Embed`;
- criação de botões e modais com `discord.ui.View` e `discord.ui.Modal`;
- tratamento de interações do usuário via `discord.Interaction`.

### Async/Await

O bot opera em ambiente assíncrono, o que é essencial para aplicações de Discord que respondem a eventos e interações do usuário em tempo real.

### Variáveis de ambiente

O projeto usa `.env` para guardar o token do bot sem expô-lo no código-fonte. Isso é feito com a biblioteca `python-dotenv`.

### Lógica de jogo

A função `calcular_rolagem()` implementa a regra central do sistema:

- copia a lista de dados;
- verifica Triscêndencia antes de alterações;
- aplica burnout ou QA conforme a regra;
- recalcula caos;
- trata casos especiais de três 3s.

### Interações do Discord

A interface inclui:

- `QAModal`: modal com campo de texto para inserir a quantidade de QA a ser paga;
- `QAView`: view com botão para abrir o modal;
- `interaction.response.send_message(...)` para enviar a resposta inicial;
- `interaction.response.edit_message(...)` para atualizar a mensagem após o gasto de QA.

### Emojis personalizados

Os emojis foram definidos como strings com IDs do Discord e exibidos no embed para dar uma identidade visual ao bot.

---

## Estrutura do projeto

```text
TriangleAgencyBot/
├── bot.py
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

### Arquivos principais

#### bot.py

Arquivo principal do bot. Contém:

- cliente do Discord;
- lógica de rolagem;
- criação dos embeds;
- comandos e interações;
- inicialização do bot.

#### requirements.txt

Lista as dependências do projeto.

#### .env

Arquivo local com a variável:

```env
DISCORD_TOKEN=seu_token_aqui
```

---

## Requisitos

Antes de rodar o bot, você precisará de:

- Python 3.9+ recomendado
- acesso ao Discord Developer Portal
- um servidor do Discord onde o bot será adicionado
- um token do bot gerado no portal do Discord

---

## Como configurar o ambiente local

### 1. Clone o repositório

```bash
git clone https://github.com/Muro2116/BotDiscordTriangleAgency
cd BotDiscordTriangleAgency
```

### 2. Crie um ambiente virtual

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Dependências do projeto:

```txt
discord.py==2.3.2
python-dotenv==1.0.0
audioop-lts==0.2.1
```

### 4. Crie o arquivo .env

No diretório raiz do projeto, crie um arquivo chamado `.env` com o seguinte conteúdo:

```env
DISCORD_TOKEN=SEU_TOKEN_AQUI
```

> Importante: nunca compartilhe esse token publicamente no GitHub.

### 5. Crie o bot no Discord

1. Acesse o Discord Developer Portal.
2. Crie uma aplicação.
3. Vá em "Bot".
4. Clique em "Reset Token" e copie o valor.
5. Cole esse valor no arquivo `.env`.
6. Ative as permissões necessárias para o bot.
7. Convide o bot para o servidor usando a URL de convite do portal.

### 6. Execute o bot

```bash
python bot.py
```

Se tudo estiver correto, o terminal deve imprimir algo como:

```text
bot operante e pronto para rolar dados!
```

---

## Como adicionar o bot ao servidor

No Discord Developer Portal:

1. Vá em "OAuth2" > "URL Generator";
2. Selecione as permissões do bot;
3. Gere a URL de convite;
4. Abra a URL em um navegador;
5. Escolha o servidor onde deseja instalar o bot;
6. Confirme a autorização.

Para slash commands funcionarem corretamente, o bot precisa estar dentro do servidor e ter as permissões necessárias para enviar mensagens e interações.

---

## Como usar o bot

No servidor do Discord, use o comando:

```text
/rolar
```

ou com burnout:

```text
/rolar burnout:2
```

O bot responderá com um embed contendo:

- dados rolados;
- caos gerado;
- Triscêndencia, se houver;
- botão para gastar QA, quando aplicável.

### Exemplo prático

Se o resultado for:

- dados: 3, 3, 4, 1, 2, 3

o sistema detecta que há 3 valores 3 e, conforme a regra, isso pode ser tratado como Triscêndencia ou como estabilidade, dependendo da lógica aplicada.

Se a rolagem sofrer burnout, o cálculo muda e alguns 3s podem ser convertidos em dados queimados, alterando o caos total.

---

## Dicas de desenvolvimento

### Segurança

- nunca commitar o arquivo `.env`;
- adicione `.env` no `.gitignore`;
- use um token separado para desenvolvimento e produção.

### Logs e debugging

O código atual imprime mensagens de estado no terminal, o que ajuda em testes locais.

Você pode adicionar logs mais detalhados para:

- número de dados rolados;
- quantidade de burnout aplicado;
- valor de QA gasto;
- total de caos calculado.

---

## Troubleshooting

### O bot não inicia

Verifique:

- se o Python está instalado corretamente;
- se o ambiente virtual foi ativado;
- se `requirements.txt` foi instalado;
- se o `.env` contém um token válido.

### O bot não aparece no servidor

Confira:

- se a URL de convite foi gerada com as permissões corretas;
- se o bot foi adicionado ao servidor;
- se o token não foi trocado ou revogado.

### O comando /rolar não funciona

Verifique:

- se as Slash Commands do bot foram sincronizadas;
- se o bot está online;
- se o servidor possui interação habilitada corretamente;
- se o código foi executado sem erro.

### Erro de importação

Execute:

```bash
pip install -r requirements.txt
```

e confirme que a biblioteca `discord.py` foi instalada corretamente.

---

## Comandos rápidos

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python bot.py
```