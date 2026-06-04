# DECISIONS — `17`

Documenteu cada decisió no-òbvia amb el seu trade-off. **Avaluat al Canal C de
la rúbrica (15%)**. Cal almenys 5 decisions amb trade-off explícit per a la
nota completa. Sigueu breus; un bullet per decisió, sempre amb un **per què**.

## Retrieval
- **k / limit** = `5`. Why: `We use a small value of k to return the top 5 most similar results, which provides a good balance between precision and simplicity in the retrieved context. This is also a common default in retrieval systems for initial experiments.`
- **numCandidates** = `10*limit (5 in this case) = 50`. Why (recall vs latency): `HNSW performs an approximate nearest-neighbor search, meaning that it does not compare the query vector against all vectors in the collection. Instead, it explores a subset of promising candidates and then selects the best results among them. For this reason, numCandidates must be larger than limit: if we only examined 5 candidates to return 5 results, we could easily miss more relevant documents. Increasing numCandidates improves recall because the algorithm explores a larger portion of the search graph and has a higher chance of finding the true nearest neighbors. However, evaluating more candidates also increases query latency. The rule of thumb numCandidates ≥ 10 × limit provides a good balance between retrieval quality and performance, which is why we use 50 candidates when limit = 5.`
- **similarity** = `cosine`. Why: `Per a vectors normalitzats, cosine i dotProduct donen el mateix resultat matemàticament, però la convenció del curs (i la que millor funciona quan no pots garantir normalització al 100%) és cosine. Euclidean no és adequada perquè mesura distància geomètrica absoluta, no angle/orientació semàntica. Amb embeddings de text, dues frases sinònimes podrien tenir magnituds molt diferents i euclidean les penalitzaria injustament.`
- **pre-filter** used? on which field (`year`?): `YES, on the 'year' field.`. Why pre- and not post-filter: `N1 only performs semantic similarity search and does not include any metadata constraints, so a pre-filter is unnecessary. A pre-filter would be useful if the query contained restrictions on fields such as year or genre, since it would limit the search space before the vector search and improve efficiency and relevance. As no such constraints exist in N1, no pre-filter is applied.`

## Embeddings
- **EMBED_MODEL** = `text-embedding-ada-002`. Why this exact model (not just 1536-d): `Because it is what they ask at the statement of the exercice. Also it's compatible wit plot_embedding of embedded_movies.`

## RAG (N2+)
- **Chunking**: N/A (we use the precomputed plot embedding) / or describe: `The system does not perform runtime chunking because each movie is stored as a single document with a precomputed embedding of the full plot (plot_embedding). Therefore, retrieval operates directly over complete movie plots without splitting them into smaller segments.`
- **Defensive prompt**: what instruction prevents hallucination: `You are a retrieval-augmented assistant.

    RULES:
    1. Use ONLY the provided context.
    2. The context is the ONLY source of truth.
    3. NEVER use external knowledge.
    4. Never infer or assume facts that are not explicitly stated.
    5. If the answer is not fully supported by the context, respond exactly:
    "I don't know."
    6. DO NOT partially answer.
    7. Always cite the movie titles used in your answer.
    8. If the movie of the context IS NOT relacionated with the question DO NOT take it into account.`
- **CHAT_MODEL** = `gpt-4o`. Why: `Usamos el modelo GPT-4o porque es un modelo muy capaz de seguir estrictamente las instrucciones del sistema y esquemas JSON.  Esto asegura que se respeten las restricciones de nuestro prompt defensivo, eliminando eficazmente las alucinaciones cuando el contexto es insuficiente.`

## Agent / Multi-agent (N3/N4)
- **Tools defined**: `filter_by_year and search_movies`
- **Architecture pattern** (chaining / routing / evaluator-optimizer / parallel): `routing + chaining`. Why: `The agent first routes the query to the appropriate tool depending on whether there are temporal constraints (filter_by_year) or not (search_movies). After tool selection, it follows a chaining process where the model iteratively calls tools, collects intermediate results, and then performs a final synthesis step using the retrieved context to generate the response.`
- **Retry / stop condition** (N4): `El orquestador vuelve al nodo de reintento retry si state["evaluation"]["sufficient"] se evalúa como False durante la etapa del Critic. Para garantizar una finalización determinante y evitar bucles infinitos costosos en producción (como cuando una consulta busca datos completamente inexistentes), el flujo fuerza una salida hacia el nodo synthesize como un interruptor de seguridad (circuit breaker) inmediatamente después de alcanzar un límite máximo de 1 reintento (state["retry_count"] >= 1).`

## Alternatives considered and rejected
- `_____` rejected because `_____`
