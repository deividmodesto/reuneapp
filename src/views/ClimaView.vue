<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../api';

// Estados para dados e carregamento inicial
const registros = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Opções de humor baseadas no models.py
const humorOptions = [
  { valor: 5, label: 'Muito Feliz', emoji: '😄' },
  { valor: 4, label: 'Feliz', emoji: '😊' },
  { valor: 3, label: 'Neutro', emoji: '😐' },
  { valor: 2, label: 'Triste', emoji: '😟' },
  { valor: 1, label: 'Muito Triste', emoji: '😢' },
];

// Estados para o formulário de novo registo
const novoHumor = ref(null);
const novoComentario = ref('');
const isSubmitting = ref(false); // NOVO: Estado de loading para envio
const sendError = ref(null);
const sendSuccess = ref(false);
const successMessage = ref(''); // Para mensagem temporária

// Função para buscar os registos
const fetchRegistros = async () => {
  try {
    isLoading.value = true;
    error.value = null; // Limpa erro anterior
    const response = await apiClient.get('/api/clima/registros-humor/'); //
    registros.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar registos de humor:", err);
    error.value = "Falha ao carregar registos de humor.";
  } finally {
    isLoading.value = false;
  }
};

// Função para enviar o registo de humor
const handleSendHumor = async () => {
  if (!novoHumor.value) {
    sendError.value = "Por favor, selecione como você está se sentindo.";
    // Limpa erro após 3 segundos
    setTimeout(() => { sendError.value = null; }, 3000);
    return;
  }
  
  isSubmitting.value = true; // Ativa loading
  sendError.value = null;
  sendSuccess.value = false;
  successMessage.value = '';

  try {
    // Payload com humor e comentário
    await apiClient.post('/api/clima/registros-humor/', {
      humor: novoHumor.value,
      comentario: novoComentario.value
    });

    sendSuccess.value = true;
    successMessage.value = "Humor registado com sucesso!"; // Define mensagem
    novoHumor.value = null; // Reseta seleção
    novoComentario.value = ''; // Limpa comentário

    // Limpa mensagem de sucesso após 3 segundos
    setTimeout(() => {
        sendSuccess.value = false;
        successMessage.value = '';
    }, 3000);

    // Recarrega a lista após um pequeno delay
    setTimeout(() => { fetchRegistros(); }, 500);

  } catch (err) {
    console.error("Erro ao enviar humor:", err);
    // Tenta pegar erro de duplicidade do backend (unique_together)
    if (err.response && err.response.status === 400 && err.response.data?.non_field_errors) {
         sendError.value = "Você já registou o seu humor hoje.";
    } else if (err.response && err.response.data?.detail) {
        sendError.value = err.response.data.detail;
    }
     else {
        sendError.value = "Falha ao enviar o registo. Tente novamente.";
    }
     // Limpa erro após 5 segundos
    setTimeout(() => { sendError.value = null; }, 5000);
  } finally {
    isSubmitting.value = false; // Desativa loading
  }
};

// Busca dados ao montar
onMounted(() => {
  fetchRegistros();
});
</script>

<template>
  <div class="page-container">
    <h1>Termómetro de Clima</h1>

    <div class="form-card">
      <h2>Como você está se sentindo hoje?</h2>
      <form @submit.prevent="handleSendHumor">
        <div class="humor-options">
          <label v-for="opt in humorOptions" :key="opt.valor" class="humor-label">
            <input
              type="radio"
              :value="opt.valor"
              v-model="novoHumor"
              name="humor"
              :disabled="isSubmitting"
            />
            <div class="emoji-box" :class="{ selected: novoHumor === opt.valor }">
              <span class="emoji">{{ opt.emoji }}</span>
              <span class="label">{{ opt.label }}</span>
            </div>
          </label>
        </div>
        <div class="form-group">
          <label for="comentario">Algum comentário? (Opcional)</label>
          <textarea
            id="comentario"
            v-model="novoComentario"
            rows="3"
            :disabled="isSubmitting"
          ></textarea>
        </div>
        <p v-if="sendError" class="message error-message">{{ sendError }}</p>
        <p v-if="sendSuccess" class="message success-message">{{ successMessage }}</p>
        <button type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? 'A Registar...' : 'Registar Humor' }}
        </button>
      </form>
    </div>

    <hr class="divider">
    <h2>Registos Anteriores</h2>
    
    <div v-if="isLoading" class="loading-state">
        <p>A carregar registos...</p>
    </div>
    <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchRegistros">Tentar Novamente</button>
    </div>
    <ul v-else-if="registros.length > 0" class="registros-lista">
      <li v-for="reg in registros" :key="reg.id" class="registro-item">
        <span class="data">{{ new Date(reg.data_registro).toLocaleDateString() }}</span>
        <span class="humor">{{ reg.humor_texto }}</span>
        <p v-if="reg.comentario" class="comentario">{{ reg.comentario }}</p>
      </li>
    </ul>
    <p v-else class="empty-state">Nenhum registo de humor encontrado.</p>
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

