import pandas as pd
import numpy as np
import string
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def carregar_modelo():
    # Carregue o DataFrame
    data = pd.read_csv('data.csv')

    # Transforme as classificações no DataFrame
    print(data.head())
    # Carregar ou treinar o modelo
    modelo_arquivo = 'modeloRedeNeural.h5'
    if os.path.exists(modelo_arquivo):
        model = tf.keras.models.load_model(modelo_arquivo)
    else:
        # Treine seu modelo aqui se necessário
        pass

    return model, data

def prever_nome(model, nome, max_posicoes=20):
    nome = nome.upper()
    alfabeto = string.ascii_uppercase
    input_vector = np.zeros(max_posicoes * len(alfabeto), dtype=int)

    for posicao, letra in enumerate(nome):
        if posicao < max_posicoes and letra in alfabeto:
            indice_letra = alfabeto.index(letra)
            indice_vetor = posicao * len(alfabeto) + indice_letra
            input_vector[indice_vetor] = 1

    previsao = model.predict(input_vector.reshape(1, -1))

    # Verifique se a previsão é uma probabilidade; converta para int se necessário
    classe_predita = (previsao > 0.5).astype(int).flatten()

    # Converte a classe prevista para a representação original ('M' ou 'F')
    classe_original = 'Masculino' if classe_predita[0] == 1 else 'Feminino'

    return classe_original

def buscar_nome(nome, data, modelo):
    retorno = {}

    if nome in data['nome'].values:
        valor = data.loc[data['nome'] == nome, [
            'nome', 'classificacao', 'frequencia_feminina',
            'frequencia_masculina', 'frequencia_total',
            'proporcao', 'porcentagem_feminina',
            'porcentagem_masculina'
        ]].copy()
        valor['classificacao'] = valor['classificacao'].map({0: 'Feminino', 1: 'Masculino'})

        dataFrame = {
            "nome": valor['nome'].iloc[0],
            "classificacao": valor['classificacao'].iloc[0],  # Acessa o primeiro elemento diretamente
            "frequencia_feminina": int(valor['frequencia_feminina'].iloc[0]),
            "frequencia_masculina": int(valor['frequencia_masculina'].iloc[0]),
            "frequencia_total": int(valor['frequencia_total'].iloc[0]),
            "proporcao": float(valor['proporcao'].iloc[0]),  # Converte para float se necessário
            "porcentagem_feminina": float(valor['porcentagem_feminina'].iloc[0]),
            "porcentagem_masculina": float(valor['porcentagem_masculina'].iloc[0])
        }
        retorno["DataFrame"] = dataFrame
    else:
        # Retorna um DataFrame vazio se o nome não for encontrado
        retorno["DataFrame"] = {
            "nome": nome,
            "classificacao": "Indefinido",
            "frequencia_feminina": 0,
            "frequencia_masculina": 0,
            "frequencia_total": 0,
            "proporcao": 0.0,
            "porcentagem_feminina": 0.0,
            "porcentagem_masculina": 0.0
        }

    resultado_modelo = prever_nome(modelo, nome)
    retorno["RedeNeural"] = resultado_modelo

    return retorno
