// reune_frontend/src/router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'; 
import LoginView from '../views/LoginView.vue';
import DashboardView from '../views/DashboardView.vue';
import OkrView from '../views/OkrView.vue';
import FeedbackView from '../views/FeedbackView.vue';
import ClimaView from '../views/ClimaView.vue';
import AvaliacoesView from '../views/AvaliacoesView.vue';
import RealizarAvaliacaoView from '../views/RealizarAvaliacaoView.vue';

const routes: Array<RouteRecordRaw> = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/', name: 'Dashboard', component: DashboardView },
  { path: '/okrs', name: 'OKRs', component: OkrView },
  { path: '/feedbacks', name: 'Feedbacks', component: FeedbackView },
  { path: '/clima', name: 'Clima', component: ClimaView },
  { path: '/avaliacoes', name: 'Avaliações', component: AvaliacoesView },
  { path: '/avaliacoes/realizar/:cicloId', name: 'RealizarAvaliacao', component: RealizarAvaliacaoView, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;