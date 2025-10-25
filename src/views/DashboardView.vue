<script setup>
import { ref, onMounted } from 'vue';
// Confirma que está a importar o apiClient configurado
import apiClient from '../api';

// Variáveis reativas (Refs) para guardar os dados e o estado
const objetivos = ref([]); // Lista de objetivos vinda da API
const isLoading = ref(true); // Controla se está a carregar
const error = ref(null); // Guarda mensagens de erro

// Função assíncrona para buscar os objetivos da API
const fetchObjetivos = async () => {
  try {
    isLoading.value = true; // Inicia o estado de carregamento
    // Faz a chamada GET para o endpoint de OKRs usando o apiClient
    const response = await apiClient.get('/api/okr/objetivos/'); //
    objetivos.value = response.data; // Armazena os dados recebidos
    error.value = null; // Limpa qualquer erro anterior
  } catch (err) {
    console.error("Erro ao buscar objetivos:", err);
    error.value = "Falha ao carregar objetivos."; // Define a mensagem de erro
    // Poderia adicionar tratamento mais específico para err.response.status se necessário
  } finally {
    isLoading.value = false; // Finaliza o estado de carregamento (sucesso ou erro)
  }
};

// Hook 'onMounted': chama a função fetchObjetivos assim que o componente é montado (exibido na tela)
onMounted(() => {
  fetchObjetivos();
});
</script>

<template>
  <div class="dashboard-container">
    <h1>Dashboard Principal</h1>
    <p>Bem-vindo ao sistema Reúne!</p>

    <hr class="divider">

    <h2>Meus OKRs</h2>

    <div v-if="isLoading" class="loading-state">
      <p>A carregar objetivos...</p>
      </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchObjetivos">Tentar Novamente</button>
    </div>

    <div v-else-if="objetivos.length > 0" class="objetivos-grid">
      <div v-for="obj in objetivos" :key="obj.id" class="objetivo-card">
        <h3>{{ obj.titulo }}</h3>
        <p class="responsavel">
          Responsável: {{ obj.responsavel.first_name || obj.responsavel.username || 'N/A' }}
        </p>
         <p class="progresso-geral">Progresso Geral: {{ obj.progresso }}%</p>
        <p class="descricao">{{ obj.descricao }}</p>
        </div>
    </div>

    <p v-else class="empty-state">
      Você ainda não tem objetivos cadastrados.
    </p>
  </div>
</template>

<style scoped>
.dashboard-container {
  max-width: 1200px; /* Largura máxima para o conteúdo */
  margin: 0 auto; /* Centraliza o container */
  padding: 1rem; /* Padding base */
}

h1 {
    text-align: center;
    margin-bottom: 0.5rem;
}
p {
    text-align: center;
    color: #666;
    margin-bottom: 1.5rem;
}
h2 {
    text-align: center;
    margin-bottom: 2rem;
    color: #333;
}

.divider {
  border: 0;
  border-top: 1px solid #eee;
  margin: 2rem 0;
}

/* Grid para os cards de objetivos */
.objetivos-grid {
  display: grid;
  /* Cria colunas responsivas: tenta encaixar o máximo de colunas com 300px,
     mas cada uma pode crescer até ocupar 1fr (fração do espaço) */
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem; /* Espaço entre os cards */
}

.objetivo-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; /* Efeito suave no hover */
}

.objetivo-card:hover {
    transform: translateY(-3px); /* Leve elevação no hover */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12); /* Sombra mais pronunciada no hover */
}

.objetivo-card h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #0056b3; /* Azul escuro para o título */
}

.responsavel {
  font-size: 0.9em;
  font-style: italic;
  color: #555;
  margin-bottom: 0.8rem;
  text-align: left; /* Alinha texto do responsável */
}

.progresso-geral {
    font-weight: bold;
    color: #1a73e8; /* Azul mais vibrante para progresso */
    margin-bottom: 0.8rem;
    text-align: left;
}

.descricao {
  font-size: 0.95em;
  color: #444;
  line-height: 1.5;
  margin-bottom: 0; /* Remove margem inferior da descrição */
   text-align: left;
}

/* Estilos para estados de carregamento, erro e vazio */
.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 3rem 1rem;
  margin-top: 2rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #6c757d; /* Cinza */
}
.error-state {
  background-color: #f8d7da; /* Fundo vermelho claro */
  color: #721c24; /* Vermelho escuro */
  border: 1px solid #f5c6cb;
}
.error-state button {
  margin-top: 1rem;
  padding: 8px 15px;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #721c24;
  background-color: transparent;
  color: #721c24;
  transition: background-color 0.2s, color 0.2s;
}
.error-state button:hover {
    background-color: #721c24;
    color: white;
}

/* --- Media Queries para Responsividade --- */

/* Ajusta o padding em ecrãs menores */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  .objetivos-grid {
    gap: 1rem; /* Reduz o espaço entre cards */
  }
  .objetivo-card {
    padding: 1rem; /* Reduz padding interno dos cards */
  }
}

/* Em ecrãs muito pequenos, garante que o grid tenha apenas uma coluna */
@media (max-width: 480px) {
    .objetivos-grid {
        /* A configuração 'auto-fit' com minmax já deve garantir uma coluna,
           mas podemos forçar se necessário */
        /* grid-template-columns: 1fr; */
    }
     h1 { font-size: 1.8em; }
     h2 { font-size: 1.3em; }
}

</style>