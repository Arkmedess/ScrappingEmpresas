from utils.file_handler import selecionar_arquivo_entrada
from core.processor import iniciar_processamento
import pandas as pd

def main():
    # 1. Seleciona
    caminho = selecionar_arquivo_entrada()
    if not caminho: return

    # 2. Carrega
    try:
        df = pd.read_excel(caminho)
    except Exception as e:
        print(f"Erro ao abrir Excel: {e}")
        return

    # 3. Processa (O backup e o salvamento final acontecem lá dentro)
    try:
        iniciar_processamento(df, caminho)
        print("\n✅ Processo finalizado com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante o processamento: {e}")
        print("💡 Dica: Verifique se foi gerado um arquivo _TEMP com os dados salvos.")

if __name__ == "__main__":
    main()