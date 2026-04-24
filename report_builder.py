from __future__ import annotations

from datetime import datetime
from pathlib import Path


def _fmt_currency(value: float) -> str:
    return f"${value:,.2f}"


def _fmt_int(value: int) -> str:
    return f"{value:,}"


def _fmt_date(value) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    return str(value)


def build_final_report(metrics: dict) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    summary = f"""# Relatório Final - E-commerce Customer Analysis

Gerado em: {generated_at}

## Resumo executivo

O estudo avaliou o comportamento de compra em um e-commerce a partir de eventos de navegação, carrinho, checkout e compra. A análise identificou gargalos relevantes de conversão, forte influência de sazonalidade e uma base de clientes ainda concentrada em segmentos de menor maturidade.

## Principais métricas

- Receita total: {_fmt_currency(metrics['total_revenue'])}
- Ticket médio: {_fmt_currency(metrics['avg_ticket'])}
- Clientes com compra: {_fmt_int(metrics['total_customers'])}
- Clientes recorrentes: {_fmt_int(metrics['recurring_users'])} ({metrics['recurring_share']:.2f}%)
- Conversão `add_to_cart -> purchase`: {metrics['cart_to_purchase_rate']:.2f}%
- Conversão por sessão `add_to_cart -> checkout`: {metrics['session_checkout_rate']:.2f}%
- Conversão por sessão `add_to_cart -> purchase`: {metrics['session_purchase_rate']:.2f}%

## Destaques analíticos

- Categoria com maior receita: {metrics['top_category']} ({_fmt_currency(metrics['top_category_revenue'])})
- Produto com maior receita: {metrics['top_product']} ({_fmt_currency(metrics['top_product_revenue'])})
- Segmento RFM mais frequente: {metrics['top_segment']} ({_fmt_int(metrics['top_segment_count'])} clientes)
- Pico diário de receita: {_fmt_date(metrics['peak_revenue_day'])} ({_fmt_currency(metrics['peak_revenue_value'])})

## Recomendações de negócio

1. Priorizar a otimização do checkout para reduzir a perda entre intenção e compra.
2. Criar campanhas de retenção para clientes de maior valor e recorrência.
3. Explorar categorias com boa conversão para ganho rápido de receita.
4. Planejar ações comerciais fora do pico sazonal para reduzir dependência de datas promocionais.
5. Desenvolver estratégias de CRM para evoluir clientes frequentes em clientes de alto valor.

## Conclusão

Os dados mostram um e-commerce com volume operacional relevante e espaço claro para ganho de eficiência comercial. As maiores oportunidades estão na melhoria do funil, na retenção de clientes valiosos e na redução da dependência de sazonalidade.
"""

    return summary


def save_final_report(report_text: str, output_path: str = "reports/final_report.md") -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report_text, encoding="utf-8")
    return output
