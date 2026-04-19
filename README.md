---
title: Classificador Musical
emoji: 🎧
colorFrom: purple
colorTo: blue
sdk: streamlit
app_file: app.py
pinned: false
---

# 🎧 Classificador de Gêneros Musicais com IA

Um projeto full-stack focado na extração e classificação de características de áudio utilizando modelos de Machine Learning. A aplicação recebe músicas (via busca ou upload de arquivo) e utiliza a arquitetura Hubert para retornar a probabilidade matemática do gênero musical predominante.

🌐 **Live Demo:** [Acesse a aplicação rodando na nuvem (Hugging Face) aqui](https://huggingface.co/spaces/itsmaddu/classificador-musical)

## 🚀 Visão Geral das Funcionalidades

- **Múltiplas Entradas (Tabs)**: O usuário pode pesquisar músicas diretamente (via `yt-dlp` integrado ao SoundCloud) ou fazer o upload de um arquivo local `.mp3`.
- **Pré-processamento Ativo (Audio Slicing)**: Isolamento automático do refrão para classificação de características sonoras, contornando vieses de introduções atípicas.
- **Visualização Analítica**: Renderização de dados com Plotly Express, convertendo matrizes de probabilidade brutas da IA em gráficos de anel interativos com porcentagens formatadas.
- **UX Otimizada**: Suporte nativo à tecla "Enter" via formulários do Streamlit e dicas visuais (Tooltips).

## 🧠 Decisões de Arquitetura e Engenharia

Durante o desenvolvimento e deploy em ambiente de nuvem (Hugging Face Spaces), vários desafios de infraestrutura foram mapeados e resolvidos:

### 1. Seleção do Modelo de Machine Learning (Estabilidade vs. Infraestrutura)
Inicialmente, modelos baseados no dataset GTZAN apresentaram instabilidade de cache (`not a local folder`) em servidores gratuitos. 
**A Solução:** Migração para o modelo `SeyedAli/Musical-genres-Classification-Hubert-V1`, que provou ser extremamente estável e eficiente em recursos.

### 2. Autenticação Segura e Gerenciamento de Cache
O carregamento de modelos via `transformers` pode sofrer bloqueios de taxa de download em ambientes de nuvem.
**A Solução:** Injeção do `HF_TOKEN` como variável de ambiente (Secrets) para garantir requisições autenticadas e estáveis.

### 3. Feature Extraction e Correção de Viés (Audio Slicing)
IAs de áudio podem ser induzidas ao erro por introduções atípicas (ex: batidas de Disco/Funk no início de músicas Pop).
**A Solução:** Utilização da biblioteca `pydub` para recortar o áudio e alimentar a IA apenas com o trecho do refrão (segundo 40 ao 70), onde a identidade sonora é mais forte.

### 4. Otimização de UX e Transparência de Dados
O controle de volume foi delegado nativamente ao navegador para evitar reprocessamentos pesados no servidor. Além disso, o filtro de "Top 5" foi removido para expor as 10 categorias originais do modelo, garantindo total transparência nos dados.

## 🛠️ Stack Tecnológica

- **Linguagem**: Python 3.9+
- **Front-end**: Streamlit, Plotly Express
- **Machine Learning**: Hugging Face `transformers`, `torch`, `torchaudio`
- **Manipulação de Mídia**: `pydub`, `yt-dlp`

## ☁️ Como Usar na Nuvem (Sem Instalação)

A aplicação está hospedada e configurada em um servidor de produção. Não é necessário instalar nenhum ambiente local.
Basta acessar o link do **Live Demo** no topo deste repositório, pesquisar o nome de uma música ou enviar o seu arquivo MP3, e o servidor em nuvem processará a IA automaticamente.

## 💻 Como Executar Localmente

1. Clone o repositório:
```bash
git clone [https://github.com/itsmaddu/classificador-musical.git](https://github.com/itsmaddu/classificador-musical.git)
cd classificador-musical
```

2. Instale as dependências rigorosamente como no `requirements.txt` para evitar conflitos de versão:
```bash
pip install -r requirements.txt
```

3. Configure a Autenticação do Modelo:
   - **Linux/Mac**: `export HF_TOKEN="seu_token_aqui"`
   - **Windows (CMD)**: `set HF_TOKEN="seu_token_aqui"`

4. Inicie o servidor local:
```bash
streamlit run app.py
```
