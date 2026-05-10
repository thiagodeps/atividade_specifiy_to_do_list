# Zentask

Uma aplicação simples de gerenciamento do ciclo de vida de tarefas construída com Python e Streamlit.

## Recursos

- Criar, editar e excluir tarefas
- Acompanhar o status das tarefas (A Fazer, Em Progresso, Concluído, Pausado)
- Adiar tarefas para datas futuras
- Trilha de auditoria para todas as alterações
- Design pensado para teclado

## Início Rápido

1. Configure o ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

2. Execute o aplicativo:
   ```bash
   python run.py
   ```

   Ou execute diretamente com Streamlit:
   ```bash
   PYTHONPATH=src streamlit run src/zentask/ui/app.py
   ```

## Desenvolvimento

Execute os testes:
```bash
pytest
```

## Arquitetura

- **Padrão MVC**: Modelos (dados), Serviços (lógica de negócio), IU (visões Streamlit)
- **Armazenamento em memória** com log de auditoria em JSON Lines
- **Trilha de auditoria imutável** para todas as mutações de tarefas
