"""
Gerador de relatório executivo para o projeto de análise de e-commerce.

Uso:
    python relatorio_ecommerce_completo.py

Saídas:
    - reports/relatorio_executivo.md
    - reports/dados_resumidos.json
    - reports/images/*.svg
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class ConfigRelatorio:
    titulo: str = "Digital Marketing Analytics"
    subtitulo: str = "Relatório Executivo de Análise de E-commerce"
    autor: str = "Ludmilla Sousa Quirino"
    data_geracao: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y"))
    dir_saida: Path = Path("reports")
    dir_imagens: Path = Path("reports/images")
    dados_padrao: dict = field(
        default_factory=lambda: {
            "receita_total": 307114.00,
            "ticket_medio": 19.74,
            "clientes_recorrentes_pct": 73.93,
            "clientes_one_time_pct": 26.07,
            "add_to_cart": 667282,
            "purchases": 15555,
            "taxa_conversao": 2.33,
            "conversao_checkout": 35.10,
            "conversao_compra": 17.00,
            "total_clientes": 4066,
            "total_eventos": 758884,
            "total_produtos": 1381,
        }
    )


class GeradorRelatorio:
    def __init__(self) -> None:
        self.config = ConfigRelatorio()
        self.dados = self.config.dados_padrao.copy()
        self.config.dir_saida.mkdir(parents=True, exist_ok=True)
        self.config.dir_imagens.mkdir(parents=True, exist_ok=True)

    def _svg_document(self, width: int, height: int, body: str) -> str:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img">'
            f'<rect width="100%" height="100%" fill="#f8fafc"/>'
            f"{body}</svg>"
        )

    def _salvar_svg(self, nome_arquivo: str, conteudo: str) -> Path:
        caminho = self.config.dir_imagens / nome_arquivo
        caminho.write_text(conteudo, encoding="utf-8")
        return caminho

    def gerar_grafico_funil(self) -> Path:
        width, height = 900, 360
        checkout = self.dados["add_to_cart"] * (self.dados["conversao_checkout"] / 100)
        dados = [
            ("Add to cart", self.dados["add_to_cart"], "#1d4ed8"),
            ("Checkout", checkout, "#3b82f6"),
            ("Purchase", self.dados["purchases"], "#0f172a"),
        ]
        max_valor = max(valor for _, valor, _ in dados)
        body = [
            '<text x="40" y="42" font-size="24" font-weight="700" fill="#0f172a">Funil de Conversão</text>'
        ]

        for indice, (label, valor, cor) in enumerate(dados):
            y = 80 + indice * 85
            barra = 620 * (valor / max_valor)
            body.append(
                f'<text x="40" y="{y + 22}" font-size="16" fill="#334155">{label}</text>'
                f'<rect x="190" y="{y}" width="{barra:.1f}" height="34" rx="8" fill="{cor}"/>'
                f'<text x="{200 + barra:.1f}" y="{y + 22}" font-size="15" fill="#0f172a">{valor:,.0f}</text>'
            )

        return self._salvar_svg("funil_conversao.svg", self._svg_document(width, height, "".join(body)))

    def gerar_grafico_clientes(self) -> Path:
        width, height = 700, 420
        recorrentes = self.dados["clientes_recorrentes_pct"]
        one_time = self.dados["clientes_one_time_pct"]
        circ = 2 * 3.14159 * 90
        parte_recorrentes = circ * (recorrentes / 100)
        parte_one_time = circ - parte_recorrentes

        body = f"""
<text x="40" y="42" font-size="24" font-weight="700" fill="#0f172a">Composição da Base de Clientes</text>
<circle cx="180" cy="220" r="90" fill="none" stroke="#e2e8f0" stroke-width="34"/>
<circle cx="180" cy="220" r="90" fill="none" stroke="#2a9d8f" stroke-width="34"
    stroke-dasharray="{parte_recorrentes:.1f} {circ:.1f}" stroke-linecap="butt"
    transform="rotate(-90 180 220)"/>
<circle cx="180" cy="220" r="90" fill="none" stroke="#e76f51" stroke-width="34"
    stroke-dasharray="{parte_one_time:.1f} {circ:.1f}" stroke-dashoffset="-{parte_recorrentes:.1f}"
    transform="rotate(-90 180 220)"/>
