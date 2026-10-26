import os
import hashlib
import hmac
from cryptography.fernet import Fernet

def hashes():
    print("HASH")
    texto1 =  input("Digite um texto ou (Enter para 'Ola'): ") or "Ola"
    texto2 = input("Digite uma pequena variação do texto anterior (Enter para 'ola'): ") or "ola"
    hash1 = hashlib.sha256(texto1.encode("utf-8")).hexdigest()
    hash2 = hashlib.sha256(texto2.encode("utf-8")).hexdigest()
    print("Hash1: ",hash1)
    print("Hash2: ",hash2)
    print("Sao iguais?", hmac.compare_digest(hash1,hash2))


def espera():
    input("Aperte Enter para continuar")
    os.system("cls")

def senhas():
    senha = input("Digite uma senha: ")
    pontos = 0

    if len(senha) >= 12: # tem 12 ou mais caracteres?
        pontos += 1

    if any(c.isupper() for c in senha ): # tem alguma letra maiuscula?
        pontos+=1

    if any(c.islower() for c in senha ): # tem alguma letra minuscula?
            pontos+=1
    if any(c.isdigit() for c in senha): # se tem algum digito?
        pontos+=1
    if any(not c.isalnum() for c in senha): # tem algum caracter q não é numero nem letra?
        pontos+=1
    print("Pontuação: ", pontos)

    if len(senha)<8:
        print("É recomendado que a senha tenha mais de 7 caractes")
        pontos-=1

    if pontos <=2:
        print("Senha fraca")
    elif pontos<=4:
        print("Senha media")
    else:
        print("Senha Forte")



from cryptography.fernet import Fernet

def cifra_cesar(texto,deslocamento):
    resultado = []
    for char in texto:
        if "A" <= char <= "Z":
            resultado.append(chr((ord(char) - ord("A") + deslocamento) % 26 + ord("A") ))
        else:
            resultado.append(char)
    return "".join(resultado)


def cifra():
    texto =(input("Mensagem ficticia (Enter = SEGREDO): ")or "SEGREDO").upper()
    cifrado = cifra_cesar(texto,3)
    print("CIFRA DE CESAR")
    print("Texto original: ", texto)
    print("Texto cifrado (+3):", cifrado)
    print("Texto decifrado (-3):", cifra_cesar(cifrado,-3) )

    chave = Fernet.generate_key()
    sistema= Fernet(chave)
    token = sistema.encrypt(texto.encode("utf-8"))
    print("CRIPTOGRAFIA com Fernet")
    print("Texto cifrado:", token.decode("ascii")[:50] + "...")
    print("Decifrado", sistema.decrypt(token).decode("utf-8"))
    print("Se perder a chave já era")
    


def menu():
    acoes={
        "1": senhas,
        "2":hashes,
        "3":cifra
    }
    opcao=""
    while opcao != "0":
        os.system("cls")
        if opcao in acoes:
            acoes[opcao]()
            espera()

        print("1 - Verificador de senhas")
        print("2 - HASHES")
        print("3 - CIFRA")
        opcao =input("Digite a poçao desejada ou 0 para sair: ")


if __name__ == "__main__":
    menu()