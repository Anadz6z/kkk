import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio
from browser_controller import BrowserController
from ai_handler import AIHandler

# Carregar variáveis de ambiente
load_dotenv()

# Configurar intents do Discord
intents = discord.Intents.default()
intents.message_content = True

# Criar bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Instâncias globais
browser_controller = None
ai_handler = None

@bot.event
async def on_ready():
    global ai_handler
    print(f'{bot.user} está online!')
    
    # Inicializar AI Handler
    ai_handler = AIHandler(os.getenv('GEMINI_API_KEY'))
    print('Bot configurado e pronto para uso!')

@bot.command(name='web')
async def start_browser(ctx):
    """Inicia o navegador e mostra a tela atual"""
    global browser_controller
    
    try:
        await ctx.send("🌐 Iniciando navegador...")
        
        # Inicializar controlador do navegador
        browser_controller = BrowserController()
        await browser_controller.start()
        
        # Capturar screenshot inicial
        screenshot_path = await browser_controller.take_screenshot()
        
        # Enviar screenshot
        with open(screenshot_path, 'rb') as f:
            file = discord.File(f, 'browser.png')
            embed = discord.Embed(
                title="🌐 Navegador Iniciado",
                description="Use comandos como: `!go <url>`, `!click <x> <y>`, `!type <texto>`, `!ai <comando>`",
                color=0x00ff00
            )
            embed.set_image(url="attachment://browser.png")
            await ctx.send(embed=embed, file=file)
            
    except Exception as e:
        await ctx.send(f"❌ Erro ao iniciar navegador: {str(e)}")

@bot.command(name='go')
async def navigate_to(ctx, url: str):
    """Navega para uma URL específica"""
    global browser_controller
    
    if not browser_controller:
        await ctx.send("❌ Navegador não iniciado. Use `!web` primeiro.")
        return
    
    try:
        await ctx.send(f"🔄 Navegando para: {url}")
        
        await browser_controller.navigate_to(url)
        await asyncio.sleep(3)  # Aguardar carregamento
        
        screenshot_path = await browser_controller.take_screenshot()
        
        with open(screenshot_path, 'rb') as f:
            file = discord.File(f, 'browser.png')
            embed = discord.Embed(
                title=f"📍 Navegando: {url}",
                color=0x0099ff
            )
            embed.set_image(url="attachment://browser.png")
            await ctx.send(embed=embed, file=file)
            
    except Exception as e:
        await ctx.send(f"❌ Erro ao navegar: {str(e)}")

@bot.command(name='click')
async def click_element(ctx, x: int, y: int):
    """Clica em coordenadas específicas"""
    global browser_controller
    
    if not browser_controller:
        await ctx.send("❌ Navegador não iniciado. Use `!web` primeiro.")
        return
    
    try:
        await browser_controller.click_at(x, y)
        await asyncio.sleep(2)
        
        screenshot_path = await browser_controller.take_screenshot()
        
        with open(screenshot_path, 'rb') as f:
            file = discord.File(f, 'browser.png')
            embed = discord.Embed(
                title=f"👆 Clicado em ({x}, {y})",
                color=0xff9900
            )
            embed.set_image(url="attachment://browser.png")
            await ctx.send(embed=embed, file=file)
            
    except Exception as e:
        await ctx.send(f"❌ Erro ao clicar: {str(e)}")

@bot.command(name='type')
async def type_text(ctx, *, text: str):
    """Digite texto no elemento focado"""
    global browser_controller
    
    if not browser_controller:
        await ctx.send("❌ Navegador não iniciado. Use `!web` primeiro.")
        return
    
    try:
        await browser_controller.type_text(text)
        await asyncio.sleep(1)
        
        screenshot_path = await browser_controller.take_screenshot()
        
        with open(screenshot_path, 'rb') as f:
            file = discord.File(f, 'browser.png')
            embed = discord.Embed(
                title=f"⌨️ Digitado: {text}",
                color=0x9900ff
            )
            embed.set_image(url="attachment://browser.png")
            await ctx.send(embed=embed, file=file)
            
    except Exception as e:
        await ctx.send(f"❌ Erro ao digitar: {str(e)}")

@bot.command(name='ai')
async def ai_command(ctx, *, command: str):
    """Usa IA para interpretar comando e executar ação no navegador"""
    global browser_controller, ai_handler
    
    if not browser_controller:
        await ctx.send("❌ Navegador não iniciado. Use `!web` primeiro.")
        return
    
    if not ai_handler:
        await ctx.send("❌ IA não configurada.")
        return
    
    try:
        await ctx.send(f"🤖 Processando comando: {command}")
        
        # Capturar estado atual da página
        screenshot_path = await browser_controller.take_screenshot()
        page_source = await browser_controller.get_page_source()
        
        # Processar comando com IA
        action = await ai_handler.process_command(command, page_source, screenshot_path)
        
        # Executar ação
        result = await browser_controller.execute_ai_action(action)
        
        # Capturar resultado
        new_screenshot_path = await browser_controller.take_screenshot()
        
        with open(new_screenshot_path, 'rb') as f:
            file = discord.File(f, 'browser.png')
            embed = discord.Embed(
                title=f"🤖 IA Executou: {command}",
                description=f"Ação: {action.get('type', 'unknown')}\nResultado: {result}",
                color=0x00ffff
            )
            embed.set_image(url="attachment://browser.png")
            await ctx.send(embed=embed, file=file)
            
    except Exception as e:
        await ctx.send(f"❌ Erro na IA: {str(e)}")

@bot.command(name='screenshot')
async def take_screenshot(ctx):
    """Captura screenshot atual do navegador"""
    global browser_controller
    
    if not browser_controller:
        await ctx.send("❌ Navegador não iniciado. Use `!web` primeiro.")
        return
    
    try:
        screenshot_path = await browser_controller.take_screenshot()
        
        with open(screenshot_path, 'rb') as f:
            file = discord.File(f, 'browser.png')
            embed = discord.Embed(
                title="📸 Screenshot Atual",
                color=0x00ff00
            )
            embed.set_image(url="attachment://browser.png")
            await ctx.send(embed=embed, file=file)
            
    except Exception as e:
        await ctx.send(f"❌ Erro ao capturar screenshot: {str(e)}")

@bot.command(name='close')
async def close_browser(ctx):
    """Fecha o navegador"""
    global browser_controller
    
    if browser_controller:
        await browser_controller.close()
        browser_controller = None
        await ctx.send("🔴 Navegador fechado.")
    else:
        await ctx.send("❌ Nenhum navegador ativo.")

@bot.command(name='help_web')
async def help_command(ctx):
    """Mostra comandos disponíveis"""
    embed = discord.Embed(
        title="🤖 Comandos do Bot Navegador",
        description="Lista de comandos disponíveis:",
        color=0x0099ff
    )
    
    commands_list = [
        ("!web", "Inicia o navegador"),
        ("!go <url>", "Navega para uma URL"),
        ("!click <x> <y>", "Clica em coordenadas"),
        ("!type <texto>", "Digite texto"),
        ("!ai <comando>", "Comando de IA (ex: 'vá para o YouTube')"),
        ("!screenshot", "Captura screenshot"),
        ("!close", "Fecha o navegador"),
        ("!help_web", "Mostra esta ajuda")
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    await ctx.send(embed=embed)

# Executar bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Token do Discord não encontrado no arquivo .env")
    else:
        bot.run(token)