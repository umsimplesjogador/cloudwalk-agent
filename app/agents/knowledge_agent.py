# from app.rag.vectorstore import VectorStore
# from app.llm.gemini_client import ask_gemini
# from typing import Dict

# class KnowledgeAgent:
#     def __init__(self):
#         self.vs = VectorStore()

#     def _filter_hits(self, hits, query):
#         query_lower = query.lower()
#         filtered = []

#         for h in hits:
#             meta = h["meta"]
#             source = meta.get("source", "")
#             section = meta.get("section", "")

#             # Mantém apenas conteúdo Cloudwalk se for relevante
#             if "cloudwalk" in query_lower and "cloudwalk.io" not in source:
#                 continue

#             # Define peso por relevância da seção
#             weight = 1.0
#             if any(key in section.lower() for key in ["pillar", "mission", "about", "product", "ai"]):
#                 weight = 2.0

#             filtered.append({**h, "weight": weight})

#         # Ordena pelo peso
#         filtered = sorted(filtered, key=lambda x: x["weight"], reverse=True)

#         # 🔹 AGRUPAR POR SEÇÃO
#         grouped = {}
#         for h in filtered:
#             sec = h["meta"].get("section", "general")
#             if sec not in grouped:
#                 grouped[sec] = []
#             grouped[sec].append(h)

#         # Se a query for sobre pilares, missão ou valores, devolve **todos os blocos da seção relevante**
#         if any(k in query_lower for k in ["pillar", "mission", "value"]):
#             relevant_sections = [sec for sec in grouped if any(k in sec.lower() for k in ["pillar", "mission", "value"])]
#             hits_final = []
#             for sec in relevant_sections:
#                 hits_final.extend(grouped[sec])
#             return hits_final

#         # Caso geral, pega top 6 hits
#         return filtered[:6]

#     def _format_context(self, hits):
#         """
#         Concatena todos os blocos mantendo a ordem original.
#         """
#         s = ""
#         for h in hits:
#             meta = h["meta"]
#             s += f"[Seção: {meta.get('section')}] {h['text']} (Fonte: {meta.get('source')})\n\n"
#         return s
    

#     def answer(self, query: str) -> Dict:
#         # Recupera os trechos mais relevantes via FAISS
#         hits = self.vs.query(query, top_k=10)
#         hits = self._filter_hits(hits, query)
#         context = self._format_context(hits)

#         prompt = f"""Contexto sobre a Cloudwalk extraído de várias seções do site:
# {context}

# Pergunta do usuário:
# {query}

# Instruções:
# - Baseie sua resposta **exclusivamente** no contexto acima.
# - Se o contexto contiver uma seção específica (ex: pillars, mission, products), use-a como fonte principal.
# - Responda em Português, mas preserve nomes próprios e termos originais em inglês (ex: Best Product).
# - Não invente informações que não estejam no contexto.
# - Se a informação não estiver disponível, diga claramente que não está no contexto e indique a seção onde procurar.
# """

#         system_instruction = (
#             "Você é um assistente especializado em informações institucionais da Cloudwalk, "
#             "incluindo missão, pilares e produtos. Responda de forma fiel ao site oficial."
#         )

#         text = ask_gemini(prompt, system=system_instruction)
#         text = text.replace("\\n", "\n").strip()
#         sources = list({h['meta']['source'] for h in hits})

#         return {"answer": text, "sources": sources}
    









# from app.rag.vectorstore import VectorStore
# from typing import Dict

# class KnowledgeAgent:
#     def __init__(self):
#         self.vs = VectorStore()

#     def _filter_hits(self, hits, query):
#         """
#         Filtra e ordena os blocos por relevância.
#         Para queries sobre pilares, missão ou valores, retorna **todos os blocos da seção**.
#         """
#         query_lower = query.lower()
#         filtered = []

#         for h in hits:
#             meta = h["meta"]
#             source = meta.get("source", "")
#             section = meta.get("section", "")

#             # Mantém apenas conteúdo Cloudwalk se for relevante
#             if "cloudwalk" in query_lower and "cloudwalk.io" not in source:
#                 continue

#             # Define peso por relevância da seção
#             weight = 1.0
#             if any(key in section.lower() for key in ["pillar", "mission", "about", "product", "ai"]):
#                 weight = 2.0

#             filtered.append({**h, "weight": weight})

#         # Ordena pelo peso
#         filtered = sorted(filtered, key=lambda x: x["weight"], reverse=True)

#         # Agrupa por seção
#         grouped = {}
#         for h in filtered:
#             sec = h["meta"].get("section", "general")
#             if sec not in grouped:
#                 grouped[sec] = []
#             grouped[sec].append(h)

#         # Para queries sobre pilares, missão ou valores, devolve **todos os blocos da seção relevante**
#         if any(k in query_lower for k in ["pillar", "pillars", "mission", "value", "values"]):
#             relevant_sections = [sec for sec in grouped if "pillar" in sec.lower()]
#             hits_final = []
#             for sec in relevant_sections:
#                 hits_final.extend(grouped[sec])
#             return hits_final

#         # Caso geral, retorna top 6
#         return filtered[:6]

#     def _format_context(self, hits):
#         """
#         Concatena todos os blocos mantendo a ordem original.
#         """
#         s = ""
#         for h in hits:
#             meta = h["meta"]
#             s += f"[Seção: {meta.get('section')}] {h['text']} (Fonte: {meta.get('source')})\n\n"
#         return s

#     def answer(self, query: str) -> Dict:
#         # Recupera blocos do FAISS
#         hits = self.vs.query_for_hits(query, top_k=50)
#         hits = self._filter_hits(hits, query)

#         # Garante que há conteúdo
#         if not hits:
#             return {"answer": "Os pilares da Cloudwalk não estão no contexto fornecido. Consulte a seção 'Pillars' no site oficial.", "sources": []}

#         # Monta prompt e chama Gemini
#         context = self._format_context(hits)
#         system_instruction = (
#             "Você é um assistente especializado em informações institucionais da Cloudwalk, "
#             "incluindo missão, pilares e produtos. Responda de forma fiel ao site oficial."
#         )

#         answer = self.vs.query_with_gemini(query, hits)
#         sources = list({h['meta'].get("source", "desconhecida") for h in hits})

#         return {"answer": answer, "sources": sources}





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
