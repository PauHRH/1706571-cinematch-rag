# DECISIONS — `<grup>`

Documenteu cada decisió no-òbvia amb el seu trade-off. **Avaluat al Canal C de
la rúbrica (15%)**. Cal almenys 5 decisions amb trade-off explícit per a la
nota completa. Sigueu breus; un bullet per decisió, sempre amb un **per què**.

## Retrieval
- **k / limit** = `_`. Why: `_____`
- **numCandidates** = `_`. Why (recall vs latency): `_____`
- **similarity** = `cosine` / `dotProduct` / `euclidean`. Why: `_____`
- **pre-filter** used? on which field (`year`?): `_____`. Why pre- and not post-filter: `_____`

## Embeddings
- **EMBED_MODEL** = `text-embedding-ada-002`. Why this exact model (not just 1536-d): `_____`

## RAG (N2+)
- **Chunking**: N/A (we use the precomputed plot embedding) / or describe: `_____`
- **Defensive prompt**: what instruction prevents hallucination: `_____`
- **CHAT_MODEL** = `_____`. Why: `_____`

## Agent / Multi-agent (N3/N4)
- **Tools defined**: `_____`
- **Architecture pattern** (chaining / routing / evaluator-optimizer / parallel): `_____`. Why: `_____`
- **Retry / stop condition** (N4): `_____`

## Alternatives considered and rejected
- `_____` rejected because `_____`
