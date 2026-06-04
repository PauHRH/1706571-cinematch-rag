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
El paràmetre numCandidates indica quants candidats explorarà l'algorisme abans de seleccionar els resultats finals. En MongoDB Atlas Vector Search s'utilitza un índex basat en HNSW, que realitza una cerca aproximada (Approximate Nearest Neighbors, ANN) navegant per un graf de veïns. Per aquest motiu, numCandidates ha de ser superior a limit: primer s'explora un conjunt ampli de candidats i després es seleccionen els limit millors resultats.

Si numCandidates == limit, l'espai d'exploració és molt reduït i HNSW podria no visitar alguns veïns rellevants del graf. Això disminueix el recall i pot provocar que es retornin documents menys similars que els realment més propers al vector de consulta.

### Q3 · Si el `$vectorSearch` NO troba res rellevant, què retorna el teu RAG? Per què?
Quan $vectorSearch no retorna documents amb una similitud suficient, la funció retorna una llista buida. El prompt del sistema indica explícitament que, en aquest cas, el model ha de respondre "I don't know" (o answered=false en la versió amb sortida estructurada) i no inventar informació.
_____

### Q4 · Per què trieu `cosine` i NO `euclidean` / `dotProduct`?
Triem cosine similarity perquè els embeddings de text codifiquen principalment informació semàntica en la direcció del vector. Cosine compara l'angle entre vectors i és relativament independent de la seva magnitud, fet que la fa especialment adequada per a cerca semàntica.

En canvi, euclidean distance depèn de la longitud dels vectors i dues representacions semànticament similars podrien aparèixer llunyanes si tenen magnituds diferents. Dot product també és sensible a la magnitud, de manera que vectors més llargs poden obtenir puntuacions elevades encara que no siguin els més similars semànticament.

Per aquest motiu, cosine és la mètrica habitual en sistemes RAG basats en embeddings textuals.

### Q5 (trieu UNA segons el vostre nivell màxim)

**Si heu fet N4:** Quina condició fa que l'orquestrador reintenti? Com evites el bucle infinit?

**Si heu arribat fins a N3 o inferior:** Per què la sortida estructurada (JSON schema) val més que una resposta en text lliure? Posa un exemple concret on un text lliure us hauria fallat.

_____
