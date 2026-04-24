# Digital Marketing Analytics

Análise exploratória de dados de um e-commerce com foco em comportamento de compra, funil de conversão, sazonalidade, performance por categoria e segmentação de clientes.

## Objetivo

Transformar dados transacionais em insights de negócio acionáveis para responder perguntas como:

- Onde estão os maiores pontos de fricção do funil?
- Quais categorias combinam volume e conversão?
- O negócio depende de sazonalidade?
- Como a base de clientes pode ser segmentada para retenção e crescimento?

## Dataset

- Fonte: Kaggle
- Base utilizada: `mexwell/google-merchandise-sales-data`
- Coleta no notebook via `kagglehub`, sem necessidade de subir os CSVs para o repositório

## Principais análises

- Análise exploratória dos datasets de eventos, usuários e produtos
- Limpeza e preparação dos dados
- Métricas de negócio, como receita total e ticket médio
- Funil de conversão agregado e por sessão
- Análise temporal de pedidos e receita
- Performance por produto e categoria
- Segmentação de clientes com modelo RFM
- Geração automatizada de relatório final em Markdown

## Principais insights

- A conversão entre `add_to_cart` e `purchase` é baixa, indicando fricção relevante na jornada de compra.
- O volume de pedidos cresce fortemente entre novembro e dezembro, sugerindo dependência de sazonalidade.
- Algumas categorias apresentam alta intenção de compra, mas baixo volume, enquanto outras concentram tráfego com baixa conversão.
- A base de clientes ainda é pouco madura em retenção: poucos clientes concentram alto valor e a maior parte está em segmentos menos estratégicos.
- Clientes frequentes representam uma oportunidade clara de crescimento por ações de upsell, cross-sell e recorrência.

## Estrutura do projeto

```text
.
├── ecommerce_customer_analysis.ipynb
├── gerar_relatorio_completo.py
├── report_builder.py
├── reports/
│   ├── relatorio_executivo.md
│   └── dados_resumidos.json
└── README.md
```

## Tecnologias

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- KaggleHub

## Como executar

1. Instale as dependências do projeto.
2. Abra o notebook [ecommerce_customer_analysis.ipynb](./ecommerce_customer_analysis.ipynb).
3. Execute as células em sequência.
4. Na etapa final, o notebook monta um relatório executivo e salva um arquivo em `reports/final_report.md`.

Exemplo de instalação:

```bash
pip install pandas numpy matplotlib seaborn plotly kagglehub notebook
```

## Relatório final automatizado

Para leitura direta no GitHub, o projeto agora inclui um relatório separado em [reports/relatorio_executivo.md](./reports/relatorio_executivo.md), sem depender da abertura do notebook. Esse material já traz gráficos em SVG incorporados ao Markdown para facilitar a leitura online.

O arquivo [gerar_relatorio_completo.py](./gerar_relatorio_completo.py) gera esse relatório e também exporta um resumo estruturado em [reports/dados_resumidos.json](./reports/dados_resumidos.json). O módulo [report_builder.py](./report_builder.py) continua sendo usado pela etapa final do notebook para montar um resumo executivo automatizado.

## Valor de portfólio

Este projeto demonstra capacidade de:

- estruturar uma análise ponta a ponta;
- traduzir dados em recomendações de negócio;
- combinar storytelling analítico com métricas operacionais;
- documentar o trabalho de forma reproduzível para GitHub.
