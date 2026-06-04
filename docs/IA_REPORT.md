# IA_REPORT — `17`

**Obligatori.** Honest i específic.

## Política d'IA del curs

L'única IA permesa per al desenvolupament d'aquesta pràctica és el bot **PROFE**
del curs (Discord). **NO** està permès usar cap altra IA (Claude Code, Claude
Copilot, ChatGPT, GitHub Copilot, etc.). **NO s'accepta lliurar codi que NO
sapigueu explicar.**

## Registre d'ús del bot PROFE

| Data | Pregunta feta a PROFE | Resposta resumida | Què hem verificat nosaltres |
|---|---|---|---|
| (data) | (la pregunta literal) | (resum del que PROFE ha dit) | (com hem comprovat que té sentit, p. ex. re-executat, llegit docs MongoDB, etc.) |
|03/06|  Q2 · Per què numCandidates ha de ser > limit? Què passa si poses numCandidates == limit?|M'ha explicat el concepte del perquè HNSW necessita més candidats que resultats i per lògica ho hem estès.| Hem comprovat i tenia sentit això i al cap d'un temps ens hem adonat que la pregunta era bastant bàsica. |
|03/06| que falla del C2 en N3? + codi   | M'ha comentat on estava la principal problemàtica que impedia que pogués passar els testos, en aquest cas que max_turns no tenia assignat cap valor per defecte. |Ho hem verificat tornant a executar les consultes i seguidament passant el validate.   |
| 03/06 | (en referència a l'anterior) 5 estaria bien? | M'ha comentat que un valor entre 3 i 10 era raonable | Verificat passant el validate i comprovant que la sortida era l'esperada quan executàvem les consultes |
| 03/06 | Li he passat les respostes que tenia als apartats teòrics k/limit, numCandidates, similarity i pre-filter | M'ha respòs que tenia algun problema estructural i no podia respondre, "m'ha donat resposta el bot PROFE i per això és tal" sinó esperava que respongués el que hem après" | Senzillament hem comprovat el que ens comentava i entès millor cada apartat |

> Afegiu una fila per cada interacció substantiva amb PROFE. Si no hi ha
> interaccions, escriviu "Cap consulta a PROFE durant el desenvolupament".

## Resum honest

- **Parts del codi que cada membre del grup pot explicar línia a línia:**
  `_____`
- **Quelcom que hem fet servir però NO entenem del tot** (sigueu honestos):
  `_____`
- **Errors / suggeriments incorrectes de PROFE que hem rebutjat:**
  `_____`

## Declaració

Per la present, els membres del grup `17` declarem que:

- [x] **NO** hem usat cap IA diferent del bot PROFE per desenvolupar aquest projecte.
- [x] Tot el codi del repositori l'entenem i podem explicar-lo.
- [x] El registre anterior reflecteix totes les interaccions substantives amb PROFE.

**Signat (NIUs):** `1702609`, `1706571`
