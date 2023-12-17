import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min';
import router from './routers';
import store from './store/store';
import './registerServiceWorker'
import '../fonts.css'

let vm = createApp(App)
vm.use(router);
vm.use(store);
vm.mount('#app')
