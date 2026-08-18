import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from dotenv import load_dotenv

# carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# emojis do bot
EMOJI_DADO_1 = "<:dice1:1404616740268277781>"
EMOJI_DADO_2 = "<:dice2:1404617032690831502>"
EMOJI_DADO_3 = "<:dice3:1404617045294714980>"
EMOJI_DADO_4 = "<:dice4:1404617054975430789>"
EMOJI_DADO_BURNOUT = "<:diceburnout:1404617063548457040>"
CAOS_EMOJI = "<:caos:1404617625706954783>"

# classe do bot
class TriangleBot(commands.Bot):
    def __init__(self):
        # intents basicos para o bot
        super().__init__(command_prefix="!", intents=discord.Intents.default())
    
    async def setup_hook(self):
        # sincroniza os comandos de barra com o discord
        await self.tree.sync()
        print("bot operante e pronto para rolar dados!")

# instancia do bot
bot = TriangleBot()

# logica de rolagem de dados, burnout e qa
def calcular_rolagem(dados, burnout=0, qa_gastos=0):
    # aplica as regras de rolagem de dados
    dados_atuais = dados.copy()

    # verifica triscêndencia (antes de ajustes)
    tres_naturais = dados_atuais.count(3)
    is_triscendencia = (tres_naturais == 3)

    caos_fantasma = 0

    # aplica burnout
    if burnout > 0:
        is_triscendencia = False # burnout altera a rolagem natural
        burns_restantes = burnout
        for i in range(len(dados_atuais)):
            if dados_atuais[i] == 3 and burns_restantes > 0:
                dados_atuais[i] = 0 # 0 representa o dado burnout
                burns_restantes -= 1

        # se ainda sobrou burnout mas não há mais '3's, vira caos extra
        caos_fantasma = burns_restantes
    
    # aplica qa
    elif qa_gastos > 0:
        qa_restante = qa_gastos
        for i in range(len(dados_atuais)):
            if dados_atuais[i] != 3 and qa_restante > 0:
                dados_atuais[i] = 3
                qa_restante -= 1
    
    # calculo de caos e estabilidade
    tres_finais = dados_atuais.count(3)

    # exatamente tres 3s geram 0 caos, independentemente de qa ou burnout
    if tres_finais == 3:
        caos_total = 0
    else:
        # caos total são todos os dados que não são 3, mais o caos excedente de burnouts
        caos_total = sum(1 for d in dados_atuais if d != 3) + caos_fantasma
    
    # garante que a triscêndencia zere o caos
    if is_triscendencia and burnout == 0 and qa_gastos == 0:
        caos_total = 0
    
    return dados_atuais, caos_total, is_triscendencia, tres_finais

# cria a embed para o discord exibir os resultados da rolagem
def gerar_embed(dados, caos, is_triscendencia, burnout, qa_gastos):
    # cria a mensagem embed para o discord
    embed = discord.Embed(title="Rolagem - Triangle Agency", color=discord.Color.dark_blue())

    # formata os emojis
    emojis_rolagem = []
    for d in dados:
        if d == 1:
            emojis_rolagem.append(EMOJI_DADO_1)
        if d == 2:
            emojis_rolagem.append(EMOJI_DADO_2)
        if d == 3:
            emojis_rolagem.append(EMOJI_DADO_3)
        if d == 4:
            emojis_rolagem.append(EMOJI_DADO_4)     
        if d == 0:
            emojis_rolagem.append(EMOJI_DADO_BURNOUT)
    
    # checa triscendencia
    if is_triscendencia and burnout == 0 and qa_gastos == 0:
        embed.color = discord.Color.red()
        texto_triscendencia = (
            "Parabéns! O RH te escolheu para brilhar com sua Triscêndencia, "
            "não abuse muito, mas saiba que este é seu momento! "
            "Celebre sua vitória. **Uhul!**\n\n"
            "*Escolha um: All Hands, Circle Back ou Employee of the Moment.*"
        )
        embed.add_field(name="TRISCÊNDENCIA!", value=texto_triscendencia, inline=False)

    # checa estabilidade (3 três sem ser triscendencia)
    elif dados.count(3) == 3:
        embed.color = discord.Color.red()
        embed.add_field(name="Estabilidade", value="O resultado formou exatamente três 3s! Zero caos foi gerado.", inline=False)
    
    embed.add_field(name="Resultados", value=" ".join(emojis_rolagem), inline=False)

    # destaca o caos gerado
    if caos > 0:
        embed.add_field(name="Caos Gerado", value=f"**{caos}** {CAOS_EMOJI}", inline=False)
    else:
        embed.add_field(name="Caos Gerado", value="**0**", inline=False)

    # rodapé informativo
    if burnout > 0:
        embed.set_footer(text=f"Burnout aplicado: {burnout}")
    elif qa_gastos > 0:
        embed.set_footer(text=f"QA Gasto: {qa_gastos}")
    
    return embed

