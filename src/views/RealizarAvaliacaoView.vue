<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '../api';

// Props
const props = defineProps({
  cicloId: { type: [String, Number], required: true }
});

const router = useRouter();

// Estados
const ciclo = ref(null);
const competencias = ref([]);
const colaboradores = ref([]);
const isLoading = ref(true);
const error = ref(null);
const submitError = ref(null);
const submitSuccess = ref(false);
const isSubmitting = ref(false); // Loading para submissão

// Estado do formulário
const avaliadoId = ref(null);
const respostas = ref({}); // { compId: { nota: null, justificativa: '' } }

// Busca dados
const fetchData = async () => {
  try {
    isLoading.value = true;
    error.value = null; // Limpa erro
    const cicloIdNum = Number(props.cicloId);
    const [cicloRes, compRes, colabRes] = await Promise.all([
      apiClient.get(`/api/avaliacoes/ciclos/${cicloIdNum}/`),
      apiClient.get('/api/avaliacoes/competencias/'),
      apiClient.get('/api/usuarios/colaboradores/')
    ]);

    ciclo.value = cicloRes.data;
    competencias.value = compRes.data;
    colaboradores.value = colabRes.data;

    // Inicializa respostas
    competencias.value.forEach(comp => {
      respostas.value[comp.id] = { nota: null, justificativa: '' };
    });

  } catch (err) {
    console.error("Erro ao buscar dados para avaliação:", err);
    error.value = "Falha ao carregar dados necessários.";
    if (err.response?.status === 404) error.value = "Ciclo ou dados não encontrados.";
  } finally {
    isLoading.value = false;
  }
};

// Validação do formulário
const isFormValid = computed(() => {
  if (!avaliadoId.value) return false;
  return competencias.value.every(comp => respostas.value[comp.id]?.nota !== null);
});

// Submissão
const handleSubmitAvaliacao = async () => {
  if (!isFormValid.value) {
    submitError.value = "Selecione o colega e preencha a nota para todas as competências.";
    setTimeout(() => { submitError.value = null }, 4000); // Erro temporário
    return;
  }

  isSubmitting.value = true; // Ativa loading
  submitError.value = null;
  submitSuccess.value = false;

  try {
    const payload = Object.entries(respostas.value).map(([competenciaId, resposta]) => ({
      ciclo: Number(props.cicloId),
      avaliado: avaliadoId.value,
      competencia: Number(competenciaId),
      nota: resposta.nota,
      justificativa: resposta.justificativa
    }));

    // Envia todas as respostas em paralelo
    await Promise.all(
        payload.map(respPayload => apiClient.post('/api/avaliacoes/respostas/', respPayload)) //
    );

    submitSuccess.value = true;
    setTimeout(() => {
        router.push({ name: 'Avaliações' }); // Volta após 2s
    }, 2000);

  } catch (err) {
    console.error("Erro ao submeter avaliação:", err);
    // Tenta obter mensagem específica (ex: duplicidade)
    submitError.value = err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || "Falha ao salvar. Verifique se já avaliou este colega neste ciclo.";
    setTimeout(() => { submitError.value = null }, 5000); // Erro temporário
  } finally {
      // Garante que loading só desativa após o delay de sucesso
     if(!submitSuccess.value) {
        isSubmitting.value = false;
     }
  }
};

// Busca dados ao montar
onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="page-container">
    <h1 v-if="!isLoading && !error">Realizar Avaliação</h1>
    <h1 v-else-if="isLoading">A Carregar Avaliação...</h1>
    <h1 v-else>Erro</h1>

    <div v-if="isLoading" class="loading-state"><p>A carregar dados...</p></div>
    <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchData">Tentar Novamente</button>
        <button @click="router.push({ name: 'Avaliações' })" style="margin-left: 10px;">Voltar</button>
    </div>

    <div v-else>
      <div class="ciclo-header">
        <h2>Ciclo: {{ ciclo?.titulo }}</h2>
        <p>Período: {{ new Date(ciclo?.data_inicio).toLocaleDateString() }} - {{ new Date(ciclo?.data_fim).toLocaleDateString() }}</p>
      </div>

      <form @submit.prevent="handleSubmitAvaliacao" class="avaliacao-form">
        <div class="form-group select-avaliado">
          <label for="avaliado">Selecione o Colega Avaliado:</label>
          <select id="avaliado" v-model="avaliadoId" required :disabled="isSubmitting">
            <option :value="null" disabled>-- Selecione --</option>
            <option v-for="colab in colaboradores" :key="colab.usuario.id" :value="colab.usuario.id">
              {{ colab.usuario.first_name }} {{ colab.usuario.last_name }} ({{ colab.cargo?.titulo || 'Sem cargo' }})
            </option>
          </select>
        </div>

        <hr class="divider">

        <h3>Competências</h3>
        <div class="competencias-container">
            <div v-for="comp in competencias" :key="comp.id" class="competencia-card">
              <h4>{{ comp.nome }}</h4>
              <p class="competencia-descricao">{{ comp.descricao }}</p>

              <div class="form-group notas-group">
                <label :for="'nota-' + comp.id">Nota (1 a 5):</label>
                <div class="notas-options">
                  <label v-for="n in 5" :key="n" class="nota-label">
                    <input
                      type="radio"
                      :name="'nota-' + comp.id"
                      :value="n"
                      v-model="respostas[comp.id].nota"
                      required
                      :disabled="isSubmitting"
                    />
                    <span>{{ n }}</span>
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label :for="'just-' + comp.id">Justificativa (Opcional):</label>
                <textarea
                  :id="'just-' + comp.id"
                  v-model="respostas[comp.id].justificativa"
                  rows="2"
                  :disabled="isSubmitting"
                ></textarea>
              </div>
            </div>
        </div>

        <div class="submit-section">
            <p v-if="submitError" class="message error-message">{{ submitError }}</p>
            <p v-if="submitSuccess" class="message success-message">Avaliação enviada com sucesso! A redirecionar...</p>
            <button type="submit" :disabled="!isFormValid || isSubmitting">
                {{ isSubmitting ? 'A Enviar...' : 'Enviar Avaliação' }}
            </button>
        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  max-width: 850px; /* Largura ajustada */
  margin: 0 auto;
  padding: 1.5rem;
}

