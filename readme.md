# Mini App de Fila de Atendimento

Aplicação web desenvolvida em **Python (Flask)** e **SQLite** para controle e gerenciamento de filas de atendimento presenciais ou virtuais.

## 🚀 Funcionalidades
- **Cadastro de Clientes:** Inserção de nome e definição de prioridade (*Normal* ou *Preferencial*).
- **Fila Inteligente (FIFO com Prioridades):** Clientes preferenciais têm preferência automática de atendimento, mantendo a ordem de chegada entre pares da mesma categoria.
- **Chamada do Próximo:** Botão para avançar o atendimento (conclui o atual automaticamente e chama o próximo da fila).
- **Cancelamento:** Permite cancelar o atendimento de um cliente na fila.
- **Histórico:** Tela dedicada para visualizar todos os atendimentos concluídos ou cancelados.
- **Atualização Automática:** A página se atualiza automaticamente a cada 10 segundos via meta-refresh (Bônus).

---

## 🛠️ Como Executar o Projeto

1. Certifique-se de ter o **Python** instalado na sua máquina.
2. Clone este repositório ou baixe os arquivos.
3. Instale as dependências executando:
   ```bash
   pip install -r requirements.txt