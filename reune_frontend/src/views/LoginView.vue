<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // <-- IMPORTE O ROTEADOR

// Inicializa o roteador para que possamos usá-lo para navegar
const router = useRouter();

const username = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
  error.value = '';
  try {
    const apiUrl = `${import.meta.env.VITE_API_BASE_URL}/api/token/`;
    const response = await axios.post(apiUrl, {
      username: username.value,
      password: password.value,
    });
    
    // 1. Pega o token de acesso da resposta
    const accessToken = response.data.access;
    console.log("Token recebido:", accessToken);

    // 2. Salva o token no localStorage do navegador para usá-lo em outras páginas
    localStorage.setItem('accessToken', accessToken);
    
    // 3. Redireciona o usuário para a página principal (Dashboard), definida como '/' no nosso router
    router.push('/');

  } catch (err) {
    console.error("Erro no login:", err);
    error.value = 'Falha no login. Verifique suas credenciais.';
  }
};
</script>

<template>
  <div class="container">
    <h1>Sistema de RH - Login</h1>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">Usuário</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Senha</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Entrar</button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<style scoped>
/* Estilos podem ser copiados do App.vue anterior */
.container { max-width: 400px; margin: 50px auto; padding: 20px; text-align: center; }
.login-form .form-group { margin-bottom: 15px; text-align: left; }
.error-message { color: red; }
/* Adicione outros estilos que desejar */
</style>