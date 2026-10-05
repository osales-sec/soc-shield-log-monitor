# SOC Shield: Monitoramento e Resposta a Incidentes em Tempo Real 🛡️

Este projeto simula o núcleo operacional de uma ferramenta de SIEM (Security Information and Event Management) e SOAR (Security Orchestration, Automation, and Response). Desenvolvido em Python, o script realiza a leitura dinâmica de arquivos de logs de autenticação corporativa e automatiza o bloqueio de IPs atacantes.

## 🚀 Funcionalidades Integradas
* **Monitoramento Real-Time (Live Monitoring):** O script roda em background inspecionando atualizações de logs no exato segundo em que acontecem (`seek` dinâmico).
* **Correlação de Eventos Temporal:** Diferencia erros humanos comuns de ataques reais calculando a janela de tempo entre tentativas consecutivas (`datetime`).
* **Firewall Action Automatizado:** Gera e alimenta uma lista negra (`blacklist_firewall.txt`) isolando cirurgicamente os endereços IP dos atacantes através de manipulação de strings (`split`).

## 🛠️ Tecnologias e Conceitos Utilizados
* **Linguagem:** Python 3.x (Bibliotecas nativas: `time`, `datetime`).
* **Conceitos de Segurança:** Engenharia Social (Mitigação de Força Bruta), Gestão de Identidade e Acessos (IAM), Resposta a Incidentes (IR), Governança e Regras de Firewall.

## 💻 Como Executar o Projeto
1. Certifique-se de ter o arquivo `server_logs.txt` criado no mesmo diretório.
2. Execute o monitor através do terminal:
   ```bash
   python log_analyzer.py
   ```
3. Simule novas tentativa de intrusão inserindo linhas de falha no arquivo de logs para visualizar a detecção e o bloqueio automático agindo em tempo real.
