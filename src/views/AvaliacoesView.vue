<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../api';

// Estados
const ciclos = ref([]);
const competencias = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Função para buscar dados
const fetchData = async () => {
  try {
    isLoading.value = true;
    error.value = null; // Limpa erro anterior
    const [ciclosRes, compRes] = await Promise.all([
      apiClient.get('/api/avaliacoes/ciclos/'), //
      apiClient.get('/api/avaliacoes/competencias/') //
    ]);
    
    ciclos.value = ciclosRes.data;
    competencias.value = compRes.data;
  } catch (err) {
    console.error("Erro ao buscar dados de avaliações:", err);
    error.value = "Falha ao carregar dados. Verifique a ligação à API.";
  } finally {
    isLoading.value = false;
  }
};

// Busca dados ao montar
onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="page-container">
    <h1>Avaliações de Desempenho</h1>

    <div v-if="isLoading" class="loading-state">
        <p>A carregar dados...</p>
    </div>
    <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchData">Tentar Novamente</button>
    </div>

    <div v-else class="content-wrapper">
      
      <div class="list-card">
        <h2>Ciclos de Avaliação</h2>
        <ul v-if="ciclos.length > 0" class="ciclo-lista">
          <li v-for="ciclo in ciclos" :key="ciclo.id">
            <div class="ciclo-info">
              <strong>{{ ciclo.titulo }}</strong>
              <span :class="['status-badge', ciclo.status.toLowerCase()]">{{ ciclo.status }}</span>
              <br>
              <small>{{ new Date(ciclo.data_inicio).toLocaleDateString() }} - {{ new Date(ciclo.data_fim).toLocaleDateString() }}</small>
            </div>
            <router-link
              v-if="ciclo.status === 'Ativo'"
              :to="{ name: 'RealizarAvaliacao', params: { cicloId: ciclo.id } }"
              class="avaliar-button"
            >
              Avaliar Colega
            </router-link>
          </li>
        </ul>
        <p v-else class="empty-list-message">Nenhum ciclo de avaliação cadastrado.</p>
      </div>

      <div class="list-card">
        <h2>Competências da Empresa</h2>
        <ul v-if="competencias.length > 0" class="competencia-lista">
          <li v-for="comp in competencias" :key="comp.id">
             <strong>{{ comp.nome }}</strong>
            <p class="competencia-descricao"><small>{{ comp.descricao }}</small></p>
          </li>
        </ul>
        <p v-else class="empty-list-message">Nenhuma competência cadastrada.</p>
      </div>
    </div>
    
  </div>
</template>

<style scoped>
.page-container {
  max-width: 1100px; /* Um pouco mais largo para as colunas */
  margin: 0 auto;
  padding: 1.5rem;
}

h1 { text-align: center; margin-bottom: 2rem; }

/* Layout Grid para os cards */
.content-wrapper { 
  display: grid;
  /* Cria colunas responsivas, mínimo 320px */
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
  gap: 2rem; 
}

/* Estilo Base dos Cards */
.list-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
.list-card h2 {
  margin-top: 0;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.8rem;
  margin-bottom: 1rem;
  font-size: 1.3em;
  color: #333;
}

/* Listas dentro dos cards */
ul { list-style: none; padding: 0; margin: 0; }
li {
  display: flex; /* Alinha info e botão */
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px dashed #eee;
  gap: 1rem; /* Espaço entre info e botão */
}
li:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }

/* Informações do Ciclo */
.ciclo-info strong { display: block; margin-bottom: 4px; color: #0056b3; }
.ciclo-info small { color: #555; font-size: 0.9em; }

/* Badge de Status (Ativo, Planejamento, Concluído) */
.status-badge {
    font-size: 0.8em;
    padding: 3px 8px;
    border-radius: 12px; /* Formato de pílula */
    margin-left: 8px;
    font-weight: 500;
    color: #fff;
    white-space: nowrap;
}
.status-badge.ativo { background-color: #28a745; } /* Verde */
.status-badge.planejamento { background-color: #ffc107; color: #333;} /* Amarelo */
.status-badge.concluído { background-color: #6c757d; } /* Cinza */

/* Informações da Competência */
.competencia-lista li { flex-direction: column; align-items: flex-start; } /* Força vertical */
.competencia-lista strong { color: #333; }
.competencia-descricao { margin: 5px 0 0 0; font-size: 0.9em; color: #555; line-height: 1.5; }

/* Botão Avaliar Colega */
.avaliar-button {
  padding: 6px 12px;
  font-size: 0.9em;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap; /* Impede quebra de texto */
  transition: background-color 0.2s;
}
.avaliar-button:hover { background-color: #0056b3; }

/* Mensagens de estado */
.loading-state, .error-state, .empty-list-message {
  text-align: center; padding: 2rem 1rem; margin-top: 1rem; background-color: #f8f9fa; border-radius: 8px; color: #6c757d;
}
.error-state { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.error-state button { margin-top: 1rem; padding: 8px 15px; cursor: pointer; border-radius: 4px; border: 1px solid #721c24; background-color: transparent; color: #721c24; transition: background-color 0.2s, color 0.2s; }
.error-state button:hover { background-color: #721c24; color: white; }
.empty-list-message { background-color: transparent; padding: 1rem; } /* Mensagem dentro do card */

/* --- Media Queries --- */
@media (max-width: 768px) {
  .page-container { padding: 1rem; }
  .content-wrapper { gap: 1.5rem; } /* Reduz espaço entre colunas/linhas */
  .list-card { padding: 1rem; }
  li { flex-direction: column; align-items: flex-start; gap: 0.5rem;} /* Empilha info e botão */
  .avaliar-button { margin-top: 0.5rem; } /* Adiciona espaço acima do botão */
}

@media (max-width: 480px) {
    h1 { font-size: 1.8em; }
    .list-card h2 { font-size: 1.15em; }
}
</style>