<text x="145" y="226" font-size="24" font-weight="700" fill="#0f172a">100%</text>

<rect x="360" y="145" width="18" height="18" rx="4" fill="#2a9d8f"/>
<text x="390" y="159" font-size="17" fill="#334155">Recorrentes: {recorrentes:.2f}%</text>
<rect x="360" y="205" width="18" height="18" rx="4" fill="#e76f51"/>
<text x="390" y="219" font-size="17" fill="#334155">One-time: {one_time:.2f}%</text>
<text x="360" y="290" font-size="15" fill="#64748b">A base mostra boa recorrência, mas ainda há espaço para reengajamento.</text>
"""
        return self._salvar_svg("composicao_clientes.svg", self._svg_document(width, height, body))

    def gerar_grafico_benchmark(self) -> Path:
        width, height = 900, 430
        categorias = [
            ("Conversão", self.dados["taxa_conversao"], 4.0),
            ("Clientes recorrentes", self.dados["clientes_recorrentes_pct"], 65.0),
            ("Ticket médio", self.dados["ticket_medio"], 60.0),
        ]
        max_valor = max(max(projeto, benchmark) for _, projeto, benchmark in categorias)
        body = [
            '<text x="40" y="42" font-size="24" font-weight="700" fill="#0f172a">Comparação com Benchmark</text>',
            '<rect x="620" y="24" width="16" height="16" rx="4" fill="#264653"/>',
            '<text x="645" y="37" font-size="14" fill="#334155">Projeto</text>',
            '<rect x="730" y="24" width="16" height="16" rx="4" fill="#e9c46a"/>',
            '<text x="755" y="37" font-size="14" fill="#334155">Benchmark</text>',
        ]

        for indice, (label, projeto, benchmark) in enumerate(categorias):
            y = 95 + indice * 95
            largura_projeto = 280 * (projeto / max_valor)
            largura_benchmark = 280 * (benchmark / max_valor)
            body.append(
                f'<text x="40" y="{y + 20}" font-size="16" fill="#334155">{label}</text>'
                f'<rect x="280" y="{y}" width="{largura_projeto:.1f}" height="24" rx="6" fill="#264653"/>'
                f'<text x="{290 + largura_projeto:.1f}" y="{y + 17}" font-size="14" fill="#0f172a">{projeto:.2f}</text>'
                f'<rect x="280" y="{y + 34}" width="{largura_benchmark:.1f}" height="24" rx="6" fill="#e9c46a"/>'
                f'<text x="{290 + largura_benchmark:.1f}" y="{y + 51}" font-size="14" fill="#0f172a">{benchmark:.2f}</text>'
            )

        return self._salvar_svg("benchmark_mercado.svg", self._svg_document(width, height, "".join(body)))

    def gerar_grafico_oportunidades(self) -> Path:
        width, height = 900, 430
        iniciativas = [
            ("Carrinho abandonado", 228000, "#457b9d"),
            ("Retenção", 418000, "#2a9d8f"),
            ("Ticket médio", 138000, "#f4a261"),
        ]
        max_valor = max(valor for _, valor, _ in iniciativas)
        body = [
            '<text x="40" y="42" font-size="24" font-weight="700" fill="#0f172a">Potencial de Receita por Iniciativa</text>'
        ]

        for indice, (label, valor, cor) in enumerate(iniciativas):
            x = 110 + indice * 240
            altura = 240 * (valor / max_valor)
            y = 330 - altura
            body.append(
                f'<rect x="{x}" y="{y:.1f}" width="96" height="{altura:.1f}" rx="10" fill="{cor}"/>'
                f'<text x="{x + 48}" y="{y - 12:.1f}" text-anchor="middle" font-size="15" fill="#0f172a">${valor:,.0f}</text>'
                f'<text x="{x + 48}" y="360" text-anchor="middle" font-size="15" fill="#334155">{label}</text>'
            )

        return self._salvar_svg("potencial_receita.svg", self._svg_document(width, height, "".join(body)))

    def gerar_graficos(self) -> list[Path]:
        return [
            self.gerar_grafico_funil(),
            self.gerar_grafico_clientes(),
            self.gerar_grafico_benchmark(),
            self.gerar_grafico_oportunidades(),
        ]

    def gerar_resumo_executivo(self) -> str:
        clientes_one_time = int(
            self.dados["total_clientes"] * self.dados["clientes_one_time_pct"] / 100
        )

        return f"""## Resumo Executivo

