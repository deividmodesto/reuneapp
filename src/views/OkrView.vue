<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../api';

// Estados existentes
const objetivos = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Estados para o Check-in
const showCheckInForm = ref(false);
const currentKr = ref(null);
const checkInData = ref({
  valor_atual: null,
  nota_confianca: 3,
  comentario: ''
});
const checkInError = ref(null);
const checkInSuccess = ref(false);
const isSubmittingCheckIn = ref(false); // Novo estado para loading do check-in

// Função para buscar os objetivos
const fetchObjetivos = async () => {
  try {
    isLoading.value = true;
    error.value = null; // Limpa erro anterior ao tentar buscar novamente
    const response = await apiClient.get('/api/okr/objetivos/');
    objetivos.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar objetivos:", err);
    error.value = "Falha ao carregar objetivos. Verifique a ligação à API.";
  } finally {
    isLoading.value = false;
  }
};

// Função para abrir o formulário de check-in
const openCheckInForm = (kr) => {
  currentKr.value = kr;
  // Tenta preencher com o último valor ou o inicial
  const lastCheckinValue = kr.checkins && kr.checkins.length > 0 ? kr.checkins[0].valor_atual : kr.valor_inicial;
  checkInData.value = {
    valor_atual: lastCheckinValue,
    nota_confianca: 3,
    comentario: ''
  };
  checkInError.value = null;
  checkInSuccess.value = false;
  isSubmittingCheckIn.value = false; // Garante que loading está resetado
  showCheckInForm.value = true;
};

// Função para fechar o formulário de check-in
const closeCheckInForm = () => {
  showCheckInForm.value = false;
  currentKr.value = null;
};

// Função para enviar o check-in
const handleSendCheckIn = async () => {
  if (checkInData.value.valor_atual === null || checkInData.value.nota_confianca === null) {
    checkInError.value = "Preencha o valor atual e a nota de confiança.";
    return;
  }
  if (!currentKr.value) return; // Segurança extra

  isSubmittingCheckIn.value = true; // Ativa loading do botão
  checkInError.value = null;
  checkInSuccess.value = false;

  try {
    const payload = {
      resultado_chave: currentKr.value.id,
      valor_atual: checkInData.value.valor_atual,
      nota_confianca: checkInData.value.nota_confianca,
      comentario: checkInData.value.comentario
    };

    await apiClient.post('/api/okr/checkins/', payload); //

    checkInSuccess.value = true;
    // Fecha o modal e recarrega APÓS um pequeno delay para mostrar a msg de sucesso
    setTimeout(() => {
        closeCheckInForm();
        fetchObjetivos(); // Recarrega os OKRs para mostrar o progresso atualizado
    }, 1500); // Espera 1.5s

  } catch (err) {
    console.error("Erro ao enviar check-in:", err);
    checkInError.value = err.response?.data?.detail || "Falha ao enviar check-in. Tente novamente.";
  } finally {
      // Desativa o loading APÓS o delay de sucesso ou imediatamente no erro
      if(!checkInSuccess.value) {
          isSubmittingCheckIn.value = false;
      }
  }
};

// Carrega os objetivos quando o componente é montado
onMounted(() => {
  fetchObjetivos();
});
</script>

