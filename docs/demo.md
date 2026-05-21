# demo.md — `<grup>`

Aquest fitxer és **obligatori**. Conté dues parts:

1. **Traça d'execució** per cada nivell lliurat (captures, exemples, sortides reals)
2. **Defensa escrita (Q&A)** — 5 preguntes obligatòries (Canal D del rúbric, 15%)

---

## 1. Traça d'execució per nivell

### N1 — Semantic Search

Comanda executada:

```bash
uv run python -m src.n1_semantic_search "_____"
```

Sortida real (top-5 pel·lícules amb `vectorSearchScore`):

```
_____
```

(Repetiu amb 3 queries diferents per demostrar que funciona; almenys una ha de
ser semàntica — sense la paraula clau literal al títol.)

### N2 — RAG (si arribeu)

**Cas positiu** (resposta basada al context):

- Query: `_____`
- Top-k títols recuperats: `_____`
- Resposta de l'LLM (ha de citar títols): `_____`

**Cas negatiu** (sense context → ha de dir "no ho sé"):

- Query: `_____`
- Resposta esperada: `_____`
- Resposta obtinguda: `_____`

### N3 — Tools + Structured Outputs (si arribeu)

3 casos que exerciten **rutes diferents** (cerca / filtre / no trobat):

1. `_____`
2. `_____`
3. `_____`

Esquema de sortida (Pydantic o JSON schema):

```python
_____
```

Exemple de sortida estructurada:

```json
_____
```

### N4 — Multi-agent (si arribeu)

Diagrama del flux d'agents (ASCII o referència a `agent_flow_diagram.png`):

```
_____
```

Traça d'una execució amb **reintent** (cas evaluator-optimizer):

```
_____
```

---

## 2. Defensa escrita (Q&A) — **OBLIGATÒRIA**

Responeu OBLIGATÒRIAMENT aquestes **5 preguntes**. Cadascuna avaluada de
0 / 1,5 / 3 punts segons completitud de la resposta (veure rúbrica). Sigueu
breus i precisos.

### Q1 · Què passa si embeus la query amb `text-embedding-3-small` en lloc d'`ada-002`?

_____

### Q2 · Per què `numCandidates` ha de ser > `limit`? Què passa si poses `numCandidates == limit`?

_____

### Q3 · Si el `$vectorSearch` NO troba res rellevant, què retorna el teu RAG? Per què?

_____

### Q4 · Per què trieu `cosine` i NO `euclidean` / `dotProduct`?

_____

### Q5 (trieu UNA segons el vostre nivell màxim)

**Si heu fet N4:** Quina condició fa que l'orquestrador reintenti? Com evites el bucle infinit?

**Si heu arribat fins a N3 o inferior:** Per què la sortida estructurada (JSON schema) val més que una resposta en text lliure? Posa un exemple concret on un text lliure us hauria fallat.

_____
