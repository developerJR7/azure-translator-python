import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

KEY = os.getenv("TRANSLATOR_KEY")
ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
REGION = os.getenv("TRANSLATOR_REGION")

def translate_text(text, to_lang="en"):
    url = f"{ENDPOINT}/translate?api-version=3.0&to={to_lang}"
    headers = {
        "Ocp-Apim-Subscription-Key": KEY,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-Type": "application/json"
    }
    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    result = response.json()
    return result[0]["translations"][0]["text"]

def translate_file(file_path, to_lang="en"):
    if not os.path.exists(file_path):
        return "Arquivo não encontrado."
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    translated_text = translate_text(text, to_lang)
    
    output_file = file_path.replace(".txt", f"_traduzido_{to_lang}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(translated_text)
    
    return f"Tradução salva em {output_file}"

def translate_article(url, to_lang="en"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n")
    
    translated_text = translate_text(text, to_lang)
    
    output_file = "artigo_traduzido.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(translated_text)
    
    return f"Artigo traduzido e salvo em {output_file}"

if __name__ == "__main__":
    while True:
        choice = input(
            "Escolha o que deseja traduzir:\n"
            "t - texto digitado\n"
            "f - arquivo TXT\n"
            "u - URL de artigo\n"
            "sair - encerrar\n> "
        ).lower()
        
        if choice == "sair":
            break
        
        to_lang = input("Digite o idioma destino (ex: en, es, fr, pt): ").lower()
        
        if choice == "t":
            text = input("Digite o texto para traduzir: ")
            translated = translate_text(text, to_lang)
            print(f"Tradução:\n{translated}\n")
        
        elif choice == "f":
            file_path = input("Digite o caminho do arquivo TXT: ")
            result = translate_file(file_path, to_lang)
            print(result + "\n")
        
        elif choice == "u":
            url = input("Digite a URL do artigo: ")
            result = translate_article(url, to_lang)
            print(result + "\n")
        
        else:
            print("Opção inválida. Use 't', 'f', 'u' ou 'sair'.\n")
