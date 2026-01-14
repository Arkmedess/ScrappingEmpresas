from utils.file_handler import selecionar_arquivo_entrada
from core.processor import iniciar_processamento
import pandas as pd
import sys

def main():
    # Verifica se foi passado arquivo como argumento (para Docker/CLI)
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
    else:
        # Caso contrário, abre diálogo (para uso local com GUI)
        caminho = selecionar_arquivo_entrada()
        if not caminho: return

    try:
        df = pd.read_excel(caminho)
    except Exception as e:
        print(f"Erro ao abrir Excel: {e}")
        return

    try:
        iniciar_processamento(df, caminho)
        print("\n✅ Processo finalizado com sucesso!")
    except Exception as e:
        print(f"\n Erro durante o processamento: {e}")
        print("Dica: Verifique se foi gerado um arquivo _TEMP com os dados salvos.")

if __name__ == "__main__":
    main()