import google.generativeai as genai
import json
import re
from bs4 import BeautifulSoup

class AIHandler:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def process_command(self, command, page_source, screenshot_path):
        """Processa comando do usuário usando Gemini AI"""
        
        # Extrair texto relevante da página
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Remover scripts e estilos
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extrair texto visível
        visible_text = soup.get_text()
        
        # Limitar tamanho do texto
        visible_text = visible_text[:2000] if len(visible_text) > 2000 else visible_text
        
        # Prompt para a IA
        prompt = f"""
        Você é um assistente que controla um navegador web. Analise o comando do usuário e a página atual, então retorne uma ação em formato JSON.

        COMANDO DO USUÁRIO: {command}

        CONTEÚDO DA PÁGINA ATUAL:
        {visible_text}

        URL ATUAL: {self._extract_url_from_source(page_source)}

        AÇÕES DISPONÍVEIS:
        1. navigate - Navegar para URL
        2. click - Clicar em coordenadas
        3. type - Digitar texto
        4. search - Pesquisar (encontra campo de busca automaticamente)
        5. scroll - Rolar página

        EXEMPLOS DE COMANDOS E RESPOSTAS:

        Comando: "vá para o youtube"
        Resposta: {{"type": "navigate", "url": "https://www.youtube.com"}}

        Comando: "pesquise por gatos"
        Resposta: {{"type": "search", "query": "gatos"}}

        Comando: "digite olá mundo"
        Resposta: {{"type": "type", "text": "olá mundo"}}

        Comando: "role para baixo"
        Resposta: {{"type": "scroll", "direction": "down", "pixels": 500}}

        Comando: "clique no meio da tela"
        Resposta: {{"type": "click", "x": 960, "y": 540}}

        IMPORTANTE:
        - Retorne APENAS o JSON, sem explicações
        - Use URLs completas (com https://)
        - Para sites brasileiros populares, use os domínios corretos (.com.br quando aplicável)
        - Seja inteligente ao interpretar comandos em português

        RESPONDA APENAS COM O JSON:
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extrair JSON da resposta
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                action = json.loads(json_str)
                return action
            else:
                # Fallback se não conseguir extrair JSON
                return {"type": "error", "message": "Não foi possível interpretar o comando"}
                
        except Exception as e:
            print(f"Erro na IA: {e}")
            return {"type": "error", "message": f"Erro na IA: {str(e)}"}
    
    def _extract_url_from_source(self, page_source):
        """Extrai URL atual do código fonte"""
        try:
            # Procurar por canonical URL ou usar método alternativo
            soup = BeautifulSoup(page_source, 'html.parser')
            canonical = soup.find('link', {'rel': 'canonical'})
            if canonical and canonical.get('href'):
                return canonical['href']
            
            # Fallback
            return "URL não detectada"
        except:
            return "URL não detectada"