Esta análise avaliou a jornada de compra de um e-commerce a partir de 758.884 eventos, com foco em conversão, retenção e potencial de crescimento comercial. Os resultados mostram uma operação com receita relevante, mas com perdas expressivas ao longo do funil e oportunidade clara de aumento de valor por cliente.

### Principais métricas

| Métrica | Valor | Leitura |
| --- | ---: | --- |
| Receita total | ${self.dados['receita_total']:,.2f} | Base atual do negócio |
| Ticket médio | ${self.dados['ticket_medio']:.2f} | Potencial para aumento |
| Conversão `add_to_cart -> purchase` | {self.dados['taxa_conversao']:.2f}% | Principal gargalo |
| Conversão `add_to_cart -> checkout` | {self.dados['conversao_checkout']:.2f}% | Queda relevante |
| Conversão `checkout -> purchase` | {self.dados['conversao_compra']:.2f}% | Etapa crítica |
| Clientes recorrentes | {self.dados['clientes_recorrentes_pct']:.2f}% | Base com bom sinal de retenção |
| Clientes one-time | {self.dados['clientes_one_time_pct']:.2f}% | Espaço para reengajamento |

### Leitura executiva

- O principal problema do negócio está na baixa conversão entre carrinho e compra.
- O ticket médio ainda limita o crescimento da receita mesmo com volume relevante.
- A base possui bons sinais de recorrência, mas ainda perde aproximadamente {clientes_one_time:,} clientes após a primeira compra.
- Há oportunidade de captura de valor em três frentes: recuperação de carrinho, retenção e aumento de ticket médio.

### Visualizações

![Funil de conversão](./images/funil_conversao.svg)

![Composição da base de clientes](./images/composicao_clientes.svg)
"""

    def gerar_analise_detalhada(self) -> str:
        checkout_iniciado = self.dados["add_to_cart"] * (self.dados["conversao_checkout"] / 100)
        receita_por_cliente = self.dados["receita_total"] / self.dados["total_clientes"]

        return f"""## Análise Detalhada

### Panorama da base

- Total de eventos: {self.dados['total_eventos']:,.0f}
- Total de clientes: {self.dados['total_clientes']:,.0f}
- Total de produtos: {self.dados['total_produtos']:,.0f}
- Receita por cliente: ${receita_por_cliente:.2f}

### Funil de conversão

| Etapa | Volume | Taxa sobre `add_to_cart` |
| --- | ---: | ---: |
| Add to cart | {self.dados['add_to_cart']:,.0f} | 100.00% |
| Checkout iniciado | {checkout_iniciado:,.0f} | {self.dados['conversao_checkout']:.2f}% |
| Compra concluída | {self.dados['purchases']:,.0f} | {self.dados['taxa_conversao']:.2f}% |

### Diagnóstico

1. A maior perda acontece entre carrinho e checkout, o que sugere fricção relevante no processo de compra.
2. A segunda perda relevante ocorre na etapa final, entre checkout e compra, possivelmente ligada a pagamento, custo final ou experiência.
3. O ticket médio baixo reduz o potencial de receita por pedido e aponta espaço para estratégias de upsell e cross-sell.
4. A presença de clientes one-time mostra que a empresa ainda pode amadurecer suas ações de CRM e retenção.

### Benchmark de referência

| Indicador | Projeto | Referência de mercado | Interpretação |
| --- | ---: | ---: | --- |
| Conversão `add_to_cart -> purchase` | {self.dados['taxa_conversao']:.2f}% | 3% a 5% | Abaixo da média |
| Clientes recorrentes | {self.dados['clientes_recorrentes_pct']:.2f}% | 60% a 70% | Sinal positivo |
| Ticket médio | ${self.dados['ticket_medio']:.2f} | $45 a $75 | Abaixo da referência |

