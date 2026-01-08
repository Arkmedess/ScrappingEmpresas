import pandas as pd
from typing import List, Dict
from services.brasil_api_cnpj import BrasilAPI
from utils.validators import validar_cnpj, limpar_cnpj
from core.controller import ControladorRateLimit
from utils.file_handler import salvar_excel, limpar_arquivo_temporario

def iniciar_processamento(df: pd.DataFrame, caminho_original:str) -> List[Dict]:
    api = BrasilAPI()
    controlador = ControladorRateLimit()
    resultados: List[Dict] = []

    print(f"🚀 Iniciando processamento de {len(df)} linhas...")

    # Busca o valor (get) na coluna definida.
    for i, (index, row) in enumerate(df.iterrows()):
        cnpj_original = str(row.get('CNPJ',''))

        if not validar_cnpj(cnpj_original):
            print(f"Linha {index}: CNPJ {cnpj_original} inválido. Pulando...")
            conversao_linha = {**row.to_dict(), "Status_Consulta": "CNPJ Inválido"}
            resultados.append(conversao_linha)
            continue
        
        print(f"Consultado CNPJ: {cnpj_original}...")
        dados_api = api.consultar_cnpj(limpar_cnpj(cnpj_original))
        controlador.analisar_status(dados_api)

        linha_completa = {**row.to_dict(), **dados_api}
        resultados.append(linha_completa)

        if i % 35 == 0 and i > 0:
            salvar_excel(resultados, caminho_original, "_TEMP")
            print(f"💾 Backup atualizado na linha {index}")

    salvar_excel(resultados, caminho_original, "_RESULTADO_FINAL")
    limpar_arquivo_temporario(caminho_original)

    return resultados