h1 { text-align: center; margin-bottom: 1.5rem; }

/* Cabeçalho do Ciclo */
.ciclo-header {
    background-color: #f8f9fa;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    border: 1px solid #e0e0e0;
}
.ciclo-header h2 { margin: 0 0 0.5rem 0; font-size: 1.4em; }
.ciclo-header p { margin: 0; color: #555; }

.avaliacao-form { margin-top: 1rem; }
.divider { border: 0; border-top: 1px solid #eee; margin: 2rem 0; }

.form-group { margin-bottom: 1.5rem; }
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
.select-avaliado { max-width: 500px; /* Limita largura do select */ }

/* Container das competências */
.competencias-container { margin-top: 1rem; }
.competencia-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.competencia-card h4 { margin-top: 0; margin-bottom: 0.5rem; color: #333; }
.competencia-descricao { font-size: 0.9em; color: #555; margin-bottom: 1rem; line-height: 1.5; }

/* Grupo de Notas */
.notas-group { margin-bottom: 1rem; }
.notas-group label:first-child { margin-bottom: 0.8rem; } /* Label "Nota (1 a 5):" */
.notas-options { display: flex; flex-wrap: wrap; /* Permite quebra de linha */ gap: 0.8rem; /* Espaço entre botões de nota */ align-items: center; }
.nota-label { display: inline-flex; align-items: center; cursor: pointer; margin: 0; }
.nota-label input[type="radio"] { display: none; } /* Esconde rádio original */
.nota-label span {
  display: inline-block;
  padding: 8px 14px; /* Tamanho do botão de nota */
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
  font-weight: 500;
}
.nota-label:hover span { background-color: #f0f0f0; }
.nota-label input[type="radio"]:checked + span {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}
.nota-label input[type="radio"]:disabled + span {
    background-color: #e9ecef;
    cursor: not-allowed;
    color: #6c757d;
    border-color: #ced4da;
}


/* Secção de Submissão */
.submit-section { margin-top: 2rem; text-align: right; }
.submit-section button {
  padding: 12px 25px;
  font-size: 1.1em;
  font-weight: 500;
  background-color: #28a745; /* Verde */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.submit-section button:hover:not(:disabled) { background-color: #218838; }
.submit-section button:disabled { background-color: #6c757d; cursor: not-allowed; }

/* Mensagens de feedback */
.message { font-size: 0.9em; margin-bottom: 1rem; /* Acima do botão */ padding: 10px; border-radius: 4px; text-align: center; }
.error-message { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;}
.success-message { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;}

/* Estados Gerais */
.loading-state, .error-state { text-align: center; padding: 3rem 1rem; margin-top: 2rem; background-color: #f8f9fa; border-radius: 8px; color: #6c757d; }
.error-state { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.error-state button { margin-top: 1rem; padding: 8px 15px; cursor: pointer; border-radius: 4px; border: 1px solid #721c24; background-color: transparent; color: #721c24; transition: background-color 0.2s, color 0.2s; }
.error-state button:hover { background-color: #721c24; color: white; }

/* --- Media Queries --- */
@media (max-width: 768px) {
  .page-container { padding: 1rem; }
  .ciclo-header { padding: 1rem; }
  .select-avaliado { max-width: none; } /* Permite que o select ocupe a largura */
  .competencia-card { padding: 1rem; }
  .notas-options { gap: 0.5rem; } /* Menos espaço entre notas */
  .nota-label span { padding: 6px 10px; } /* Botões de nota menores */
}

@media (max-width: 480px) {
  h1 { font-size: 1.6em; }
  .ciclo-header h2 { font-size: 1.2em; }
  .submit-section { text-align: center; }
  .submit-section button { width: 100%; } /* Botão ocupa largura total */
}
</style>