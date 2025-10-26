from app.rag.vectorstore import VectorStore
from typing import Dict

class KnowledgeAgent:
    def __init__(self):
        self.vs = VectorStore()

    def _filter_hits(self, hits, query):
        """
        Mantém hits relevantes por seção e prioridade sem eliminar blocos úteis.
        """
        query_lower = query.lower()
        filtered = []

        for h in hits:
            meta = h["meta"]
            section = meta.get("section", "")
            source = meta.get("source", "")

            weight = 1.0
            if any(k in section.lower() for k in ["pillar", "pillars", "mission", "missions", "about", "product", "products", "ai"]):
                weight = 2.0

            filtered.append({**h, "weight": weight})

        filtered = sorted(filtered, key=lambda x: x["weight"], reverse=True)

        # Se a pergunta for sobre pilares, manter **todos os blocos da seção**
        if any(k in query_lower for k in ["pillar", "pilares"]):
            return [h for h in filtered if "pillar" in h["meta"].get("section", "").lower()]

        return filtered[:6]

    def _format_context(self, hits):
        """
        Concatena todos os blocos mantendo estrutura.
        """
        s = ""
        for h in hits:
            meta = h["meta"]
            s += f"[Seção: {meta.get('section')}] {h['text']} (Fonte: {meta.get('source')})\n\n"
        return s

    def answer(self, query: str) -> Dict:
        res = self.vs.query(query, top_k=10)
        hits = res["hits"]

        # Filtra e prepara o contexto
        hits = self._filter_hits(hits, query)
        context = self._format_context(hits)

        # Usa a resposta já gerada no VectorStore, se disponível
        text = res["answer"].replace("\\n", "\n").strip()
        sources = list({h['meta']['source'] for h in hits})

        return {"answer": text, "sources": sources}
