<template>
  <div class="min-h-screen bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
      <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">Classificador de Nomes</h1>

      <form @submit.prevent="classifyName" class="mb-6">
        <div class="relative">
          <input
            v-model="name"
            type="text"
            maxlength="20"
            placeholder="Digite um nome"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            :class="{ 'border-red-500': error }"
            aria-label="Nome para classificação"
          />
          <button
            type="submit"
            class="absolute right-2 top-2 bg-purple-500 text-white rounded-md px-4 py-1 hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-400 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!name || isLoading"
            aria-label="Classificar nome"
          >
            <LoaderIcon v-if="isLoading" class="animate-spin h-5 w-5" aria-hidden="true" />
            <span v-else>Classificar</span>
          </button>
        </div>
        <p v-if="error" class="mt-2 text-red-500 text-sm" role="alert">{{ error }}</p>
      </form>

      <div v-if="result" class="bg-gray-100 rounded-lg p-6">
        <h2 class="text-2xl font-semibold mb-4 text-center" :class="resultColor">
          Rede Neural: {{ result.RedeNeural }}
        </h2>
        <div v-if="result.DataFrame.classificacao !== 'Indefinido'" class="space-y-2">
          <p><strong>Nome:</strong> {{ result.DataFrame.nome }}</p>
          <p><strong>Classificação DataFrame:</strong> {{ result.DataFrame.classificacao }}</p>
          <p><strong>Frequência Total:</strong> {{ formatNumber(result.DataFrame.frequencia_total) }}</p>
          <div class="flex justify-between">
            <p><strong>Feminino:</strong> {{ formatPercentage(result.DataFrame.porcentagem_feminina) }}</p>
            <p><strong>Masculino:</strong> {{ formatPercentage(result.DataFrame.porcentagem_masculina) }}</p>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div 
              class="bg-blue-600 h-2.5 rounded-full" 
              :style="{ width: `${result.DataFrame.porcentagem_masculina * 100}%` }"
              role="progressbar"
              :aria-valuenow="result.DataFrame.porcentagem_masculina * 100"
              aria-valuemin="0"
              aria-valuemax="100"
            ></div>
          </div>
        </div>
        <p v-else class="text-center text-gray-600 mt-4">
          Dados insuficientes para classificação no DataFrame.
        </p>
      </div>

      <p class="mt-8 text-sm text-gray-600 text-center">
        ESSE PROJETO É SOMENTE PARA FINS DIDÁTICOS. O AUTOR DOS ESTUDOS NÃO PROMOVE QUALQUER ATO DE DISCRIMINAÇÃO DE PESSOAS TRANS.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { LoaderIcon } from 'lucide-vue-next'

const name = ref('')
const result = ref(null)
const error = ref('')
const isLoading = ref(false)

const classifyName = async () => {
  if (name.value.length > 20) {
    error.value = 'O nome deve ter no máximo 20 caracteres.'
    return
  }

  error.value = ''
  isLoading.value = true

  try {
    const response = await axios.get(`https://projeto.augustosouza.tech/api/prever?nome=${encodeURIComponent(name.value)}`)
    result.value = response.data
  } catch (err) {
    error.value = 'Ocorreu um erro ao classificar o nome. Por favor, tente novamente.'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

const resultColor = computed(() => {
  return result.value?.RedeNeural === 'Masculino' ? 'text-blue-600' : 'text-pink-600'
})

const formatNumber = (num) => {
  return new Intl.NumberFormat('pt-BR').format(num)
}

const formatPercentage = (num) => {
  return (num * 100).toFixed(2) + '%'
}
</script>