![Comparação com benchmark de mercado](./images/benchmark_mercado.svg)
"""

    def gerar_plano_acao(self) -> str:
        ganho_carrinho = 228000
        ganho_retencao = 418000
        ganho_ticket = 138000

        return f"""## Plano de Ação

### Prioridade 1: Recuperação de carrinho abandonado

- Objetivo: reduzir a perda entre `add_to_cart` e compra.
- Impacto estimado: +${ganho_carrinho:,.0f} em receita.
- Ações sugeridas:
  - fluxo de email de recuperação em 3 etapas;
  - revisão do checkout para reduzir atrito;
  - teste de incentivo pontual para fechamento de compra.

### Prioridade 2: Retenção de clientes

- Objetivo: aumentar recompra e reduzir a proporção de clientes one-time.
- Impacto estimado: +${ganho_retencao:,.0f} em receita.
- Ações sugeridas:
  - sequência de relacionamento pós-compra;
  - campanha de reengajamento;
  - programa simples de fidelização ou benefícios.

### Prioridade 3: Aumento do ticket médio

- Objetivo: elevar o valor médio por pedido.
- Impacto estimado: +${ganho_ticket:,.0f} em receita.
- Ações sugeridas:
  - recomendação de produtos complementares;
  - incentivo por faixa de valor;
  - bundles ou kits promocionais.

### Priorização sugerida

1. Carrinho abandonado
2. Retenção de clientes
3. Aumento de ticket médio

![Potencial de receita por iniciativa](./images/potencial_receita.svg)
"""

    def gerar_monitoramento(self) -> str:
        return f"""## Monitoramento

### KPIs principais

| KPI | Baseline | Meta inicial |
| --- | ---: | ---: |
| Conversão `add_to_cart -> purchase` | {self.dados['taxa_conversao']:.2f}% | 3.50% |
| Ticket médio | ${self.dados['ticket_medio']:.2f} | $23.00 |
| Clientes recorrentes | {self.dados['clientes_recorrentes_pct']:.2f}% | 80.00% |
| Receita por cliente | ${self.dados['receita_total'] / self.dados['total_clientes']:.2f} | $90.00 |

### Rotina sugerida

- acompanhar os KPIs semanalmente;
- revisar desempenho das iniciativas a cada 30 dias;
- registrar testes, aprendizados e próximas iterações.
"""

    def gerar_relatorio_markdown(self) -> str:
        return f"""# {self.config.titulo}

{self.config.subtitulo}

**Autora:** {self.config.autor}  
**Data:** {self.config.data_geracao}

---

{self.gerar_resumo_executivo()}

---

{self.gerar_analise_detalhada()}

---

{self.gerar_plano_acao()}

---

{self.gerar_monitoramento()}

---

## Arquivos de apoio

- `ecommerce_customer_analysis.ipynb`: notebook com a análise exploratória completa.
- `reports/dados_resumidos.json`: resumo estruturado das métricas do relatório.
- `reports/images/`: gráficos exportados para leitura direta no GitHub.
- `relatorio_ecommerce_completo.py`: script para regenerar os arquivos desta seção.
"""

    def salvar_markdown(self) -> Path:
        caminho = self.config.dir_saida / "relatorio_executivo.md"
        caminho.write_text(self.gerar_relatorio_markdown(), encoding="utf-8")
        return caminho

    def salvar_json(self) -> Path:
        payload = {
            "metadata": {
                "titulo": self.config.titulo,
                "subtitulo": self.config.subtitulo,
                "autor": self.config.autor,
                "data_geracao": self.config.data_geracao,
            },
            "metricas": self.dados,
            "projecoes": {
                "ganho_carrinho_abandonado": 228000,
                "ganho_retencao": 418000,
                "ganho_ticket_medio": 138000,
            },
        }

        caminho = self.config.dir_saida / "dados_resumidos.json"
        caminho.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return caminho

    def gerar(self) -> tuple[Path, Path]:
        self.gerar_graficos()
        return self.salvar_markdown(), self.salvar_json()


def main() -> None:
    gerador = GeradorRelatorio()
    md_path, json_path = gerador.gerar()
    print(f"Relatório salvo em: {md_path}")
    print(f"Resumo estruturado salvo em: {json_path}")


if __name__ == "__main__":
    main()
