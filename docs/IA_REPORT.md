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
|03/06| que falla del C2 en N3? + codi   | M'ha comentat on estava la principal problemàtica que impedia que pogués passar els testos, en aquest cas que max_turns no tenia assignat cap valor per defecte. |Ho hem verificat tornant a executar les consultes i seguidament passant el validate tampoc ha funcionat. Hi havia algun altre error.   |
| 03/06 | (en referència a l'anterior) 5 estaria bien? | M'ha comentat que un valor entre 3 i 10 era raonable | Verificat passant el validate i comprovant que la sortida era l'esperada quan executàvem les consultes |
| 03/06 | Li he passat les respostes que tenia als apartats teòrics k/limit, numCandidates, similarity i pre-filter | M'ha respòs que tenia algun problema estructural i no podia respondre, "m'ha donat resposta el bot PROFE i per això és tal" sinó esperava que respongués el que hem après" | Senzillament hem comprovat el que ens comentava i entès millor cada apartat |
| 04/06 | que falla del c2 del n3 que tenemos 0/2 + codi | M'ha respòs que el problema era el que retornàvem al rag_agent que no concordava exactament amb el que l'enunciat esperava i el validador per tant, també |  El fet de no respondre'ns exactament com fer-ho i orientar-nos només ha fet que haguéssim de tornar a l'enunciat i observar i pensar què fallava  |
| 04/06 | per què la part c2 de la part n3 de la pràctica ens avalua 0/2? | Ens ha respost que hi havia un rang de valors de confiança que no contemplàvem que feia que en algun cas el validador no rebés res | Hem explorat opcions i mirat possibles solucions |
| 04/06 (seguit anterior) | què passa si elimino la condició? | M'ha donat una resposta molt oberta, "massa" pel meu gust XD. M'ha dit que què passava si tots els resultats tenien socre entre 0.60 i 0.74. En tot cas m'ha fer reflexionar" | Hem provat de treure-la i no ens ha funcionat llavors hem canviat el codi en aquella part afegint uns condicionals amb el que generava conflicte |
| 04/06 | llavors com hauria de ser per passar c2 i els altres? | M'ha dit que el gran problema era que mai arribava el prompt defensiu per culpa d'una línia results [:3] | Senzillament hem tret la línia i hem modificat el que li enviàvem perquè detectés prompt defensiu enfortint-lo i fent una llista de rules jugant amb les majúscules també |
| 04/06 | tinc 9,5/15, què esta fallant? + defensa| M'ha comentat els principals erros que hi havien als apartats Q2, Q4 i Q5. | M'han fet canviar algunes respostes que gràcies a la resposta del BOT he pogut comprendre molt millor | 







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
