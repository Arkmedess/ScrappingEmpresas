import time

class ControladorRateLimit:
    def __init__(self):
        self.pausa_base = 0.5
        self.pausa_maxima = 3.0
        self.contador_rate_limit = 0
        self.requisicoes_sucesso = 0

    def registrar_sucesso(self):
        # Reduz pausas em caso de sucesso constante, 0,3s é o mínimo para evitar bloqueios constantes
        self.requisicoes_sucesso += 1
        self.contador_sequencial_rate_limit = 0

        if self.requisicoes_sucesso > 20 and self.pausa_base > 0.3:
            self.pausa_base = max(0.3, self.pausa_base - 0.05)
            self.requisicoes_sucesso = 0
    
    def registrar_rate_limit(self):
        # Serve para aumentar a pausa e evitar caso de rate limit frequentes.
        self.contador_rate_limit += 1
        self.contador_sequencial_rate_limit += 1
        self.pausa_base = min(self.pausa_maxima, self.pausa_base + 0.1)
        self.requisicoes_sucesso = 0

        pausa_rate_limit = 10 * self.contador_sequencial_rate_limit

        if self.contador_sequencial_rate_limit > 1:
            print(f"[RATE LIMIT] Sequência de {self.contador_sequencial_rate_limit} erros.")
        
        print(f"Pausa de resfriamento atual: {pausa_rate_limit}s")

        time.sleep(pausa_rate_limit)

    def analisar_status(self, resultado_api: dict):
        status: str = str(resultado_api.get("Status_Consulta") or "")

        acoes = {
            "Sucesso": self.registrar_sucesso,
            "Rate Limit Excedido": self.registrar_rate_limit
        }

        acoes.get(status, lambda: None)

        time.sleep(self.pausa_base)