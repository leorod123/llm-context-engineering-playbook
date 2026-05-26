# LLM Context Engineering Playbook

**Uma camada de governança de contexto para desenvolvimento assistido por IA.**

Este projeto surgiu a partir da observação de um problema recorrente em fluxos de trabalho com agentes de programação (Codex, Claude, Copilot e similares): em projetos reais, os erros mais graves raramente acontecem porque o modelo não sabe programar.

Na prática, muitos erros acontecem porque o agente recebe contexto incompleto, desatualizado, ambíguo ou sem validação adequada.

O objetivo deste projeto é organizar conhecimento de projeto de forma que agentes consigam responder perguntas importantes:

- Qual informação é realmente confiável?
- O que é hipótese e o que já foi validado?
- Qual documento possui autoridade sobre determinado assunto?
- Quais limitações ainda existem?
- Quais partes do sistema podem ser impactadas por uma mudança?
- O contexto encontrado é suficiente para tomar uma decisão?

A proposta não é fazer o agente ler mais documentação.

A proposta é fazer o agente ler o contexto correto, com o nível correto de confiança e com limitações explícitas.

---

# Como o projeto surgiu

Durante auditorias de projetos reais utilizando agentes de IA, foi possível observar padrões recorrentes de falha.

Alguns exemplos:

### Deriva de contexto (Context Drift)

O agente continua raciocinando a partir de planos antigos mesmo após o código já ter evoluído.

### Colapso de autoridade (Authority Collapse)

Notas preliminares, rascunhos, planos de migração e documentação validada passam a ser tratados como se tivessem o mesmo peso.

### Lacuna entre implementação e comportamento

O código existe, mas não há evidência suficiente de que o comportamento real corresponde ao projeto original.

### Cegueira de dependências

Uma alteração parece correta localmente, mas viola pressupostos importantes em outro subsistema.

### Sobrecarga de contexto

Adicionar mais documentação piora a qualidade da resposta porque o agente perde capacidade de distinguir o que é realmente relevante.

---

# A hipótese central

A hipótese deste projeto é simples:

> Muitos problemas atribuídos aos modelos são, na verdade, problemas de governança de contexto.

Se conseguirmos organizar documentos, evidências, validações e níveis de confiança de forma explícita, os agentes passam a tomar decisões melhores mesmo sem alterar o modelo utilizado.

---

# O que este projeto demonstra

Mais do que uma ferramenta, este repositório procura demonstrar uma forma de pensar sobre desenvolvimento assistido por IA.

Ele demonstra:

- investigação sistemática de falhas em fluxos com LLMs;
- engenharia de contexto para agentes de programação;
- separação entre histórico bruto e conhecimento operacional;
- uso de metadados para representar maturidade e evidência;
- mecanismos de validação antes da promoção de contexto;
- recuperação de contexto explicável;
- documentação orientada a auditoria;
- processos para reduzir decisões baseadas em inferência não validada.

---

# Conceito principal

Cada documento pode declarar metadados sobre seu estado:

```yaml
validation_state: implementation_validated
semantic_status: partially_validated
bot_usage: restricted
evidence_status: partial
```

Essas informações permitem responder perguntas como:

- O documento pode ser descoberto?
- O agente pode confiar nele?
- Existe validação semântica?
- Existe evidência?
- Ainda há limitações relevantes?
- O contexto é seguro para uso operacional?

A ideia principal é simples:

> Contexto descoberto não significa contexto confiável.

---

# Componentes do projeto

## Registry

Transforma documentos estruturados em um catálogo consultável.

Permite localizar rapidamente:

- projetos;
- auditorias;
- validações;
- registros operacionais;
- contratos;
- documentos relacionados.

---

## Validation

Verifica regras de maturidade e promoção.

Ajuda a evitar que hipóteses ou documentos incompletos sejam tratados como verdade operacional.

---

## Discovery

Seleciona um conjunto pequeno e explicável de contexto relevante.

O objetivo não é maximizar quantidade de informação.

O objetivo é maximizar relevância e transparência.

---

## Contracts

Conjunto de contratos reutilizáveis que definem:

- modos de operação;
- critérios de validação;
- tratamento de contexto bruto;
- impacto entre sistemas;
- limites operacionais.

---

# Estrutura do repositório

```text
docs/
├─ method/
├─ contracts/
├─ templates/

src/
└─ context_governance/

examples/
└─ synthetic_saas/

tests/
```

---

# Exemplo rápido

```powershell
python -m pip install -e .

python -m context_governance build ^
  --root examples/synthetic_saas

python -m context_governance validate ^
  --root examples/synthetic_saas

python -m context_governance discover ^
  --root examples/synthetic_saas ^
  --system billing
```

Fluxo esperado:

1. Construir o registry.
2. Validar regras de maturidade.
3. Descobrir contexto relevante.
4. Receber limitações explícitas junto com o resultado.

---

# O que este projeto NÃO é

Este projeto não é:

- um banco vetorial;
- um sistema de RAG completo;
- uma plataforma SaaS;
- uma ferramenta de observabilidade;
- uma solução proprietária específica de um projeto.

Ele procura permanecer pequeno, auditável e adaptável.

A intenção é funcionar apenas com:

- arquivos;
- metadados;
- regras explícitas;
- validações determinísticas.

---

# Privacidade

Este repositório utiliza apenas exemplos sintéticos.

Ao adaptar a metodologia para projetos reais, recomenda-se não publicar:

- documentação interna;
- dados de produção;
- logs operacionais;
- credenciais;
- caminhos locais;
- informações de clientes;
- detalhes sensíveis de arquitetura.

---

# Validação empírica

O repositório inclui uma avaliação sintética antes/depois em `evals/`.

O resultado atual dos fixtures é:

| Métrica | Baseline | Com Playbook |
| --- | ---: | ---: |
| Score total | 6 / 30 | 28 / 30 |
| Score médio por cenário | 1.2 / 6 | 5.6 / 6 |
| Score geral | 20.0% | 93.3% |

Essa avaliação é deliberadamente pequena, controlada e auditável. As respostas
incluídas são fixtures sintéticos, não uma chamada ao vivo para um modelo. Para
testar um modelo real, use o protocolo em `evals/manual_protocol.md` e substitua
as respostas em `evals/runs/` por outputs capturados com o mesmo modelo e as
mesmas configurações.

Limitação importante: o benchmark mede os modos de falha cobertos pelo
playbook. Ele não deve ser apresentado como uma métrica universal de desempenho
de LLMs.

---

# Estado atual

Esta é uma versão pública funcional da metodologia, com CLI executável, exemplo sintético, avaliação determinística, testes e CI via GitHub Actions.

O objetivo não é apresentar uma solução definitiva.

O objetivo é abrir a discussão sobre um tema que tende a se tornar cada vez mais importante:

> Como transformar grandes quantidades de documentação, histórico e conhecimento de projeto em contexto realmente confiável para agentes de IA?
