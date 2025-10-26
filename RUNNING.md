Como rodar (prototype):
1. Copie .env.example para .env e configure GEMINI_API_KEY.
2. Instale dependências: pip install -r requirements.txt
3. Rodar index build (opcional para protótipo, alguns métodos são placeholders):
   python -m app.scripts.build_index
4. Start API:
   uvicorn main:app --reload
