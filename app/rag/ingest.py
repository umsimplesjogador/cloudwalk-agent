import os
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class RAGIngest:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ";"]
        )

    def scrape_page(self, url):
        print(f"🌐 Coletando {url}")
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            # remove scripts, styles e navegação
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.extract()
            text = soup.get_text(separator="\n", strip=True)
            return text
        except Exception as e:
            print(f"❌ Erro ao coletar {url}: {e}")
            return ""

    def build_index(self):
        urls = [
            "https://www.cloudwalk.io/",
            "https://www.cloudwalk.io/#our-pillars",
            "https://www.cloudwalk.io/#mission",
            "https://www.cloudwalk.io/#our-products",
            "https://www.cloudwalk.io/#about",
            "https://www.cloudwalk.io/#ai",
            "https://www.infinitepay.io/",
            "https://www.jim.com/",
            "https://www.cloudwalk.io/stratus"
        ]

        all_chunks = []
        for url in urls:
            content = self.scrape_page(url)
            if content:
                chunks = self.text_splitter.split_text(content)
                section = "our-pillars" if "pillars" in url else \
                          "mission" if "mission" in url else \
                          "about" if "about" in url else \
                          "ai" if "ai" in url else "general"
                for c in chunks:
                    all_chunks.append({
                        "text": c,
                        "meta": {"source": url, "section": section}
                    })
                print(f"✅ Extraído {len(content)} caracteres e dividido em {len(chunks)} blocos de {url}")

        if not all_chunks:
            print("❌ Nenhum conteúdo coletado!")
            return

        # Salva o texto completo
        txt_path = os.path.join(DATA_DIR, "cloudwalk_content.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            for c in all_chunks:
                f.write(c["text"] + "\n")
        print(f"💾 Conteúdo salvo em {txt_path}")

        # Construindo FAISS
        print("🧠 Gerando embeddings e construindo FAISS...")
        texts = [c["text"] for c in all_chunks]
        metadatas = [c["meta"] for c in all_chunks]
        vectorstore = FAISS.from_texts(texts, embedding=self.embeddings, metadatas=metadatas)
        vectorstore.save_local(os.path.join(DATA_DIR, "faiss_index"))
        print("📦 Índice FAISS salvo em data/faiss_index")


if __name__ == "__main__":
    RAGIngest().build_index()
