# Rúbrica — PLAB1 Mini-Agentic-RAG

> Avaluació del repte CineMatch-RAG. Grups de **1-2 alumnes**.
> Nota sobre 10. Mínim 5/10 per superar la part pràctica del Tema 3 (guia docent).
> S'avalua el **nivell màxim assolit I FUNCIONANT**, no el nivell intentat.

---

## 1. Estructura de la nota (6 canals d'evidència)

| Canal | Pes | Què mesura | Com es comprova |
|---|---|---|---|
| **A · Funcionalitat (N1→N4)** | **45%** | Cada nivell funciona end-to-end | Tests automàtics del professor sobre el repo |
| **B · Qualitat tècnica** | **15%** | Codi reproduïble, estructura, **MAI** secrets | Validador automàtic + static analysis |
| **C · Decisions documentades** | **15%** | `DECISIONS.md` justifica params/model/patró | Lectura amb rúbrica |
| **D · Defensa escrita (Q&A)** | **15%** | 5 preguntes obligatòries a `docs/demo.md` | Lectura amb rúbrica estricta |
| **E · Evidència d'execució** | **5%** | Activitat real al cluster (profile) | `system.profile` analitzat per NIU |
| **F · Transparència IA** | **5%** | `IA_REPORT.md` honest sobre ús del bot PROFE | Lectura profe |

Nota final = 0,45·A + 0,15·B + 0,15·C + 0,15·D + 0,05·E + 0,05·F.

> **Regla anti-"N4 trencat":** un nivell només compta si **funciona de forma
> reproduïble** des d'un clone net del repositori. Un N4 que peta val com el
> darrer nivell inferior que sí funciona.

---

## 2. Canal A — Funcionalitat (45%)

Es pren el **nivell més alt completament funcional**. Nota base del canal A:

| Nivell assolit i funcionant | Punts canal A (sobre 10) |
|---|---|
| Res funcional / només connexió | 0–3 |
| **N1** — Semantic Search correcte | 5 |
| **N2** — RAG amb prompt defensiu | 6,5 |
| **N3** — Tools + Structured Outputs | 8 |
| **N4** — Multi-agent amb reintent | 10 |

### Criteris d'acceptació per nivell (checklist binari verificable)

**N1 — Semantic Search**

- [ ] Índex `vectorSearch` creat correctament (1536, `cosine`, `filter` sobre `year`)
- [ ] La query s'embeu amb **`text-embedding-ada-002`** (mateix model que el corpus)
- [ ] Pipeline amb `$vectorSearch` (`numCandidates` > `limit`); retorna 5 resultats coherents
- [ ] Es mostra `vectorSearchScore`

**N2 — RAG** (a més de N1)

- [ ] Recupera top-k i construeix prompt augmentat amb el context
- [ ] Prompt **defensiu**: davant pregunta sense resposta al context, **diu que NO ho sap** (NO inventa pel·lícules)
- [ ] La resposta **cita** els títols usats com a font

**N3 — Tools + Structured Outputs** (a més de N2)

- [ ] ≥2 tools definides (function calling) amb schema vàlid
- [ ] Loop multi-torn correcte (model → tool_call → result → model)
- [ ] Sortida final **estructurada i validada** (Pydantic / JSON schema)

**N4 — Multi-agent** (a més de N3)

- [ ] ≥2 subagents amb rol diferenciat i un orquestrador documentat
- [ ] Patró **evaluator-optimizer**: cas demostrat on es **reintenta** la recuperació
- [ ] Diagrama del flux + traça d'execució amb el reintent

---

## 3. Canal B — Qualitat tècnica (15%)

Checklist binari (1,25 pts cada un, sobre 10):

