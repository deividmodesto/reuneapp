// reune_frontend/src/main.ts
import { createApp } from 'vue'
import App from './App.vue'     // Standard import for .vue
import router from '@/router';
import 'primevue/resources/themes/lara-light-indigo/theme.css'; 
import 'primevue/resources/primevue.min.css';

import PrimeVue from 'primevue/config';

// Keep standard PrimeVue CSS imports
import '../node_modules/primevue/resources/themes/lara-light-indigo/theme.css'; 
import '../node_modules/primevue/resources/primevue.min.css';
import '../node_modules/primeicons/primeicons.css';
const app = createApp(App)

app.use(router)
app.use(PrimeVue);

app.mount('#app')