# CineMatch-RAG — PLAB starter (Tema 3 · ATS 2025-26)

Mini-Agentic-RAG sobre `sample_mflix.embedded_movies` (Atlas Vector Search + OpenAI).
Llegiu el repte complet a **[`enunciat_mini_agentic_rag.pdf`](enunciat_mini_agentic_rag.pdf)** i la
rúbrica d'avaluació a **[`rubrica_niveles.md`](rubrica_niveles.md)**. Aquesta
plantilla us dóna un **N1 funcional**; construïu N2 → N4 a sobre.

> **Grup:** `_____` · **Membres:** `_____`
> **Nivell màxim assolit:** `N_` (actualitzeu abans del lliurament)

---

## 1. Setup

```bash
cp .env.example .env          # ompliu MONGODB_URI, OPENAI_API_KEY, DB_NAME
uv sync                       # crea .venv i instal·la deps
```

Al `.env`, fixeu **`DB_NAME=cinematch_<NIU_lider>`** (substituïu pel NIU d'un
membre del grup). Treballareu sempre sobre **aquesta BD pròpia**, no sobre
`sample_mflix`.

**MAI** committegeu `.env` (està al `.gitignore`). Una clau committejada =
penalització + rotació immediata.

## 2. Copieu el corpus a la vostra BD i creeu l'índex vectorial (una sola vegada)

NO teniu accés d'escriptura a `sample_mflix` (és compartit). Copieu el corpus a
la vostra BD amb mongosh:

```js
use cinematch_<NIU_lider>            // p.ex. cinematch_1703702
db.embedded_movies.drop()            // per si ja existia

// IMPORTANT: $merge (no $out). Atlas no permet $out cross-database
// per als usuaris s_<NIU>; $merge sí está permès i té el mateix efecte.
db.getSiblingDB("sample_mflix").embedded_movies.aggregate([
  { $merge: {
      into: { db: "cinematch_<NIU_lider>", coll: "embedded_movies" },
      on: "_id",
      whenMatched: "replace",
      whenNotMatched: "insert"
  } }
])
db.embedded_movies.countDocuments()  // ha de donar ~3 500
```

Després creeu l'índex vectorial sobre la **vostra** col·lecció:

```js
db.embedded_movies.createSearchIndex(
  "vectorPlotIndex",
  "vectorSearch",
  { fields: [
      { type: "vector", path: "plot_embedding",
        numDimensions: 1536, similarity: "cosine" },
      { type: "filter", path: "year" }
  ]}
)
// El camp `queryable` triga 2-3 min en passar a true (no 1 min com sembla
// inicialment — `createSearchIndex` retorna OK abans que mongot acabi).
// Espereu fins veure queryable:true ABANS de córrer N1.
db.embedded_movies.getSearchIndexes()
```

(Alternativa: Atlas UI → la vostra BD → `embedded_movies` → Search Indexes → Create.)

## 3. Executeu N1

```bash
uv run python -m src.n1_semantic_search "space movies where humanity is in danger"
```

Esperat: 5 pel·lícules ordenades per `vectorSearchScore`, semànticament
relacionades amb la consulta. Si funciona, el N1 base està OK — construïu a sobre.

---

## ⚠️ Regla d'embedding-model (llegir-ho)

La query **ha** de ser embeguda amb el **mateix model** que el corpus
(`text-embedding-ada-002`). La dimensió coincident (1536) **NO** n'hi ha prou:
`text-embedding-3-small` també és 1536-d però viu en un espai semàntic diferent
→ resultats com soroll. `EMBED_MODEL` al `.env` ja està al valor correcte; **NO
el canvieu** tret que regenereu tot el corpus (fora de l'abast de PLAB).

---

## 🔴 Política d'IA del curs

L'única IA permesa per al desenvolupament és el bot **PROFE** del curs (Discord).
**NO** està permès usar cap altra IA (Claude Code, Claude Copilot, ChatGPT,
GitHub Copilot, etc.). NO s'accepta lliurar codi que NO sapigueu explicar.

## ⚠️ Auditoria automàtica del cluster

El cluster del curs té el **profiler de MongoDB actiu**. Tota l'activitat
contra la vostra `cinematch_<NIU>` queda registrada al `system.profile`
(queries `$vectorSearch`, paràmetres, timestamps). **Forma part de
l'avaluació**: un repositori amb tests verds però sense activitat real al
cluster es considera no executat.

---

## 4. Estructura del repositori (obligatòria)

```
<NIU_lider>-cinematch-rag/
├── README.md          ← com executar + nivell assolit + decisions
├── .env.example       ← (MAI pujar .env real ni claus)
├── pyproject.toml
├── src/ o notebook.ipynb
│   ├── n1_semantic_search.py    ← proporcionat, funciona
│   ├── n2_rag.py                ← VOSALTRES: retriever + generator
│   ├── n3_agent_tools.py        ← VOSALTRES: function calling + JSON
│   └── n4_multiagent.py         ← VOSALTRES: orquestrador + subagents
├── docs/
│   ├── DECISIONS.md   ← per què k / numCandidates / model — trade-offs
│   ├── demo.md        ← traça de cada nivell + Q&A escrita (5 preguntes obligatòries)
│   └── IA_REPORT.md   ← registre d'ús del bot PROFE
└── (N4) diagrama del flux d'agents (PNG o ASCII)
```

**NO s'avaluaran lliuraments que NO segueixin aquesta estructura exacta.** Es
publicarà un validador automàtic al canal [#pràctiques-s1](https://discord.com/channels/1468871413371768926/1468871413988331657) per comprovar-ho abans del
lliurament.

N4 amb LangGraph: `uv sync --extra n4` (ja és a `pyproject.toml`).

## 5. Lliurament

- Push al vostre repositori GitHub privat. **Afegir el professor com a
  col·laborador:** GitHub user `albertgilopez`.
- **Lliurament via Campus Virtual abans del 5 juny 2026, 08:30 h.**
- `docs/IA_REPORT.md`, `docs/demo.md` i `docs/DECISIONS.md` són **obligatoris**.
- Reviseu que els tests del CI passen i que el `system.profile` mostra
  activitat (auditoria automàtica).

## 6. Avaluació — 6 canals d'evidència

Veure [`rubrica_niveles.md`](rubrica_niveles.md) per al detall. Resum:

| Canal | % | Eina |
|---|---|---|
| A · Funcionalitat (N1→N4) | 45% | Tests automàtics |
| B · Qualitat tècnica | 15% | Static analysis + validador estructura |
| C · Decisions documentades (`docs/DECISIONS.md`) | 15% | Lectura amb rúbrica |
| D · Defensa escrita (Q&A a `docs/demo.md`) | 15% | Lectura amb rúbrica |
| E · Evidència d'execució (profiler) | 5% | Anàlisi `system.profile` |
| F · Transparència IA (`docs/IA_REPORT.md`) | 5% | Lectura profe |
