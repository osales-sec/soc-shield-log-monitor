# SOC Shield: Monitoramento e Resposta a Incidentes em Tempo Real 🛡️

Este projeto simula o núcleo operacional de uma ferramenta de SIEM (Security Information and Event Management) e SOAR (Security Orchestration, Automation, and Response). Desenvolvido em Python, o script realiza a leitura dinâmica de arquivos de logs de autenticação corporativa e automatiza o bloqueio de IPs atacantes.

## 🚀 Funcionalidades Integradas
* **Monitoramento Real-Time (Live Block Engine):** O script roda em background inspecionando atualizações de blocos de logs no disco através de um motor de atualização contínua de cache (`Refresh Engine`).
* **Correlação de Eventos Temporal:** Diferencia erros humanos comuns de ataques reais calculando a janela de tempo entre tentativas consecutivas baseando-se estritamente no timestamp interno dos logs (`datetime`).
* **Firewall Action Automatizado com Regex:** Captura e isola cirurgicamente endereços IP através de Expressões Regulares robustas (`re`), alimentando uma lista negra (`blacklist_firewall.txt`) com garantia de unicidade e proteção contra concorrência de múltiplos atacantes simultâneos.

## 🛠️ Tecnologias e Conceitos Utilizados
* **Linguagem:** Python 3.x (Bibliotecas nativas: `time`, `datetime`, `re`).
* **Conceitos de Segurança:** Engenharia Social (Mitigação de Força Bruta), Gestão de Identidade e Acessos (IAM), Resposta a Incidentes (IR), Governança, Resiliência de Código e Regras de Firewall.

## 💻 Como Executar o Projeto
1. Certifique-se de ter o arquivo `server_logs.txt` criado no mesmo diretório.
2. Execute o monitor através do terminal:
   ```bash
   python log_analyzer.py
   ```
3. Simule novas tentativas de intrusão inserindo linhas de falha de múltiplos IPs no arquivo de logs para visualizar a detecção simultânea e o bloqueio automático agindo em tempo real.
