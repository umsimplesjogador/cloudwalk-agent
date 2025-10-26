# import os
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate
# from app.llm.gemini_client import ask_gemini

# DATA_DIR = "data"
# MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# class VectorStore:
#     def __init__(self):
#         self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
#         self.index_path = os.path.join(DATA_DIR, "faiss_index")

#         # Reconstrói índice se não existir
#         if not os.path.exists(self.index_path):
#             from app.rag.ingest import RAGIngest
#             print("⚙️ Índice FAISS não encontrado. Construindo com RAGIngest...")
#             RAGIngest().build_index()

#         print("📂 Carregando índice FAISS existente...")
#         self.vectorstore = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)

#         # Prompt
#         template = (
#             "Você é um assistente especializado em responder perguntas sobre a empresa Cloudwalk e o site InfinitePay.\n"
#             "Baseie suas respostas exclusivamente no contexto fornecido abaixo.\n"
#             "Se a pergunta for sobre missão, pilares, visão ou valores, responda **todos os itens completos com suas descrições**, exatamente como estão no contexto.\n"
#             "Responda em português, mantendo nomes e termos originais em inglês.\n\n"
#             "Contexto:\n{context}\n\n"
#             "Pergunta: {question}\n\n"
#             "Resposta:"
#         )
#         self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])

#     def query(self, question: str, top_k: int = 10):
#         try:
#             # Recupera os documentos mais relevantes do FAISS
#             docs = self.vectorstore.similarity_search(question, k=top_k)
#             context = "\n\n".join([f"[Seção: {d.metadata.get('section', 'desconhecida')}] {d.page_content}" for d in docs])

#             # Monta prompt para o Gemini
#             prompt_text = self.prompt.format(context=context, question=question)

#             # Chama Gemini LLM
#             answer = ask_gemini(prompt_text)

#             # Retorna no formato esperado pelo KnowledgeAgent
#             return [{"text": answer, "meta": {"source": ", ".join({d.metadata.get('source', 'desconhecida') for d in docs})}}]

#         except Exception as e:
#             print("Erro ao consultar o modelo:", e)
#             return [{"text": "Erro ao processar a pergunta.", "meta": {}}]











# import os
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate
# from app.llm.gemini_client import ask_gemini

# DATA_DIR = "data"
# MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# class VectorStore:
#     def __init__(self):
#         self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
#         self.index_path = os.path.join(DATA_DIR, "faiss_index")

#         # Reconstrói índice se não existir
#         if not os.path.exists(self.index_path):
#             from app.rag.ingest import RAGIngest
#             print("⚙️ Índice FAISS não encontrado. Construindo com RAGIngest...")
#             RAGIngest().build_index()

#         print("📂 Carregando índice FAISS existente...")
#         self.vectorstore = FAISS.load_local(
#             self.index_path, self.embeddings, allow_dangerous_deserialization=True
#         )

#         # Prompt template
#         template = (
#             "Você é um assistente especializado em responder perguntas sobre a Cloudwalk e InfinitePay.\n"
#             "Use **exclusivamente** o contexto fornecido abaixo.\n"
#             "Se a pergunta for sobre missão, pilares ou valores, inclua **todos os itens completos com suas descrições**, exatamente como no contexto.\n"
#             "Responda em português, mantendo nomes e termos originais em inglês.\n\n"
#             "Contexto:\n{context}\n\n"
#             "Pergunta: {question}\n\n"
#             "Resposta:"
#         )
#         self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])

#     def query_for_hits(self, question: str, top_k: int = 50):
#         """
#         Retorna todos os blocos relevantes do FAISS sem chamar Gemini.
#         Cada bloco é um dict com 'text' e 'meta'.
#         """
#         try:
#             docs = self.vectorstore.similarity_search(question, k=top_k)
#             hits = []
#             for d in docs:
#                 hits.append({
#                     "text": getattr(d, "page_content", str(d)),
#                     "meta": getattr(d, "metadata", {})
#                 })
#             return hits
#         except Exception as e:
#             print("Erro ao buscar hits:", e)
#             return []

#     def query_with_gemini(self, question: str, hits):
#         """
#         Recebe blocos já filtrados, concatena e envia para Gemini.
#         """
#         context = "\n\n".join([f"[Seção: {h['meta'].get('section','desconhecida')}] {h['text']}" for h in hits])
#         prompt_text = self.prompt.format(context=context, question=question)
#         answer = ask_gemini(prompt_text)
#         return answer











import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from app.llm.gemini_client import ask_gemini

DATA_DIR = "data"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        self.index_path = os.path.join(DATA_DIR, "faiss_index")

        # Reconstrói índice se não existir
        if not os.path.exists(self.index_path):
            from app.rag.ingest import RAGIngest
            print("⚙️ Índice FAISS não encontrado. Construindo com RAGIngest...")
            RAGIngest().build_index()

        print("📂 Carregando índice FAISS existente...")
        self.vectorstore = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)

        # Prompt reforçado para garantir todos os pilares
        template = (
            "Você é um assistente especializado em responder perguntas sobre a empresa Cloudwalk e o site InfinitePay.\n"
            "Baseie suas respostas **exclusivamente** no contexto fornecido abaixo.\n"
            "⚠️ Somente mencione os pilares (Best Product, Customer Engagement, Disruptive Economics) se a pergunta for **explicitamente sobre pilares, valores ou visão**.\n"
            "Se a pergunta **não mencionar** esses temas, **não inclua os pilares** em hipótese alguma.\n"
            "Se a pergunta for sobre filosofia ou religião, responda **exclusivamente** com FIAT LUX e sua descrição.\n"
            "Se a pergunta for sobre missão, utilize **todo o conteúdo textual** encontrado no link https://www.cloudwalk.io/#our-mission, incluindo a explicação completa sobre a democratização da indústria financeira, a importância do preço e o objetivo de construir um novo sistema justo para todos.\n"
            "Mantenha o texto em português natural e fluido, traduzindo integralmente o conteúdo original em inglês.\n"
            "Quando citar os pilares, mantenha os nomes em inglês, mas **traduza as descrições para o português**, preservando o sentido original.\n"
            "Responda de forma organizada, com formatação em tópicos e linguagem natural.\n\n"
            "Contexto:\n{context}\n\n"
            "Pergunta: {question}\n\n"
            "Resposta:"
        )
        
        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    def query(self, question: str, top_k: int = 10):
        try:
            # Recupera os documentos mais relevantes
            docs = self.vectorstore.similarity_search(question, k=top_k)

            # Garante que se a pergunta for sobre pilares, tragam TODOS da seção "our-pillars"
            if "pillar" in question.lower() or "pilares" in question.lower():
                all_docs = self.vectorstore.similarity_search("pillars", k=50)
                docs = [d for d in all_docs if "pillar" in d.metadata.get("section", "").lower()]

            # Monta o contexto completo (sem cortar)
            context_blocks = []
            for d in docs:
                section = d.metadata.get("section", "desconhecida")
                text = d.page_content
                context_blocks.append(f"[Seção: {section}] {text}")

            context = "\n\n".join(context_blocks)

            # Monta e envia prompt ao Gemini
            prompt_text = self.prompt.format(context=context, question=question)
            answer = ask_gemini(prompt_text)

            sources = list({d.metadata.get("source", "desconhecida") for d in docs})

            return {"hits": [{"text": d.page_content, "meta": d.metadata} for d in docs],
                    "answer": answer,
                    "sources": sources}

        except Exception as e:
            print("❌ Erro ao consultar o modelo:", e)
            return {"hits": [], "answer": "Erro ao processar a pergunta.", "sources": []}
