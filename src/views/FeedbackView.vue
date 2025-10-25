<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../api';

// Estados para dados e carregamento inicial
const feedbacks = ref([]);
const colaboradores = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Estados para o formulário de novo feedback
const novoFeedbackTexto = ref('');
const novoFeedbackReceptor = ref(null);
const isSubmitting = ref(false); // NOVO: Estado de loading para envio
const sendError = ref(null);
const sendSuccess = ref(false);
const successMessage = ref(''); // Para mensagem temporária

// Função para buscar dados iniciais
const fetchData = async () => {
  try {
    isLoading.value = true;
    error.value = null; // Limpa erro anterior
    const [feedbacksRes, colabRes] = await Promise.all([
      apiClient.get('/api/feedback/feedbacks/'), //
      apiClient.get('/api/usuarios/colaboradores/') //
    ]);
    
    feedbacks.value = feedbacksRes.data;
    colaboradores.value = colabRes.data;
  } catch (err) {
    console.error("Erro ao buscar dados de feedback:", err);
    error.value = "Falha ao carregar dados da página.";
  } finally {
    isLoading.value = false;
  }
};

// Função para enviar o feedback
const handleSendFeedback = async () => {
  if (!novoFeedbackTexto.value || !novoFeedbackReceptor.value) {
    sendError.value = "Por favor, selecione um receptor e escreva uma mensagem.";
    // Limpa o erro após 3 segundos
    setTimeout(() => { sendError.value = null; }, 3000);
    return;
  }

  isSubmitting.value = true; // Ativa loading
  sendError.value = null;
  sendSuccess.value = false;
  successMessage.value = '';

  try {
    const payload = {
      receptor_id: novoFeedbackReceptor.value, //
      texto: novoFeedbackTexto.value
    };

    await apiClient.post('/api/feedback/feedbacks/', payload);

    sendSuccess.value = true;
    successMessage.value = "Feedback enviado com sucesso!"; // Define mensagem
    novoFeedbackTexto.value = '';
    novoFeedbackReceptor.value = null;
    
    // Limpa a mensagem de sucesso após 3 segundos
    setTimeout(() => {
        sendSuccess.value = false;
        successMessage.value = '';
    }, 3000);

    // Recarrega a lista após um pequeno delay para garantir que o novo item apareça
    setTimeout(() => { fetchData(); }, 500);

  } catch (err) {
    console.error("Erro ao enviar feedback:", err);
    sendError.value = err.response?.data?.detail || "Falha ao enviar feedback. Tente novamente.";
     // Limpa o erro após 5 segundos
    setTimeout(() => { sendError.value = null; }, 5000);
  } finally {
    isSubmitting.value = false; // Desativa loading
  }
};

// Busca os dados ao montar
onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="page-container">
    <h1>Feedbacks</h1>

    <div class="form-card">
      <h2>Enviar Novo Feedback</h2>
      <form @submit.prevent="handleSendFeedback">
        <div class="form-group">
          <label for="receptor">Para:</label>
          <select id="receptor" v-model="novoFeedbackReceptor" :disabled="isSubmitting">
            <option :value="null" disabled>Selecione um colaborador...</option>
            <option v-for="colab in colaboradores" :key="colab.usuario.id" :value="colab.usuario.id">
              {{ colab.usuario.first_name }} {{ colab.usuario.last_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="texto">Mensagem:</label>
          <textarea id="texto" v-model="novoFeedbackTexto" rows="4" :disabled="isSubmitting"></textarea>
        </div>
        <p v-if="sendError" class="message error-message">{{ sendError }}</p>
        <p v-if="sendSuccess" class="message success-message">{{ successMessage }}</p>
        <button type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? 'A Enviar...' : 'Enviar' }}
        </button>
      </form>
    </div>

    <hr class="divider">
    <h2>Meus Feedbacks</h2>

    <div v-if="isLoading" class="loading-state">
        <p>A carregar feedbacks...</p>
    </div>
    <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchData">Tentar Novamente</button>
    </div>
    <div v-else-if="feedbacks.length > 0" class="feedback-lista">
      <div v-for="fb in feedbacks" :key="fb.id" class="feedback-card">
        <p class="meta">
          <strong>De: {{ fb.emissor.first_name || fb.emissor.username || 'Utilizador' }}</strong>
          para
          <strong>{{ fb.receptor.first_name || fb.receptor.username || 'Utilizador' }}</strong>
          <span class="data">{{ new Date(fb.data_criacao).toLocaleString() }}</span> </p>
        <p class="texto">{{ fb.texto }}</p>
      </div>
    </div>
    <p v-else class="empty-state">Você ainda não recebeu ou enviou feedbacks.</p>
  </div>
</template>

<style scoped>
.page-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem;
}

h1, h2 { text-align: center; margin-bottom: 1.5rem; }
h2 { margin-top: 2rem; }

.divider { border: 0; border-top: 1px solid #eee; margin: 2.5rem 0; }

/* Card do Formulário */
.form-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}
.form-card h2 { margin-top: 0; text-align: left; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #495057; }
.form-group select, .form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}
.form-group select:focus, .form-group textarea:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
button[type="submit"] {
  width: 100%;
  padding: 12px;
  font-size: 1.1em;
  font-weight: 500;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 1rem; /* Espaço acima do botão */
}
button:hover:not(:disabled) { background-color: #0056b3; }
button:disabled { background-color: #6c757d; cursor: not-allowed; }

/* Mensagens de feedback do formulário */
.message {
  font-size: 0.9em;
  margin-top: 1rem; /* Espaço acima da mensagem */
  margin-bottom: 0; /* Remove espaço abaixo antes do botão */
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}
.error-message { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;}
.success-message { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;}

/* Lista de Feedbacks */
.feedback-lista { margin-top: 1rem; }
.feedback-card {
  border: 1px solid #e0e0e0;
  padding: 1.2rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.feedback-card .meta {
  margin-bottom: 0.5rem;
  color: #555;
  font-size: 0.9em;
  display: flex; /* Alinha 'De/Para' e 'Data' */
  justify-content: space-between;
  flex-wrap: wrap; /* Permite quebrar linha em ecrãs pequenos */
  gap: 5px;
}
.feedback-card .data { color: #777; white-space: nowrap; }
.feedback-card .texto { margin-top: 5px; color: #333; line-height: 1.6; }

/* Estados de Carregamento, Erro e Vazio */
.loading-state, .error-state, .empty-state {
  text-align: center; padding: 3rem 1rem; margin-top: 2rem; background-color: #f8f9fa; border-radius: 8px; color: #6c757d;
}
.error-state { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.error-state button { margin-top: 1rem; padding: 8px 15px; cursor: pointer; border-radius: 4px; border: 1px solid #721c24; background-color: transparent; color: #721c24; transition: background-color 0.2s, color 0.2s; }
.error-state button:hover { background-color: #721c24; color: white; }

/* --- Media Queries --- */
@media (max-width: 768px) {
  .page-container { padding: 1rem; }
  .form-card { padding: 1.5rem; }
  .feedback-card { padding: 1rem; }
}

@media (max-width: 480px) {
    h1 { font-size: 1.8em; }
    h2 { font-size: 1.3em; }
    .form-card { padding: 1rem; }
    .feedback-card .meta { flex-direction: column; align-items: flex-start; } /* Empilha 'De/Para' e 'Data' */
    .feedback-card .data { margin-top: 5px; }
}
</style>