# Bot Discord com IA Gemini e Controle de Navegador

Este bot Discord permite controlar um navegador web através de comandos, usando IA Gemini para interpretar comandos em linguagem natural.

## Funcionalidades

- 🌐 Controle completo de navegador web
- 🤖 IA Gemini para interpretar comandos
- 📸 Screenshots automáticos
- 🔍 Webscraping inteligente
- 🛡️ Proteção anti-captcha e anti-detecção
- 🎯 Cliques precisos e digitação natural

## Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env`:

```env
DISCORD_TOKEN=seu_token_do_discord_aqui
GEMINI_API_KEY=sua_chave_da_api_gemini_aqui
```

### 3. Obter Tokens

#### Discord Bot Token:
1. Vá para https://discord.com/developers/applications
2. Crie uma nova aplicação
3. Vá para "Bot" e crie um bot
4. Copie o token

#### Gemini API Key:
1. Vá para https://makersuite.google.com/app/apikey
2. Crie uma nova chave API
3. Copie a chave

### 4. Executar o Bot

```bash
python bot.py
```

## Comandos Disponíveis

### Comandos Básicos
- `!web` - Inicia o navegador
- `!go <url>` - Navega para uma URL
- `!click <x> <y>` - Clica em coordenadas específicas
- `!type <texto>` - Digite texto
- `!screenshot` - Captura screenshot atual
- `!close` - Fecha o navegador
- `!help_web` - Mostra ajuda

### Comando de IA
- `!ai <comando>` - Usa IA para interpretar e executar comandos

#### Exemplos de comandos de IA:
- `!ai vá para o youtube`
- `!ai pesquise por música brasileira`
- `!ai role a página para baixo`
- `!ai clique no primeiro resultado`
- `!ai digite meu nome é João`

## Recursos Anti-Detecção

O bot inclui várias técnicas para evitar detecção:

- ✅ User-Agent personalizado
- ✅ Remoção de propriedades webdriver
- ✅ Delays aleatórios entre ações
- ✅ Movimento natural do mouse
- ✅ Digitação com timing humano
- ✅ Undetected Chrome Driver

## Estrutura do Projeto

```
├── bot.py                 # Bot principal do Discord
├── browser_controller.py  # Controlador do navegador
├── ai_handler.py         # Handler da IA Gemini
├── requirements.txt      # Dependências
├── .env                 # Variáveis de ambiente
└── screenshots/         # Pasta para screenshots
```

## Exemplo de Uso

1. Digite `!web` para iniciar o navegador
2. Use `!ai vá para o youtube` para navegar
3. Use `!ai pesquise por música` para pesquisar
4. Use `!screenshot` para ver o resultado

## Troubleshooting

### Erro de ChromeDriver
Se houver problemas com o ChromeDriver, ele será baixado automaticamente pelo webdriver-manager.

### Erro de API Gemini
Verifique se sua chave API está correta e tem créditos disponíveis.

### Bot não responde
Verifique se o token do Discord está correto e o bot tem as permissões necessárias no servidor.

## Permissões Necessárias do Bot

- Enviar mensagens
- Anexar arquivos
- Usar comandos de barra
- Ler histórico de mensagens

## Aviso Legal

Este bot é para fins educacionais. Respeite os termos de serviço dos sites que visitar e use com responsabilidade.