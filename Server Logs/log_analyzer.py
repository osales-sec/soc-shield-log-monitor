import time
import re
from datetime import datetime

def monitor_soc_estrito(arquivo_origem, arquivo_blacklist):
    print("=" * 60)
    print("   SOC SHIELD ENTERPRISE - REFRESH ENGINE v7.1    ")
    print("=" * 60)
    print("[*] Monitorando alterações estruturais de logs no disco...\n")
    
    JANELA_TEMPO_SEGUNDOS = 15
    LIMITE_TENTATIVAS = 3
    PADRAO_LOG = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - FAILED_LOGIN - .*? - IP:\s*([\d\.]+)')
    
    historico_falhas = {}
    
    # Descobre o tamanho atual do arquivo para ler apenas o que surgir de novo
    try:
        with open(arquivo_origem, 'r', encoding="utf-8") as f:
            f.seek(0, 2)
            ultimo_posicionamento = f.tell()
    except FileNotFoundError:
        ultimo_posicionamento = 0

    try:
        while True:
            # 1. TRATAMENTO DE FALHA NA LEITURA: Abre e fecha o arquivo a cada ciclo
            # Isso força o Windows a atualizar o cache de modificações do disco imediatamente.
            try:
                with open(arquivo_origem, 'r', encoding="utf-8") as logs:
                    logs.seek(0, 2)
                    tamanho_atual = logs.tell()
                    
                    # Se o arquivo aumentou de tamanho, significa que novos logs entraram
                    if tamanho_atual > ultimo_posicionamento:
                        logs.seek(ultimo_posicionamento)
                        novas_linhas = logs.read().splitlines() # Lê tudo de novo e divide em linhas com segurança
                        ultimo_posicionamento = tamanho_atual
                        
                        # Processa cada nova linha encontrada no bloco de texto
                        for linha in novas_linhas:
                            match = PADRAO_LOG.match(linha.strip())
                            if not match:
                                continue
                            
                            texto_data_hora, ip_extraido = match.groups()
                            horario_evento = datetime.strptime(texto_data_hora, "%Y-%m-%d %H:%M:%S")
                            
                            if ip_extraido not in historico_falhas:
                                historico_falhas[ip_extraido] = []
                            
                            historico_falhas[ip_extraido].append(horario_evento)
                            print(f"[LOG] Falha mapeada: IP {ip_extraido} em {texto_data_hora}")
                            
                            # Limpeza de memória baseada no tempo interno
                            historico_falhas[ip_extraido] = [
                                t for t in historico_falhas[ip_extraido] 
                                if (horario_evento - t).total_seconds() <= JANELA_TEMPO_SEGUNDOS
                            ]
                            
                            # Validação de ataque por IP isolado
                            if len(historico_falhas[ip_extraido]) >= LIMITE_TENTATIVAS:
                                
                                # Evita IPs duplicados em disco (Garantia de integridade)
                                ip_ja_bloqueado = False
                                try:
                                    with open(arquivo_blacklist, 'r', encoding="utf-8") as bl:
                                        if ip_extraido in bl.read():
                                            ip_ja_bloqueado = True
                                except FileNotFoundError:
                                    pass
                                
                                if not ip_ja_bloqueado:
                                    print(f"\n[💥 BLOQUEIO CRÍTICO] Força bruta do IP {ip_extraido} mitigada com sucesso!")
                                    with open(arquivo_blacklist, 'a', encoding="utf-8") as bl:
                                        bl.write(f"{ip_extraido}\n")
                                    
                                    del historico_falhas[ip_extraido]
                                    
            except Exception as erro_interno:
                print(f"[⚠️ Erro de leitura em disco] Aguardando estabilização: {erro_interno}")
            
            time.sleep(0.5) # Intervalo seguro de atualização
            
    except KeyboardInterrupt:
        print("\n[*] Monitoramento encerrado pelo operador.")

if __name__ == "__main__":
    monitor_soc_estrito("server_logs.txt", "blacklist_firewall.txt")
