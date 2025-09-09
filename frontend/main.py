import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading

# --- FUNÇÕES DE LÓGICA DO BACKEND ---

processo_servidor = None
processo_escritor = None

def adicionar_log(mensagem):
    """ Adiciona uma mensagem na área de log de forma segura para threads """
    log_area.configure(state='normal')
    log_area.insert(tk.END, mensagem + "\n")
    log_area.configure(state='disabled')
    log_area.see(tk.END) 

def ler_saida_processo(processo, nome_processo):
    """ Função para ler a saída de um processo em uma thread separada para não travar a interface """
    for linha in iter(processo.stdout.readline, ''):
        adicionar_log(f"[{nome_processo}] {linha.strip()}")
    processo.stdout.close()
    adicionar_log(f">>> {nome_processo} encerrou. <<<")

def executar_ipc():
    """ Função principal que é chamada pelo botão e decide qual backend executar """
    modo = modo_ipc.get()
    mensagem = campo_mensagem.get()
    if not mensagem:
        mensagem = "Mensagem de teste"

    adicionar_log(f"\n>>> EXECUTANDO MODO: {modo.upper()} <<<")

    try:
        if modo == "pipes":
            pasta_dos_executaveis = "../executaveis/"
            caminho_completo_pai = "../executaveis/backendpipe.exe"
            
            resultado = subprocess.run(
                [caminho_completo_pai, mensagem], 
                capture_output=True, text=True, check=True, encoding="utf-8",
                cwd=pasta_dos_executaveis 
            )
            adicionar_log(resultado.stdout.strip())
        
        elif modo == "sockets":
            global processo_servidor
            if not processo_servidor or processo_servidor.poll() is not None:
                adicionar_log(">>> Iniciando o Servidor de Socket...")
                caminho_servidor = "../executaveis/socketservidor.exe"
                processo_servidor = subprocess.Popen(
                    [caminho_servidor],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW
                )
                thread = threading.Thread(target=ler_saida_processo, args=(processo_servidor, "Servidor"))
                thread.daemon = True
                thread.start()
                adicionar_log(">>> Servidor no ar. Agora, digite uma mensagem e clique em 'Executar Ação' novamente para enviar como cliente.")
            else:
                adicionar_log(">>> Conectando o Cliente de Socket...")
                caminho_cliente = "../executaveis/socketcliente.exe"
                resultado = subprocess.run(
                    [caminho_cliente, mensagem],
                    capture_output=True, text=True, check=True, encoding="utf-8"
                )
                adicionar_log(resultado.stdout.strip())

        elif modo == "shared_memory":
            global processo_escritor
            if not processo_escritor or processo_escritor.poll() is not None:
                adicionar_log(">>> Iniciando o Escritor na Memória...")
                caminho_escritor = "../executaveis/memoriaesc.exe"
                processo_escritor = subprocess.Popen(
                    [caminho_escritor],
                    stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW
                )
                thread = threading.Thread(target=ler_saida_processo, args=(processo_escritor, "Escritor"))
                thread.daemon = True
                thread.start()
                adicionar_log(">>> Escritor no ar. Clique em 'Executar Ação' novamente para ler a memória.")
            else:
                adicionar_log(">>> Executando o Leitor da Memória...")
                caminho_leitor = "../executaveis/memorialeitor.exe"
                resultado = subprocess.run(
                    [caminho_leitor], capture_output=True, text=True, check=True, encoding="utf-8"
                )
                for linha in resultado.stdout.strip().split('\n'):
                    adicionar_log(f"[Leitor] {linha}")

    except FileNotFoundError as e:
        adicionar_log(f"ERRO: Executável não encontrado! Verifique se o nome e o caminho estão corretos no script Python e se o arquivo existe na pasta 'executaveis'. Arquivo: {e.filename}")
    except Exception as e:
        adicionar_log(f"Ocorreu um erro: {e}")

# CONFIGURAÇÃO DA JANELA GRÁFICA
janela = tk.Tk()
janela.title("Projeto Final - Comunicação Entre Processos")
janela.geometry("800x600")

frame_controle = tk.Frame(janela)
frame_controle.pack(pady=10, padx=10, fill='x')

tk.Label(frame_controle, text="Selecione o Modo de IPC:").pack(side=tk.LEFT, padx=5)
modo_ipc = tk.StringVar(value="pipes")
opcoes = [("Pipes", "pipes"), ("Sockets", "sockets"), ("Memória Compartilhada", "shared_memory")]
for texto, modo in opcoes:
    tk.Radiobutton(frame_controle, text=texto, variable=modo_ipc, value=modo).pack(side=tk.LEFT)

frame_acao = tk.Frame(janela)
frame_acao.pack(pady=10, padx=10, fill='x')

tk.Label(frame_acao, text="Mensagem:").pack(side=tk.LEFT, padx=5)
campo_mensagem = tk.Entry(frame_acao, width=50)
campo_mensagem.pack(side=tk.LEFT, expand=True, fill='x', padx=5)
botao_executar = tk.Button(frame_acao, text="Executar Ação", command=executar_ipc)
botao_executar.pack(side=tk.LEFT, padx=5)

log_area = scrolledtext.ScrolledText(janela, wrap=tk.WORD, height=25)
log_area.pack(pady=10, padx=10, expand=True, fill='both')
log_area.configure(state='disabled')

def ao_fechar():
    """ Garante que os processos em segundo plano sejam encerrados ao fechar a janela """
    if messagebox.askokcancel("Sair", "Você quer sair? Isso encerrará todos os processos em segundo plano."):
        if processo_servidor: processo_servidor.terminate()
        if processo_escritor: processo_escritor.terminate()
        janela.destroy()

janela.protocol("WM_DELETE_WINDOW", ao_fechar)
janela.mainloop()
