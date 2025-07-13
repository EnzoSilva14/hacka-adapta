# 🤖 CodePhoenix - Agent as a Service

> **Pequenas melhorias, grandes resultados — sem backlog parado.**

Um **Agente Autônomo como Serviço** que monitora métricas de uso, identifica gargalos e gera melhorias de UI/UX e código automaticamente, integrando diretamente ao seu repositório via Pull Requests.

## 🚀 O Problema

Produtos digitais acumulam **toneladas de dados de analytics**, mas pequenas melhorias ficam **semanas no backlog**. Isso custa:
- 📉 **Conversão** perdida
- 💰 **Receita** não otimizada  
- ⏰ **Tempo de desenvolvimento** desperdiçado

## 💡 A Solução

O **CodePhoenix** é um sistema inteligente que:

1. **📊 Monitora** métricas de comportamento do usuário
2. **🔍 Identifica** gargalos e oportunidades de melhoria
3. **🛠️ Gera** melhorias de UI/UX e código automaticamente
4. **🔄 Integra** ao repositório com Pull Requests automáticos

## 🏗️ Como Funciona

### 1. **Coleta de Dados**
- SDK injetado no SaaS/Produto do cliente
- Coleta dados comportamentais sob medida
- Envia para nossa API via eventos

### 2. **Processamento Inteligente**
- Dois módulos especializados:
  - **UX Analyst**: Foca em melhorias de usabilidade
  - **Code Refactor**: Gera snippets de código otimizado

### 3. **Automação**
- Agente cria uma nova branch
- Implementa as melhorias no código
- Gera commit com as alterações
- **Abre Pull Request automaticamente** via GitHub/GitLab/Bitbucket

## 🛠️ Tecnologias

### Backend
- **FastAPI** - API moderna e performática
- **CrewAI** - Orquestração de agentes de IA
- **Nvidia/Meta Llama 3.3 Nematron** - Modelo de linguagem avançado
- **LangSmith** - Observabilidade e tracing

### Integrações
- **GitHub API** - Criação automática de PRs
- **Python** - Stack principal de desenvolvimento

### Infraestrutura
- **Docker** - Containerização
- **SQS** - Fila de eventos (planejado)
- **APIs RESTful** - Comunicação entre serviços

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Docker (opcional)
- Token do GitHub
- Chave da API Nvidia

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/hacka-adapta.git
cd hacka-adapta
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
GITHUB_TOKEN=seu_token_github
NVIDIA_API_KEY=sua_chave_nvidia
LANGCHAIN_API_KEY=sua_chave_langsmith
```

### 4. Execute a Aplicação
```bash
# Desenvolvimento
uvicorn src.main:app --reload

# Docker
docker build -t hacka-adapta .
docker run -p 8000:8000 hacka-adapta
```

## 📋 Uso da API

### Endpoint Principal

**POST** `/api/analisar-ux`

```json
{
  "heatmap": {
    "sessoes": 1250,
    "cliques_inativos": 320,
    "intencao": "compra",
    "dispositivo": "mobile",
    "paginas_saida": ["/checkout", "/produto"]
  }
}
```

**Resposta:**
```json
{
  "descricao": "Pull Request criado com melhorias de UX baseadas na análise comportamental"
}
```

## 📝 Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
