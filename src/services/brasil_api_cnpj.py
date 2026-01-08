import requests

class BrasilAPI:
    def __init__(self, recurso="cnpj", versao="v1"):
        self.url_base = f"https://brasilapi.com.br/api/{recurso}/{versao}"

    def consultar_cnpj(self, cnpj: str):
        url = f"{self.url_base}/{cnpj.zfill(14)}"

        try:
            resposta = requests.get(url, timeout=6)

            match resposta.status_code:
                case 200:
                    return self._formatar_resposta(resposta.json())

                case 429:
                    return {"Status_Consulta": "Rate Limit Excedido"}

                case 404:
                    return {f"Status_Consulta": resposta.json().get("message")}

                case 400:
                    return {"Status_Consulta": resposta.json().get("message")}

                case _:
                    return {"Status_Consulta": f"Erro inesperado - {resposta.json().get("message", "Erro não catalogado.")}"}
                
        except requests.exceptions.RequestException as e:
            return {"Status_Consulta": f"Erro de rede: {str(e)}"}

    def _formatar_resposta(self, data):
        return {
            "Status_Consulta": "Sucesso",
            "cnpj": data.get("cnpj", ""),
            "razao_social": data.get("razao_social", ""),
            "nome_fantasia": data.get("nome_fantasia", ""),
            "porte": data.get("porte", ""),
            "descricao_porte": data.get("descricao_porte", ""),
            "CNAE": data.get("cnae_fiscal", ""),
            "DescricaoCNAE": data.get("cnae_fiscal_descricao", ""),
            "TipoLogradouro": data.get("descricao_tipo_de_logradouro" ""),
            "logradouro": data.get("logradouro", ""),
            "numero": data.get("numero", ""),
            "complemento": data.get("complemento", ""),
            "bairro": data.get("bairro", ""),
            "municipio": data.get("municipio", ""),
            "uf": data.get("uf", ""),
            "cep": data.get("cep", ""),
            "telefone": data.get("ddd_telefone_1", ""),
            "telefone2": data.get("ddd_telefone_2", ""),
            "email": data.get("email", ""),
            "situacao_cadastral": data.get("descricao_situacao_cadastral", ""),
            "descricao_motivo_situacao": data.get("descricao_motivo_situacao_cadastral", ""),
            "data_situacao": data.get("data_situacao_cadastral", ""),
            "natureza_juridica": data.get("natureza_juridica", ""),
            "capital_social": data.get("capital_social", 0),
        }