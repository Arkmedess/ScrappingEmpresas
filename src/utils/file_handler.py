from tkinter import Tk, filedialog
import pandas as pd
import os

def selecionar_arquivo_entrada(titulo: str = "Selecione o arquivo Excel", pasta_inicial: str = "~\\Desktop"):
    root = Tk()
    root.withdraw()
    arquivo = filedialog.askopenfilename(
        title=titulo,
        filetypes=[("Arquivos Excel", "*.xlsx *.xls"), ("Todos os arquivos", "*.*")],
        initialdir=os.path.expanduser(pasta_inicial)
    )

    root.destroy()

    if not arquivo:
        return None
    
    return arquivo

def salvar_excel(dados: list, caminho_referencia: str, sufixo: str) -> None:
    if not dados:
        return
    
    df = pd.DataFrame(dados)
    nome_base, extensao = os.path.splitext(caminho_referencia)
    caminho_saida = f"{nome_base}{sufixo}{extensao}"
    
    df.to_excel(caminho_saida, index=False)

def limpar_arquivo_temporario(caminho_referencia: str) -> None:
    nome_base, extensao = os.path.splitext(caminho_referencia)
    caminho_temp = f"{nome_base}_TEMP{extensao}"

    if os.path.exists(caminho_temp):
        os.remove(caminho_temp)
        print(f"Arquivo temporário removido: {os.path.basename(caminho_temp)}")