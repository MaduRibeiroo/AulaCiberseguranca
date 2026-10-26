#!/usr/bin/env python3
# 12o FIPPETEC - Introducao a Ciberseguranca
# Material didatico. Python 3.8+; bibliotecas padrao apenas.

import hashlib
import hmac
import secrets
import sys
from pathlib import Path
from urllib.parse import urlsplit

PASTA = Path.home() / "FIPPETEC_LAB"
ITERACOES = 200_000


def titulo(nome):
    print("\n" + "=" * 62)
    print(nome)
    print("=" * 62)


def pausa():
    input("\nPressione Enter para voltar ao menu...")


def teste_ambiente():
    titulo("TESTE DO LABORATORIO - 12o FIPPETEC")
    print("Python:", sys.version.split()[0])
    print("Executavel:", sys.executable)
    print("Pasta para os arquivos:", PASTA)
    erros = []

    if sys.version_info >= (3, 8):
        print("[OK] Versao compativel (3.8 ou superior)")
    else:
        erros.append("Python abaixo da versao 3.8")
        print("[FALHA] Recomenda-se Python 3.8 ou superior")

    try:
        print("[OK] SHA-256:", hashlib.sha256(b"teste").hexdigest()[:16] + "...")
        senha = b"senha-ficticia"
        salt = secrets.token_bytes(16)
        derivada = hashlib.pbkdf2_hmac("sha256", senha, salt, ITERACOES)
        assert hmac.compare_digest(derivada, hashlib.pbkdf2_hmac("sha256", senha, salt, ITERACOES))
        print("[OK] Salt aleatorio, PBKDF2 e verificacao de senha")
    except Exception as exc:
        erros.append("Hash e autenticacao: " + str(exc))
        print("[FALHA] Funcoes de hash/autenticacao:", exc)

    try:
        PASTA.mkdir(parents=True, exist_ok=True)
        arq = PASTA / "teste_escrita.txt"
        arq.write_text("Teste de leitura e escrita - FIPPETEC.\n", encoding="utf-8")
        assert "FIPPETEC" in arq.read_text(encoding="utf-8")
        arq.unlink()
        print("[OK] Criar, ler e excluir arquivos na pasta do usuario")
    except Exception as exc:
        erros.append("Acesso a arquivos: " + str(exc))
        print("[FALHA] Permissao de escrita/leitura:", exc)

    try:
        from cryptography.fernet import Fernet  # opcional
        Fernet.generate_key()
        print("[EXTRA] Biblioteca 'cryptography' instalada: criptografia real disponivel")
    except Exception:
        print("[EXTRA] Biblioteca 'cryptography' nao encontrada (nao e obrigatoria)")

    print("\nRESULTADO:")
    if erros:
        print("O ambiente precisa de ajustes:")
        for erro in erros:
            print(" -", erro)
    else:
        print("APROVADO para as atividades basicas, sem internet e sem instalacoes extras.")
    return not erros


def senhas():
    titulo("1. SENHAS FRACAS E FRASES-SENHA")
    senha = input("Digite uma senha: ")
    pontos = 0
    if len(senha) >= 12:
        pontos += 1
    if any(c.isupper() for c in senha):
        pontos += 1
    if any(c.islower() for c in senha):
        pontos += 1
    if any(c.isdigit() for c in senha):
        pontos += 1
    if any(not c.isalnum() for c in senha):
        pontos += 1
    print("Pontuação:", pontos)
    if pontos <= 2:
        print("Senha fraca!")
    elif pontos <= 4:
        print("Senha média!")
    else :
        print("Senha forte!")
    pausa()


def hashes():
    titulo("2. HASH - IMPRESSAO DIGITAL DE UM TEXTO")
    texto1 = input("Digite um texto (ou Enter para 'ola'): ") or "ola"
    texto2 = input("Digite uma pequena variacao (ou Enter para 'Ola'): ") or "Ola"
    hash1 = hashlib.sha256(texto1.encode("utf-8")).hexdigest()
    hash2 = hashlib.sha256(texto2.encode("utf-8")).hexdigest()
    print("Hash 1:", hash1)
    print("Hash 2:", hash2)
    print("Sao iguais?", hmac.compare_digest(hash1, hash2))
    #print("Hash nao e criptografia reversivel.")
    #print("SHA-256 puro nao e recomendado para armazenar senhas.")
    pausa()


def cifra_cesar(texto, deslocamento):
    resultado = []
    for char in texto:
        if "A" <= char <= "Z":
            resultado.append(chr((ord(char) - ord("A") + deslocamento) % 26 + ord("A")))
        else:
            resultado.append(char)
    return "".join(resultado)


def criptografia():
    titulo("6. CRIPTOGRAFIA - DEMONSTRACAO")
    texto = (input("Mensagem ficticia (Enter = SEGREDO): ") or "SEGREDO").upper()
    cifrado = cifra_cesar(texto, 3)
    print("Texto original:", texto)
    print("Texto cifrado (+3):", cifrado)
    print("Texto decifrado (-3):", cifra_cesar(cifrado, -3))
    try:
        from cryptography.fernet import Fernet
    except Exception:
        print("Criptografia moderna extra indisponivel: biblioteca opcional nao instalada.")
    else:
        chave = Fernet.generate_key()
        sistema = Fernet(chave)
        token = sistema.encrypt(texto.encode("utf-8"))
        print("\nEXTRA - Criptografia autenticada com Fernet:")
        print("Texto cifrado (inicio):", token.decode("ascii")[:50] + "...")
        print("Decifrado:", sistema.decrypt(token).decode("utf-8"))
        print("Importante: proteger e guardar a chave de forma segura.")
    pausa()


def menu():
    acoes = {
        "1": senhas,
        "2": hashes,
        "3": criptografia,
    }
    while True:
        titulo("12o FIPPETEC - INTRODUCAO A CIBERSEGURANCA")
        print("1 - Senhas e autenticacao (conceitos)")
        print("2 - Hash SHA-256")
        print("3 - Criptografia didatica (+ extra se disponivel)")
        print("T - Testar compatibilidade do laboratorio")
        print("0 - Sair")
        escolha = input("Escolha: ").strip().lower()
        if escolha == "0":
            print("Ate a proxima!")
            break
        elif escolha == "t":
            teste_ambiente()
            pausa()
        elif escolha in acoes:
            try:
                acoes[escolha]()
            except OSError as exc:
                print("Erro de acesso a arquivos:", exc)
                pausa()
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--teste":
            sys.exit(0 if teste_ambiente() else 1)
        if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
            print("Use: python fippetec_ciberseguranca.py [--teste]")
            sys.exit(0)
        menu()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
