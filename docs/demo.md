# demo.md — `17`

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
Si utilitzem el model text-embedding-3-small enlloc de l'ada-002 per la query, segurament el sistema retornarà resultats aleatoris i per tant, incorrectes. Cada model entén el llenguatge i distribueix els conceptes en un espai matemàtic diferent. Com que la col·lecció sample_mflix.embedded_movies ja ve precalculada per ada-002, si utilitzem el text-embedding-3-small el $vectorSearch de MongoDB calcularà erròniament les distàncies.
_____

### Q2 · Per què `numCandidates` ha de ser > `limit`? Què passa si poses `numCandidates == limit`?
El paràmetre numCandidates és el nombre de nodes veïns potencials que l'algoritme explorarà durant la cerca, mentre que limit és la quantitat de documents finals que s'acaben retornant a l'usuari. numCandidates ha de ser major que limit perquè la primera fa referència a la fase d'exploració i la segona la de selecció, per tant, lògicament no té sentit. Si fossin iguals l'algoritme haurà d'aturar la seva exploració ja que no tindrà marge. Hi haurà una pèrdua de qualitat i eficàcia en els reusltats.
_____

### Q3 · Si el `$vectorSearch` NO troba res rellevant, què retorna el teu RAG? Per què?
Retornarà textualment una resposta de negació. En el nostre cas I don't know, perquè quan hem construït el prompt hem afegit una cláusula estricta: Answer only using the provided context. If the context doesn't containt the answer, say that you don't know. Do not invent movies.
_____

### Q4 · Per què trieu `cosine` i NO `euclidean` / `dotProduct`?
Principalment per coincidència amb l'origen de les dades i per la naturalesa de la cerca de text en RAG. El corpus original de la base de dades es va indexar en origen utilitzant la mètrica cosine per tant, aquesta coincidència tècnica és obligatòria. A part, la mètrica cosine mesura l'angle entre dos vectors ignorant la seva longitud. No es podria fer amb dotProduct ja que la magnitud poden tenir variacions. L'euclidean mira les distàncies en línia recta si una és molt més llarga que l'altra
_____

### Q5 (trieu UNA segons el vostre nivell màxim)

**Si heu fet N4:** Quina condició fa que l'orquestrador reintenti? Com evites el bucle infinit?

**Si heu arribat fins a N3 o inferior:** Per què la sortida estructurada (JSON schema) val més que una resposta en text lliure? Posa un exemple concret on un text lliure us hauria fallat.

_____
