from validate_docbr import CNPJ
import re

_validador_CNPJ = CNPJ()

def limpar_cnpj(cnpj: str) -> str:
    return re.sub(r"\D", "", str(cnpj))

def validar_cnpj(cnpj_bruto: str) -> bool:
    # Necessário para evitar consulta de CNPJ inválido.
    cnpj_limpo = limpar_cnpj(cnpj_bruto)
    return _validador_CNPJ.validate(cnpj_limpo)