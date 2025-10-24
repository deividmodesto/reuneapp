import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import DashboardView from '../views/DashboardView.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView
  },
  // Adicionaremos outras rotas aqui (OKRs, Feedbacks, etc.)
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;