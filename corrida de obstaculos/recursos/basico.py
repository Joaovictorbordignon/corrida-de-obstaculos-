import os, time, json
from datetime import datetime


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def aguarde(segundos):
    time.sleep(segundos)

def inicializarBancoDeDados():
    try:
        with open("base.dados", "r") as banco:
            # Apenas testa se o JSON está OK
            json.load(banco)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Banco de Dados Inexistente ou Inválido. Criando...")
        with open("base.dados", "w") as banco:
            json.dump({}, banco)

def escreverDados(nome, pontos):
    # Lê o banco
    try:
        with open("base.dados", "r") as banco:
            dadosDict = json.load(banco)
    except:
        dadosDict = {}

    # Adiciona novo dado
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)

    # Escreve no banco
    with open("base.dados", "w") as banco:
        json.dump(dadosDict, banco, indent=4)

    print("✅ Dados salvos com sucesso!")

# EXEMPLO DE USO
if __name__ == "__main__":
    inicializarBancoDeDados()

    nome = input("Digite seu nome: ")
    pontos = int(input("Digite sua pontuação: "))

    escreverDados(nome, pontos)
