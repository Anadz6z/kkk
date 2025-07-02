#!/usr/bin/env python3
"""
Script para executar o bot Discord com verificações de dependências
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def install_requirements():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        sys.exit(1)

def check_env_file():
    """Verifica se o arquivo .env existe e tem as variáveis necessárias"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ Arquivo .env não encontrado")
        print("📝 Criando arquivo .env de exemplo...")
        
        with open(".env", "w") as f:
            f.write("DISCORD_TOKEN=seu_token_do_discord_aqui\n")
            f.write("GEMINI_API_KEY=sua_chave_da_api_gemini_aqui\n")
        
        print("✅ Arquivo .env criado. Configure suas chaves API antes de continuar.")
        return False
    
    # Verificar se as variáveis estão configuradas
    with open(".env", "r") as f:
        content = f.read()
        
    if "seu_token_do_discord_aqui" in content or "sua_chave_da_api_gemini_aqui" in content:
        print("❌ Configure suas chaves API no arquivo .env")
        return False
    
    print("✅ Arquivo .env configurado")
    return True

def create_directories():
    """Cria diretórios necessários"""
    os.makedirs("screenshots", exist_ok=True)
    print("✅ Diretórios criados")

def main():
    """Função principal"""
    print("🤖 Iniciando Bot Discord com IA Gemini")
    print("=" * 50)
    
    # Verificações
    check_python_version()
    
    # Instalar dependências
    install_requirements()
    
    # Verificar configuração
    if not check_env_file():
        print("\n📋 Para configurar o bot:")
        print("1. Obtenha um token do Discord em: https://discord.com/developers/applications")
        print("2. Obtenha uma chave API do Gemini em: https://makersuite.google.com/app/apikey")
        print("3. Configure as chaves no arquivo .env")
        print("4. Execute novamente este script")
        return
    
    # Criar diretórios
    create_directories()
    
    # Executar bot
    print("\n🚀 Iniciando bot...")
    print("=" * 50)
    
    try:
        import bot
    except KeyboardInterrupt:
        print("\n👋 Bot encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao executar bot: {e}")

if __name__ == "__main__":
    main()