<template>
  <div class="page-container">
    <h1>Meus Objetivos e KRs</h1>

    <div v-if="isLoading" class="loading-state">
      <p>A carregar objetivos...</p>
      </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchObjetivos">Tentar Novamente</button>
    </div>

    <div v-else-if="objetivos.length > 0" class="objetivo-lista">
      <div v-for="obj in objetivos" :key="obj.id" class="objetivo-card">
        <h3>{{ obj.titulo }}</h3>
        <p class="responsavel">
          Responsável: {{ obj.responsavel.first_name }} {{ obj.responsavel.last_name }}
        </p>
        <p class="progresso-geral">Progresso Geral: {{ obj.progresso }}%</p>
        <p class="descricao">{{ obj.descricao }}</p>

        <div v-if="obj.resultados_chave.length > 0" class="kr-section">
            <h4>Resultados-Chave:</h4>
            <ul class="kr-lista">
              <li v-for="kr in obj.resultados_chave" :key="kr.id" class="kr-item">
                <div class="kr-info">
                  <span class="kr-descricao">{{ kr.descricao }}</span>
                  <span class="kr-meta">
                    (Inic: {{ kr.valor_inicial }}, Alvo: {{ kr.valor_alvo }})
                  </span>
                  <span class="progresso">Progresso: {{ kr.progresso }}%</span>
                </div>
                <button @click="openCheckInForm(kr)" class="checkin-button">Check-in</button>
              </li>
            </ul>
        </div>
        <p v-else class="no-krs">Este objetivo ainda não possui Resultados-Chave.</p>
      </div>
    </div>

    <p v-else class="empty-state">
      Nenhum objetivo cadastrado no momento.
    </p>

    <div v-if="showCheckInForm" class="modal-overlay" @click.self="closeCheckInForm">
      <div class="modal-content">
        <h2>Fazer Check-in</h2>
        <p class="kr-modal-descricao">{{ currentKr?.descricao }}</p>
        <form @submit.prevent="handleSendCheckIn">
          <div class="form-group">
            <label for="valor_atual">Valor Atual:</label>
            <input type="number" step="any" id="valor_atual" v-model="checkInData.valor_atual" required>
            <small>(Valor inicial: {{ currentKr?.valor_inicial }}, Alvo: {{ currentKr?.valor_alvo }})</small>
          </div>
          <div class="form-group">
            <label for="nota_confianca">Nota de Confiança (1-5):</label>
            <select id="nota_confianca" v-model="checkInData.nota_confianca" required>
              <option value="5">5 - No caminho certo</option>
              <option value="4">4</option>
              <option value="3">3 - Neutro</option>
              <option value="2">2</option>
              <option value="1">1 - Em risco</option>
            </select>
          </div>
          <div class="form-group">
            <label for="comentario">Comentário:</label>
            <textarea id="comentario" v-model="checkInData.comentario" rows="3"></textarea>
          </div>

          <p v-if="checkInError" class="error-message modal-message">{{ checkInError }}</p>
          <p v-if="checkInSuccess" class="success-message modal-message">Check-in salvo com sucesso!</p>

          <div class="modal-actions">
            <button type="button" @click="closeCheckInForm" :disabled="isSubmittingCheckIn">Cancelar</button>
            <button type="submit" :disabled="isSubmittingCheckIn">
                {{ isSubmittingCheckIn ? 'A guardar...' : 'Salvar Check-in' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    </div>
</template>

<style scoped>
/* Estilos Gerais */
.page-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem; /* Padding ligeiramente aumentado */
}

h1 { text-align: center; margin-bottom: 2rem; }

/* Cards de Objetivo */
.objetivo-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}
.objetivo-card h3 { margin-top: 0; margin-bottom: 0.5rem; color: #0056b3; }
.responsavel { font-size: 0.9em; font-style: italic; color: #555; margin-bottom: 0.5rem; }
.progresso-geral { font-weight: bold; color: #1a73e8; margin-bottom: 0.8rem; }
.descricao { font-size: 0.95em; color: #444; line-height: 1.5; margin-bottom: 1rem; }

/* Secção de KRs */
.kr-section { margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #eee; }
.kr-section h4 { margin-top: 0; margin-bottom: 1rem; color: #333; }
.kr-lista { list-style: none; padding: 0; margin: 0; }
.kr-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 0;
  border-bottom: 1px dashed #eee;
}
.kr-item:last-child { border-bottom: none; }
.kr-info { display: flex; flex-direction: column; flex-grow: 1; margin-right: 1rem; }
.kr-descricao { font-weight: 500; }
.kr-meta { font-size: 0.85em; color: #666; }
.progresso { font-weight: bold; color: #0056b3; font-size: 0.9em; margin-top: 4px; }
.no-krs { font-style: italic; color: #888; margin-top: 1rem; }

/* Botão de Check-in */
.checkin-button {
  padding: 6px 12px;
  font-size: 0.9em;
  background-color: #28a745; /* Verde */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap; /* Impede quebra de linha */
  transition: background-color 0.2s;
}
.checkin-button:hover { background-color: #218838; }

/* Estados de Carregamento, Erro e Vazio */
.loading-state, .error-state, .empty-state {
  text-align: center; padding: 3rem 1rem; margin-top: 2rem; background-color: #f8f9fa; border-radius: 8px; color: #6c757d;
}
.error-state { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.error-state button { margin-top: 1rem; padding: 8px 15px; cursor: pointer; border-radius: 4px; border: 1px solid #721c24; background-color: transparent; color: #721c24; transition: background-color 0.2s, color 0.2s; }
.error-state button:hover { background-color: #721c24; color: white; }

/* Modal de Check-in */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 1rem; /* Adiciona padding para evitar que o modal toque as bordas */ box-sizing: border-box; }
.modal-content { background-color: white; padding: 2rem; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); width: 100%; max-width: 500px; max-height: 90vh; /* Altura máxima */ overflow-y: auto; /* Permite scroll se o conteúdo for grande */ }
.modal-content h2 { margin-top: 0; margin-bottom: 0.5rem; }
.kr-modal-descricao { font-weight: 500; margin-bottom: 1.5rem; color: #555; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.form-group input[type="number"], .form-group select, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.form-group small { font-size: 0.8em; color: #666; margin-top: 4px; display: block; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #eee; }
.modal-actions button { padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; font-weight: 500; }
.modal-actions button[type="button"] { background-color: #6c757d; color: white; }
.modal-actions button[type="button"]:hover:not(:disabled) { background-color: #5a6268; }
.modal-actions button[type="submit"] { background-color: #007bff; color: white; }
.modal-actions button[type="submit"]:hover:not(:disabled) { background-color: #0056b3; }
.modal-actions button:disabled { background-color: #adb5bd; cursor: not-allowed; }

/* Mensagens dentro do Modal */
.modal-message { font-size: 0.9em; margin-top: 1rem; padding: 10px; border-radius: 4px; text-align: center; }
.error-message.modal-message { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;}
.success-message.modal-message { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;}

/* --- Media Queries para Responsividade --- */
@media (max-width: 768px) {
  .page-container { padding: 1rem; }
  .objetivo-card { padding: 1rem; }
  .kr-item { flex-direction: column; /* Empilha info e botão */ align-items: flex-start; /* Alinha à esquerda */ gap: 0.5rem; /* Espaço entre info e botão */ }
  .checkin-button { margin-left: 0; margin-top: 0.5rem; /* Espaço acima do botão */ }
}

@media (max-width: 480px) {
  .modal-content { padding: 1.5rem; }
  .modal-actions { flex-direction: column; gap: 0.5rem; } /* Botões em coluna */
  .modal-actions button { width: 100%; } /* Botões ocupam largura total */
}
</style>