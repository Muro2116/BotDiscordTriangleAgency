# Triangle Agency Discord Bot

Bot em Python para rolar dados do sistema Triangle Agency no Discord.

## O que ele faz

- gera 6 dados de 1 a 4;
- calcula caos final;
- detecta Triscêndencia;
- aplica burnout;
- permite gastar QA via botão interativo;
- responde com embed visual no Discord.

## Tecnologias usadas

- Python 3
- discord.py
- dotenv
- interação assíncrona com Discord (`commands.Bot`, slash commands, embeds, modais e botões)

## Estrutura do projeto

```text
BotDiscordTriangleAgency/
├── bot.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── .env
```

## Como rodar localmente

### 1. Clone o projeto

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

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o token do bot

Crie um arquivo `.env` na raiz do projeto com:

```env
DISCORD_TOKEN=SEU_TOKEN_AQUI
```

Você pode usar o arquivo `.env.example` como base.

> Nunca publique esse token no GitHub.

### 5. Crie o bot no Discord

1. Acesse o Discord Developer Portal.
2. Crie uma aplicação.
3. Vá em "Bot" e gere um token.
4. Copie o token para o arquivo `.env`.
5. Convide o bot para o servidor via OAuth2 > URL Generator.

### 6. Execute o bot

```bash
python bot.py
```

Se estiver tudo certo, o terminal deve mostrar:

```text
bot operante e pronto para rolar dados!
```

## Como usar

No Discord, use:

```text
/solicitar-a-agencia
```

Ou com burnout:

```text
/solicitar-a-agencia burnout:2
```

O bot retorna um embed com os dados, caos, Triscêndencia e botão para gastar QA quando aplicável.

## Regras principais implementadas

- 6 dados de 1 a 4 são rolados;
- a rolagem é avaliada por caos;
- três 3s podem ativar Triscêndencia;
- burnout altera os dados e o caos;
- QA pode converter dados não 3 em 3 antes do cálculo final.

## Arquivos importantes

- `bot.py`: lógica principal do bot
- `requirements.txt`: dependências do projeto
- `.env`: token do bot em ambiente local

## Troubleshooting

Se o bot não iniciar:

- verifique se o Python está instalado;
- confirme que o ambiente virtual foi ativado;
- confira se o token do `.env` está correto;
- rode `pip install -r requirements.txt` novamente.

Se o comando `/solicitar-a-agencia` não aparecer:

- confirme que o bot está no servidor;
- confirme que as permissões de interação estão corretas;
- reinicie o bot após adicionar o bot ao servidor.
