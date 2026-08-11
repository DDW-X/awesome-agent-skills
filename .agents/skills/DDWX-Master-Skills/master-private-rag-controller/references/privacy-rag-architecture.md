# Privacy-First RAG Technical Reference & Architecture

## System Architecture

```
                      +-----------------------------+
                      |         User Query          |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |       AI Coding Agent       |
                      |      (Blind Controller)     |
                      +--------------+--------------+
                                     |
                         Invokes Query Tool Only
                                     |
                                     v
                      +-----------------------------+
                      |  src/core/rag/              |
                      |  query_private_index.py     |
                      +--------------+--------------+
                                     |
                             Sub-ms BM25 Search
                                     |
                                     v
                      +-----------------------------+
                      |  D-csR_Index/               |
                      |  private_rag.db (FTS5)      |
                      +--------------+--------------+
                                     |
                      +--------------+--------------+
                      |          Raw Data           |
                      |  (D-csR/ - Fully Isolated)  |
                      +-----------------------------+
```

## Security & Confidentiality Matrix

| Operation | Direct Agent Access | Tool-Mediated Access |
|---|---|---|
| Read Raw Source (`cat`, `view_file`) | ❌ STRICTLY FORBIDDEN | ❌ NOT PERFORMED |
| List Raw File Contents | ❌ STRICTLY FORBIDDEN | ❌ NOT PERFORMED |
| BM25 Token Matching | N/A | ✅ Isolated in SQLite FTS5 Engine |
| Context Extraction | ❌ NO RAW DUMPS | ✅ Top-k Chunks (Minimally Scoped) |
| Console Progress Telemetry | N/A | ✅ Silent Counter (No text leaks) |

## SQLite FTS5 Tokenizer & BM25 Scoring Mechanics

- **Tokenizer**: `unicode61 remove_diacritics 2` enables robust accent-insensitive, case-insensitive keyword matching across multilingual text.
- **BM25 Scoring**: Evaluates term frequency and inverse document frequency across chunks:
  $$\text{Score}(D, Q) = \sum_{i=1}^{N} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
- **Performance**: Capable of querying over 100,000 chunks in < 2ms without requiring heavy GPU or external vector database processes.
