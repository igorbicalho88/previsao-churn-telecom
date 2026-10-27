"""Cálculo financeiro de uma campanha de retenção de clientes.

Premissas (ajustáveis):
  - cada cliente contatado custa CUSTO_CONTATO (ligação, atendimento);
  - todo cliente contatado recebe uma oferta: desconto equivalente a MESES_DESCONTO mensalidades;
  - quem ia cancelar aceita a oferta e fica com probabilidade TAXA_RETENCAO;
    ficando, a empresa preserva MESES_VALOR mensalidades de receita (menos o desconto);
  - quem NÃO ia cancelar também aceita o desconto: é dinheiro dado sem necessidade.
"""
import numpy as np

CUSTO_CONTATO = 10      # US$ por cliente contatado
MESES_DESCONTO = 2      # desconto oferecido, em mensalidades
MESES_VALOR = 12        # receita preservada de um cliente retido, em mensalidades
TAXA_RETENCAO = 0.30    # % dos clientes que iam cancelar e ficam por causa da oferta


def lucro_real(contatar, churn, mensalidade, taxa=TAXA_RETENCAO):
    """Lucro da campanha, sabendo quem de fato cancelaria (usado para avaliar no teste)."""
    ganho = np.where(churn == 1,
                     taxa * (MESES_VALOR - MESES_DESCONTO) * mensalidade,  # cliente salvo (em média)
                     -MESES_DESCONTO * mensalidade)                         # desconto dado à toa
    return float(((ganho - CUSTO_CONTATO) * contatar).sum())


def lucro_esperado(prob, mensalidade, taxa=TAXA_RETENCAO):
    """Lucro esperado de contatar cada cliente, usando a probabilidade de churn do modelo."""
    return (prob * taxa * (MESES_VALOR - MESES_DESCONTO) * mensalidade
            - (1 - prob) * MESES_DESCONTO * mensalidade
            - CUSTO_CONTATO)
