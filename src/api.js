// reune_frontend/src/api.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Interceptor de REQUISIÇÃO (adiciona o token)
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de RESPOSTA (lida com token expirado)
apiClient.interceptors.response.use(
  (response) => {
    // Se a resposta for boa, só a retorna
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Se o erro for 401 E não for uma tentativa de refresh
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Marca como "já tentei"
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        
        // Pede um token novo
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/token/refresh/`, {
          refresh: refreshToken
        });

        // Salva o token novo
        const newAccessToken = response.data.access;
        localStorage.setItem('accessToken', newAccessToken);

        // Atualiza o cabeçalho da requisição original
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        
        // Tenta a requisição original de novo
        return apiClient(originalRequest);

      } catch (refreshError) {
        // Se o refresh falhar (ex: token de refresh expirou)
        console.error("Erro ao renovar token:", refreshError);
        // Desloga o usuário e o manda para o login
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    // Se não for um erro 401, só retorna o erro
    return Promise.reject(error);
  }
);

export default apiClient;