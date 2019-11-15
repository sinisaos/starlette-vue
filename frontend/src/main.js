import 'bootstrap/dist/css/bootstrap.css'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import Vuelidate from 'vuelidate'
import App from './App.vue'
import router from './router'
import store from './store'
import Axios from 'axios'
import VuePaginate from 'vue-paginate'

Vue.use(BootstrapVue)
Vue.use(Vuelidate)
Vue.use(VuePaginate)
Vue.prototype.$http = Axios;
Axios.defaults.withCredentials = true;

const token = localStorage.getItem('token');
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
