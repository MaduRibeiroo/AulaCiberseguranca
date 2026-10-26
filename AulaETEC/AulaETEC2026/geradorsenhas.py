import tkinter as tk
import secrets
import string

# Cores da interface
FUNDO = "#101827"
PAINEL = "#1E293B"
BRANCO = "#F8FAFC"
VERDE = "#22C55E"


def gerar_senha():
    tamanho = tamanho_var.get()

    # Grupos de caracteres disponíveis
    grupos = [string.ascii_lowercase, string.ascii_uppercase]

    if numeros_var.get():
        grupos.append(string.digits)

    if simbolos_var.get():
        grupos.append("!@#$%&*?")

    # Garante pelo menos um caractere de cada grupo
    senha = [secrets.choice(grupo) for grupo in grupos]

    caracteres = "".join(grupos)

    while len(senha) < tamanho:
        senha.append(secrets.choice(caracteres))

    # Embaralha a senha com aleatoriedade segura
    for i in range(len(senha) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        senha[i], senha[j] = senha[j], senha[i]

    senha_var.set("".join(senha))

    # Classificação didática da força
    if tamanho < 12:
        nivel = "SENHA FRACA"
        cor = "#EF4444"
        dica = "Use pelo menos 12 caracteres."

    elif tamanho >= 16 and len(grupos) >= 3:
        nivel = "SENHA FORTE"
        cor = "#22C55E"
        dica = "Boa combinação de tamanho e caracteres!"

    elif tamanho >= 20:
        nivel = "SENHA FORTE"
        cor = "#22C55E"
        dica = "Senha longa e gerada aleatoriamente!"

    else:
        nivel = "SENHA MÉDIA"
        cor = "#F59E0B"
        dica = "Aumente o tamanho ou use números e símbolos."

    resultado.config(text=nivel, fg=cor)
    recomendacao.config(text=dica)
    aviso_copia.config(text="")


def copiar_senha():
    senha = senha_var.get()

    if senha:
        janela.clipboard_clear()
        janela.clipboard_append(senha)
        aviso_copia.config(text="Senha copiada!", fg=VERDE)


# Janela principal
janela = tk.Tk()
janela.title("Gerador de Senhas - FIPPETEC")
janela.geometry("460x510")
janela.resizable(False, False)
janela.configure(bg=FUNDO)

# Título
tk.Label(
    janela,
    text="🔐 GERADOR DE SENHAS",
    font=("Arial", 18, "bold"),
    bg=FUNDO,
    fg=BRANCO
).pack(pady=(25, 5))

tk.Label(
    janela,
    text="Crie senhas aleatórias e seguras",
    font=("Arial", 10),
    bg=FUNDO,
    fg="#94A3B8"
).pack(pady=(0, 20))

# Área da senha
senha_var = tk.StringVar()

tk.Entry(
    janela,
    textvariable=senha_var,
    font=("Consolas", 16),
    justify="center",
    bg=PAINEL,
    fg=BRANCO,
    insertbackground=BRANCO,
    relief="flat",
    width=32
).pack(ipady=12, padx=20)

tk.Button(
    janela,
    text="Copiar senha",
    command=copiar_senha,
    bg="#334155",
    fg=BRANCO,
    relief="flat",
    font=("Arial", 10),
    cursor="hand2"
).pack(pady=(10, 0))

aviso_copia = tk.Label(
    janela, text="", bg=FUNDO, fg=VERDE
)
aviso_copia.pack()

# Controle de tamanho
tamanho_var = tk.IntVar(value=16)

tk.Label(
    janela,
    text="Tamanho da senha",
    bg=FUNDO,
    fg=BRANCO,
    font=("Arial", 11, "bold")
).pack(pady=(15, 0))

tk.Scale(
    janela,
    from_=4,
    to=32,
    orient="horizontal",
    variable=tamanho_var,
    bg=FUNDO,
    fg=BRANCO,
    troughcolor=PAINEL,
    highlightthickness=0,
    length=320
).pack()

# Opções de caracteres
numeros_var = tk.BooleanVar(value=True)
simbolos_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    janela,
    text="Incluir números (0-9)",
    variable=numeros_var,
    bg=FUNDO,
    fg=BRANCO,
    selectcolor=PAINEL,
    activebackground=FUNDO,
    activeforeground=BRANCO
).pack(anchor="w", padx=75)

tk.Checkbutton(
    janela,
    text="Incluir símbolos (!@#$%)",
    variable=simbolos_var,
    bg=FUNDO,
    fg=BRANCO,
    selectcolor=PAINEL,
    activebackground=FUNDO,
    activeforeground=BRANCO
).pack(anchor="w", padx=75)

# Botão gerar
tk.Button(
    janela,
    text="GERAR NOVA SENHA",
    command=gerar_senha,
    font=("Arial", 12, "bold"),
    bg="#2563EB",
    fg="white",
    relief="flat",
    cursor="hand2",
    width=28,
    height=2
).pack(pady=20)

# Indicador de força
resultado = tk.Label(
    janela,
    text="",
    font=("Arial", 13, "bold"),
    bg=FUNDO
)
resultado.pack()

recomendacao = tk.Label(
    janela,
    text="",
    font=("Arial", 10),
    bg=FUNDO,
    fg="#94A3B8"
)
recomendacao.pack(pady=5)

# Gerar a primeira senha automaticamente
gerar_senha()

janela.mainloop()