# modal para qa
class QAModal(discord.ui.Modal, title='Gastar Quality Assurances'):
    quantidade = discord.ui.TextInput(
        label='Quantos QA deseja gastar?',
        style=discord.TextStyle.short,
        required=True,
        default='1',
        max_length=1
    )

    # inicializa o modal com os dados originais da rolagem
    def __init__(self, dados_originais):
        super().__init__()
        self.dados_originais = dados_originais

    # trata o envio do modal
    async def on_submit(self, interaction: discord.Interaction):
        # valida a quantidade de qa inserida pelo usuário (deve ser um inteiro entre 1 e 6)
        try:
            qa_gastos = int(self.quantidade.value)
            if qa_gastos <= 0 or qa_gastos > 6:
                raise ValueError

        # caso o usuário insira um valor inválido, envia uma mensagem de erro
        except ValueError:
            await interaction.response.send_message("Valor inválido. Insira um número inteiro entre 1 e 6.", ephemeral=True)
            return
        
        # recalcula a rolagem com o QA gasto
        dados_finais, caos, is_triscendencia, _ = calcular_rolagem(self.dados_originais, burnout=0, qa_gastos=qa_gastos)

        # gera a nova embed com os resultados atualizados
        embed = gerar_embed(dados_finais, caos, is_triscendencia, burnout=0, qa_gastos=qa_gastos)

        # atualiza a mensagem removendo o botao e atualiando o embed
        await interaction.response.edit_message(embed=embed, view=None)

# view para o botao de qa
class QAView(discord.ui.View):
    def __init__(self, dados_originais):
        super().__init__(timeout=600) # o botao expira em 10 minutos
        self.dados_originais = dados_originais

    # botao para gastar qa
    @discord.ui.button(label="Gastar QA", style=discord.ButtonStyle.success, custom_id="btn_gastar_qa")
    async def btn_qa(self, interaction: discord.Interaction, button: discord.ui.Button):
        # abre o modal para o usuário digitar a quantidade
        await interaction.response.send_modal(QAModal(self.dados_originais))
    
# comando de barra para rolar os dados
@bot.tree.command(name="rolar", description="Rola 6 dados para o sistema Triangle Agency.")

# burnout opcional
@app_commands.describe(burnout="Quantidade de Burnout a aplicar (Opcional, padrão: 0)")

# comando de barra para rolar os dados
async def rolar(interaction: discord.Interaction, burnout: int = 0):
    # rola 6d4
    dados_rolados = [random.randint(1, 4) for _ in range(6)]
    
    # calcula os resultados iniciais
    dados_finais, caos, is_triscendencia, tres_finais = calcular_rolagem(dados_rolados, burnout=burnout, qa_gastos=0)
    embed = gerar_embed(dados_finais, caos, is_triscendencia, burnout, qa_gastos=0)

    # logica de interface, exibe o botão de qa apenas sem burnout e se o usuário ainda tiver dados para converter
    view = None

    if burnout == 0 and tres_finais < 6:
        view = QAView(dados_rolados)

    if view:
        await interaction.response.send_message(embed=embed, view=view)
    else:
        # se teve burnout ou tirou seis sucessos, não precisa de botão
        await interaction.response.send_message(embed=embed)

# inicia o bot
if __name__ == '__main__':
    bot.run(TOKEN)