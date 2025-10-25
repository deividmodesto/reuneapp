<script setup>
import { ref } from 'vue';
import apiClient from '../api';
import { useRouter } from 'vue-router';

// Importações dos componentes PrimeVue
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password'; // Componente específico para senhas
import Button from 'primevue/button';
import Message from 'primevue/message';
import FloatLabel from 'primevue/floatlabel'; // Para o efeito visual da label

const router = useRouter();

// Refs (sem alterações na lógica)
const username = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  error.value = '';
  isLoading.value = true;
  
  try {
    const apiUrl = `/api/token/`;
    const response = await apiClient.post(apiUrl, {
      username: username.value,
      password: password.value,
    });
    
    const accessToken = response.data.access;
    const refreshToken = response.data.refresh;
    
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    
    router.push('/');

  } catch (err) {
    console.error("Erro no login:", err);
    if (err.response?.data?.detail) {
        error.value = err.response.data.detail;
    } else {
        error.value = 'Falha no login. Verifique as suas credenciais ou a ligação à API.';
    }
     // Limpa o erro após 5 segundos
    setTimeout(() => { error.value = null; }, 5000);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login-container">
    <Card class="login-card">
      <template #title>
        <div class="card-title">
            <i class="pi pi-lock p-mr-2" style="font-size: 1.5rem; vertical-align: middle;"></i> Login Reúne RH
        </div>
      </template>
      <template #content>
        <form @submit.prevent="handleLogin" class="login-form">
          <FloatLabel class="form-group">
            <InputText
            id="username"
            v-model="username"
            required
            autocomplete="username"
            class="p-inputtext-lg" 
            style="width: 100%;" 
          />
            <label for="username">Utilizador</label>
          </FloatLabel>

          <FloatLabel class="form-group">
            <Password
              id="password"
              v-model="password"
              required
              autocomplete="current-password"
              :feedback="false"
              :toggleMask="true"
              inputClass="p-inputtext-lg" /* Aplica tamanho maior ao input interno */
              style="width: 100%;" /* Garante largura total do container */
              :inputStyle="{ width: '100%' }" /* Garante largura total do input interno */
            />
            <label for="password">Senha</label>
          </FloatLabel>

          <Message v-if="error" severity="error" :closable="false" class="error-message">
            {{ error }}
          </Message>

          <Button
            type="submit"
            label="Entrar"
            icon="pi pi-sign-in" /* Ícone de login */
            iconPos="right" /* Posição do ícone */
            :loading="isLoading" /* Mostra spinner quando isLoading=true */
            class="p-button-lg login-button" /* Botão grande */
            style="width: 100%;" /* Largura total */
          />
        </form>
      </template>
    </Card>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 150px); /* Ajustar conforme altura do header/footer */
  padding: 1.5rem;
  /* background-color: var(--surface-ground); Usa cor de fundo do tema */
}

.login-card {
  width: 100%;
  max-width: 450px; /* Largura máxima um pouco maior */
  /* O componente Card já tem sombra e padding, não precisamos definir aqui */
}

.card-title {
    text-align: center;
    margin-bottom: 1.5rem; /* Espaço abaixo do título */
    color: var(--primary-color); /* Cor primária do tema */
    display: flex; /* Alinha ícone e texto */
    align-items: center;
    justify-content: center;
    gap: 0.5rem; /* Espaço entre ícone e texto */
}

.login-form .form-group {
  margin-bottom: 2rem; /* Aumenta espaço entre os campos */
}

/* Ajuste necessário para o Password component ocupar largura total */
/* Precisamos estilizar o elemento interno que o PrimeVue cria */
:deep(.p-password input) {
    width: 100% !important;
}

.error-message {
  margin-top: 0;
  margin-bottom: 1.5rem;
  width: 100%; /* Ocupa largura total */
}

.login-button {
  margin-top: 1rem; /* Espaço acima do botão */
}

/* Media Queries */
@media (max-width: 480px) {
  .login-card {
     /* Remove sombra e adiciona borda em ecrãs muito pequenos, se desejado */
    /* box-shadow: none; */
    /* border: 1px solid var(--surface-border); */
    padding: 1.5rem 1rem; /* Reduz padding */
  }
   .card-title {
       font-size: 1.3em; /* Título um pouco menor */
   }
}
</style>