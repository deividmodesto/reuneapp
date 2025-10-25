<script setup>
import { ref } from 'vue'; // Importa ref para definir dados reativos
import { useRouter } from 'vue-router';
import Menubar from 'primevue/menubar'; // Importa o componente Menubar

const router = useRouter();

// Função de Logout (igual a antes)
const handleLogout = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  router.push({ name: 'Login' });
};

// Define os itens do menu para o Menubar
// A estrutura segue a documentação do PrimeVue
const items = ref([
  {
    label: 'Dashboard',
    icon: 'pi pi-fw pi-home', // Ícone da biblioteca primeicons
    command: () => router.push('/') // Navega ao clicar
  },
  {
    label: 'OKRs',
    icon: 'pi pi-fw pi-flag',
    command: () => router.push('/okrs')
  },
  {
    label: 'Feedbacks',
    icon: 'pi pi-fw pi-comments',
    command: () => router.push('/feedbacks')
  },
  {
    label: 'Clima',
    icon: 'pi pi-fw pi-sun',
    command: () => router.push('/clima')
  },
  {
    label: 'Avaliações',
    icon: 'pi pi-fw pi-users',
    command: () => router.push('/avaliacoes')
  },
  {
    label: 'Sair',
    icon: 'pi pi-fw pi-sign-out',
    command: handleLogout // Chama a função de logout ao clicar
  }
]);
</script>

<template>
  <div id="app-layout">
    <header>
      <Menubar :model="items" class="main-menubar">
          <template #start>
              <h2 class="app-title">Reúne RH</h2>
          </template>
      </Menubar>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
        <p>&copy; {{ new Date().getFullYear() }} Reúne App</p>
    </footer>
  </div>
</template>

<style> /* Alterado de scoped para global para alguns estilos base */

/* Estilos Globais (pode ir para style.css se preferir) */
body {
  margin: 0; /* Remove margem padrão do body */
  font-family: var(--font-family); /* Usa a fonte definida pelo tema PrimeVue */
  background-color: #f4f7f6; /* Fundo cinza claro para a página toda */
  color: var(--text-color); /* Usa a cor de texto do tema */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Layout Principal */
#app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  flex-shrink: 0; /* Impede que o header encolha */
  /* Removemos estilos específicos do header antigo, o Menubar cuida disso */
}

/* Estilo para o título dentro do Menubar */
.app-title {
    margin: 0 1rem 0 0; /* Margem à direita */
    font-weight: 600;
    color: var(--primary-color); /* Usa a cor primária do tema */
}

/* Ajuste no Menubar para ocupar a largura */
.main-menubar {
    border-radius: 0; /* Remove cantos arredondados padrão */
    border-left: none;
    border-right: none;
}

main {
  padding: 1.5rem; /* Padding base */
  flex-grow: 1; /* Ocupa espaço restante */
  background-color: #ffffff; /* Fundo branco para a área de conteúdo */
}

footer {
    flex-shrink: 0;
    text-align: center;
    padding: 1rem;
    background-color: #e9ecef; /* Fundo cinza para o rodapé */
    color: #6c757d; /* Cor cinza para o texto do rodapé */
    font-size: 0.9em;
    border-top: 1px solid #dee2e6;
}

/* --- Media Queries --- */
@media (max-width: 768px) {
  main {
    padding: 1rem;
  }
   .app-title {
        font-size: 1.2em; /* Título menor em ecrãs pequenos */
    }
}
@media (max-width: 480px) {
  main {
    padding: 0.8rem;
  }
}

/* Estilos gerais para cards (podem ser movidos/refinados) */
.card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 6px; /* Usa o border-radius padrão do PrimeVue */
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
}

/* Estilos para formulários (podem ser movidos/refinados) */
.form-group {
    margin-bottom: 1rem;
}
.form-group label {
    display: block;
    margin-bottom: .5rem;
    font-weight: 600;
}

</style>