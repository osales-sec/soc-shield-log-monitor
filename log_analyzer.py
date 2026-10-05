import time
from datetime import datetime

def monitoramento_em_tempo_real(arquivo_origem, arquivo_blacklist):
    print("=" * 60)
    print("   SOC SHIELD - INSTANT LIVE MONITOR & FIREWALL v5.0   ")
    print("=" * 60)
    print("[*] Iniciando monitoramento em tempo real...")
    print("[*] Aguardando novos eventos no servidor corporativo... (Ctrl+C para parar)\n")
    
    # Dicionário de rastreamento temporal
    historico_falhas = {}
    ips_bloqueados_na_sessao = set() # Usamos set para garantir que não haverá IPs repetidos
    
    try:
        # Abrimos o arquivo de log original
        with open(arquivo_origem, 'r', encoding="utf-8") as logs:
            
            # O truque de mestre: Movemos o cursor de leitura direto para o FINAL do arquivo.
            # Assim, o script ignora o passado e foca apenas no que for digitado a partir de AGORA.
            logs.seek(0, 2)
            
            # Loop infinito para monitorar o arquivo a cada segundo
            while True:
                linha = logs.readline()
                
                # Se uma nova linha surgir no arquivo (ou seja, se alguém tentar logar no sistema)
                if linha:
                    # Filtra apenas se for falha de login
                    if "FAILED_LOGIN" in linha:
                        
                        # Extração cirúrgica de dados
                        partes_linha = linha.split(" - ")
                        texto_data_hora = partes_linha[0]
                        ip_extraido = linha.split("IP: ")[1].strip()
                        horario_evento = datetime.strptime(texto_data_hora, "%Y-%m-%d %H:%M:%S")
                        
                        # Se o IP já foi bloqueado antes nesta sessão, ignora os novos logs dele
                        if ip_extraido in ips_bloqueados_na_sessao:
                            continue
                            
                        # Inicializa o histórico do IP caso seja o primeiro erro dele
                        if ip_extraido not in historico_falhas:
                            historico_falhas[ip_extraido] = []
                        
                        historico_falhas[ip_extraido].append(horario_evento)
                        print(f"[LOG RECEBIDO] Nova falha registrada do IP: {ip_extraido}")
                        
                        # Lógica de detecção temporal rápida
                        horarios = historico_falhas[ip_extraido]
                        if len(horarios) >= 3:
                            tempo_primeira_falha = horarios[-3] # Analisa as últimas 3 tentativas
                            tempo_ultima_falha = horarios[-1]
                            diferenca_tempo = (tempo_ultima_falha - tempo_primeira_falha).total_seconds()
                            
                            # Se acontecerem 3 erros em menos de 15 segundos: BLOQUEIO IMEDIATO!
                            if diferenca_tempo <= 15:
                                print(f"\n[💥 ATENTADO DETECTADO] Força bruta detectada do IP {ip_extraido}!")
                                print(f"[🛡️ FIREWALL ACTION] Bloqueando tráfego do IP {ip_extraido} imediatamente.\n")
                                
                                ips_bloqueados_na_sessao.add(ip_extraido)
                                
                                # Escreve na blacklist ao vivo sem apagar os IPs anteriores ('a' de append)
                                with open(arquivo_blacklist, 'a', encoding="utf-8") as blacklist:
                                    blacklist.write(f"{ip_extraido}\n")
                                    
                # Pequena pausa de 0.1 segundo para não estressar o processador do computador
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\n[*] Monitoramento encerrado pelo operador do SOC.")
    except FileNotFoundError:
        print("Erro: Arquivo de logs não encontrado.")

# Inicia o monitoramento contínuo
monitoramento_em_tempo_real("server_logs.txt", "blacklist_firewall.txt")