/* Opções de Humor */
.humor-options {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap; /* Permite quebrar linha em ecrãs pequenos */
  gap: 1rem; /* Espaço entre as opções */
  margin-bottom: 1.5rem;
}
.humor-label { cursor: pointer; text-align: center; }
.humor-label input[type="radio"] { display: none; } /* Esconde o botão de rádio padrão */
.emoji-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 15px; /* Padding ajustado */
  border-radius: 8px;
  border: 2px solid transparent;
  transition: all 0.2s ease-in-out;
  min-width: 80px; /* Largura mínima para alinhar */
}
.emoji-box:hover { background-color: #f0f0f0; }
.emoji-box.selected {
  border-color: #007bff;
  background-color: #e6f2ff;
  transform: scale(1.05); /* Efeito de zoom leve */
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
}
.emoji { font-size: 2.5rem; margin-bottom: 5px; }
.label { font-size: 0.9em; font-weight: 500; }

/* Campo Comentário */
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #495057; }
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  box-sizing: border-box;
  resize: vertical; /* Permite redimensionar apenas verticalmente */
}
.form-group textarea:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Botão de Submissão */
button[type="submit"] {
  width: 100%;
  padding: 12px;
  font-size: 1.1em;
  font-weight: 500;
  background-color: #28a745; /* Verde */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 1rem;
}
button:hover:not(:disabled) { background-color: #218838; }
button:disabled { background-color: #6c757d; cursor: not-allowed; }

/* Mensagens de feedback do formulário */
.message { font-size: 0.9em; margin-top: 1rem; margin-bottom: 0; padding: 10px; border-radius: 4px; text-align: center; }
.error-message { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;}
.success-message { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;}

/* Lista de Registos */
.registros-lista { list-style-type: none; padding: 0; margin-top: 1rem; }
.registro-item {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  flex-wrap: wrap; /* Permite quebra de linha */
  align-items: center; /* Alinha itens verticalmente */
  gap: 10px 20px; /* Espaçamento entre data, humor, comentário */
}
.registro-item .data { font-weight: bold; color: #333; }
.registro-item .humor { font-weight: 500; color: #0056b3; }
.registro-item .comentario {
  font-size: 0.9em;
  color: #555;
  margin: 5px 0 0 0; /* Pequena margem superior */
  width: 100%; /* Ocupa linha própria */
  border-left: 3px solid #eee; /* Linha à esquerda para destaque */
  padding-left: 10px;
}

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
  .humor-options { gap: 0.5rem; } /* Menos espaço entre emojis */
  .emoji-box { min-width: 65px; padding: 8px 10px;}
  .emoji { font-size: 2rem; }
  .registro-item { padding: 0.8rem 1rem; }
}

@media (max-width: 480px) {
  h1 { font-size: 1.8em; }
  h2 { font-size: 1.3em; }
  .form-card { padding: 1rem; }
  .emoji-box { min-width: 55px; padding: 5px 8px;} /* Ainda menor */
  .emoji { font-size: 1.8rem; }
  .label { font-size: 0.8em; }
  button[type="submit"] { font-size: 1em; }
}
</style>