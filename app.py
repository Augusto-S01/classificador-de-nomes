from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from modelo import carregar_modelo, buscar_nome
import numpy as np

# Inicializa a aplicação FastAPI
app = FastAPI()

# Adiciona o middleware CORS
origins = [
    "http://localhost:3000",  # Substitua pelo domínio do seu frontend
    "http://127.0.0.1:3000",  # Substitua pelo domínio do seu frontend
    "http://projeto.augustosouza.tech",  # Adicione seu domínio real
    "*",  # Para permitir todos os domínios (não recomendado em produção)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir as origens especificadas
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Carrega o modelo e o DataFrame
modelo, data = carregar_modelo()
print("Servidor iniciando")

# Definindo um modelo Pydantic para a resposta
class Resultado(BaseModel):
    DataFrame: dict
    RedeNeural: str

@app.get("/api/prever", response_model=Resultado)
def prever(nome: str):
    if not nome:
        raise HTTPException(status_code=400, detail="Nome não fornecido")

    try:
        resultado = buscar_nome(nome.upper(), data, modelo)

        # Verifique se o resultado é válido antes de enviar
        if not resultado:
            raise HTTPException(status_code=500, detail="Erro no processamento")

        return resultado
    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@app.get("/test")
def test():
    return {"message": "Servidor FastAPI está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)
