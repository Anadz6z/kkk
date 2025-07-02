import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import asyncio
import os
import time
import random

class BrowserController:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.screenshot_counter = 0
        
    async def start(self):
        """Inicia o navegador com configurações anti-detecção"""
        try:
            # Configurações do Chrome para evitar detecção
            options = uc.ChromeOptions()
            
            # Configurações anti-bot
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Configurações de janela
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            
            # User agent personalizado
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Inicializar driver
            self.driver = uc.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Script para remover propriedades de webdriver
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Navegar para página inicial
            self.driver.get('https://www.google.com')
            
            # Aguardar carregamento
            await asyncio.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"Erro ao iniciar navegador: {e}")
            return False
    
    async def navigate_to(self, url):
        """Navega para uma URL específica"""
        if not self.driver:
            raise Exception("Navegador não iniciado")
        
        # Adicionar protocolo se necessário
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        self.driver.get(url)
        
        # Aguardar carregamento com delay aleatório
        await asyncio.sleep(random.uniform(2, 4))
        
        return True
    
    async def click_at(self, x, y):
        """Clica em coordenadas específicas"""
        if not self.driver:
            raise Exception("Navegador não iniciado")
        
        # Usar ActionChains para movimento mais natural
        actions = ActionChains(self.driver)
        
        # Mover para coordenadas com movimento suave
        actions.move_by_offset(x, y)
        actions.click()
        actions.perform()
        
        # Delay aleatório após clique
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        return True
    
    async def type_text(self, text):
        """Digite texto com timing humano"""
        if not self.driver:
            raise Exception("Navegador não iniciado")
        
        # Encontrar elemento ativo ou usar body
        try:
            active_element = self.driver.switch_to.active_element
        except:
            active_element = self.driver.find_element(By.TAG_NAME, "body")
        
        # Digitar com delays aleatórios entre caracteres
        for char in text:
            active_element.send_keys(char)
            await asyncio.sleep(random.uniform(0.05, 0.15))
        
        return True
    
    async def take_screenshot(self):
        """Captura screenshot e processa com Pillow"""
        if not self.driver:
            raise Exception("Navegador não iniciado")
        
        # Criar diretório se não existir
        os.makedirs('screenshots', exist_ok=True)
        
        # Nome do arquivo
        filename = f'screenshots/browser_{self.screenshot_counter}.png'
        self.screenshot_counter += 1
        
        # Capturar screenshot
        self.driver.save_screenshot(filename)
        
        # Processar com Pillow
        with Image.open(filename) as img:
            # Redimensionar se muito grande
            if img.width > 1920 or img.height > 1080:
                img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
            
            # Salvar imagem processada
            img.save(filename, 'PNG', optimize=True)
        
        return filename
    
    async def get_page_source(self):
        """Obtém o código fonte da página"""
        if not self.driver:
            raise Exception("Navegador não iniciado")
        
        return self.driver.page_source
    
    async def execute_ai_action(self, action):
        """Executa ação baseada na resposta da IA"""
        if not self.driver:
            raise Exception("Navegador não iniciado")
        
        action_type = action.get('type', '')
        
        try:
            if action_type == 'navigate':
                url = action.get('url', '')
                await self.navigate_to(url)
                return f"Navegado para: {url}"
            
            elif action_type == 'click':
                x = action.get('x', 0)
                y = action.get('y', 0)
                await self.click_at(x, y)
                return f"Clicado em ({x}, {y})"
            
            elif action_type == 'type':
                text = action.get('text', '')
                await self.type_text(text)
                return f"Digitado: {text}"
            
            elif action_type == 'search':
                query = action.get('query', '')
                # Procurar campo de busca
                search_selectors = [
                    'input[name="q"]',
                    'input[type="search"]',
                    'input[placeholder*="search" i]',
                    'input[placeholder*="buscar" i]'
                ]
                
                for selector in search_selectors:
                    try:
                        search_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                        search_box.clear()
                        await self.type_text(query)
                        search_box.send_keys(Keys.RETURN)
                        return f"Pesquisado: {query}"
                    except:
                        continue
                
                return "Campo de busca não encontrado"
            
            elif action_type == 'scroll':
                direction = action.get('direction', 'down')
                pixels = action.get('pixels', 500)
                
                if direction == 'down':
                    self.driver.execute_script(f"window.scrollBy(0, {pixels});")
                else:
                    self.driver.execute_script(f"window.scrollBy(0, -{pixels});")
                
                await asyncio.sleep(1)
                return f"Rolado {direction} {pixels}px"
            
            else:
                return f"Ação não reconhecida: {action_type}"
                
        except Exception as e:
            return f"Erro ao executar ação: {str(e)}"
    
    async def close(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
        
        return True