- [ ] `uv sync && uv run python -m src.n1_semantic_search "test"` funciona des de clone net
- [ ] `.env` NO committejat; `.gitignore` el cobreix
- [ ] Cap API key hardcoded al codi
- [ ] Estructura de carpetes exacta (validador d'estructura passa)
- [ ] Paràmetres declarats (no magic numbers): `numCandidates`, `limit`, `k`, `temperature`
- [ ] Imports nets (sense `import *`, sense dead code obvi)
- [ ] `numCandidates > limit` (regla aNN respectada)
- [ ] Embed model = `text-embedding-ada-002` (matching corpus)

---

## 4. Canal C — Decisions documentades (15%)

`DECISIONS.md` ha de documentar **almenys 5 decisions** amb trade-off explícit
(3 pts cada una, sobre 15, escalat a 10):

1. Per què `k = N` (no més, no menys)
2. Per què `numCandidates = M`
3. Per què aquest `CHAT_MODEL`
4. Per què aquest patró d'orquestració (chaining / routing / evaluator-optimizer / multi-agent)
5. Una **alternativa rebutjada** i el motiu

Rúbric per decisió:

| Qualitat | Punts |
|---|---|
| Absent o tautologia ("perquè sí") | 0 |
| Valor declarat sense justificació | 1 |
| Justificació amb trade-off explícit | 2 |
| A més, valors alternatius valorats i descartats amb criteri | 3 |

---

## 5. Canal D — Defensa escrita (Q&A) (15%)

A `docs/demo.md`, secció **"Defensa escrita"**, responen OBLIGATÒRIAMENT
aquestes **5 preguntes** (3 pts cada una, sobre 15, escalat a 10):

1. *Què passa si embeus la query amb `text-embedding-3-small` en lloc d'`ada-002`?*
2. *Per què `numCandidates` ha de ser > `limit`? Què passa si poses `numCandidates == limit`?*
3. *Si el `$vectorSearch` NO troba res rellevant, què retorna el teu RAG?*
4. *Per què trieu `cosine` i NO `euclidean` / `dotProduct`?*
5. *(N4)* Quina condició fa que l'orquestrador reintenti? Com evites el bucle infinit?
   *(N3 o inferior)* Per què la sortida estructurada (JSON schema) val més que text lliure?

Rúbric per resposta:

| Qualitat | Punts |
|---|---|
| No menciona cap concepte clau o és incorrecte | 0 |
| Menciona 1–2 conceptes però incomplet | 1,5 |
| Cobreix els 2–3 conceptes amb claredat i exemple | 3 |

> **Nota.** Aquestes preguntes són **públiques** abans del lliurament. Les
> responeu al vostre ritme al fitxer `docs/demo.md`.

---

## 6. Canal E — Evidència d'execució (5%)

Sobre el `system.profile` del vostre `cinematch_<NIU>` al cluster del curs.
**Gates binaris** (no compleixen → puntuació canal A penalitzada):

- [ ] **Setup**: hi ha evidència del `$merge` o la col·lecció `embedded_movies` té ~3 500 docs
- [ ] **Índex**: hi ha registre de `createSearchIndexes` amb la spec correcta (`numDimensions:1536`, `similarity:"cosine"`, `path:"plot_embedding"`)
- [ ] **Activitat real**: ≥ 3 operacions `$vectorSearch` registrades sota el vostre usuari `s_<NIU>`

**Senyal soft** (cap a la nota del canal E, 5 pts):

- [ ] Paràmetres raonables: `numCandidates` ∈ [50, 500], `limit` ∈ [1, 20] (2 pts)
- [ ] Diversitat de queries: ≥ 3 query vectors diferents (no la mateixa repetida) (1 pt)
- [ ] Distribució temporal: ≥ 2 sessions de treball separades (2 pts) — anti procrastinació última nit

---

## 7. Canal F — Transparència IA (5%)

`IA_REPORT.md` (al vostre repositori, al directori `docs/`):

- [ ] Present i no buit (>200 caràcters) (1 pt)
- [ ] Llista herramientas/IAs concretes usades durant el desenvolupament (1 pt)
- [ ] Per a cada IA: per què, què va fer, què van verificar ells (2 pts)
- [ ] Honest: secció "el que NO entenem del tot" omplerta (1 pt)

---

## 8. Penalitzacions i gates duros

| Situació | Efecte |
|---|---|
| Clau OpenAI o `.env` committejada (qualsevol commit, qualsevol moment) | **−2 punts globals** + rotació immediata de la clau |
| Estructura del repositori incorrecta (validador falla) | **NO s'avalua** (cal corregir abans del lliurament) |
| `n_vector_searches == 0` al profile AND tests CI verds | **Bandera roja: revisió manual** (sospita de hardcoded outputs) |
| Cap altra IA que NO sigui PROFE detectada sense declarar | **−3 punts globals** + revisió de tota la pràctica |
| Modificar `sample_mflix.embedded_movies` (col·lecció compartida) | **−1 punt** |
| `IA_REPORT.md` clarament fals o absent | **Canal F = 0** |
| Lliurament fora de termini (després 5 jun 08:30) | Segons normativa general del curs |
