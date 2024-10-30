import { createApp } from 'vue'
import { createBootstrap } from 'bootstrap-vue-next'
import router from "./router"
import store from "./store"
import axios from 'axios'
import App from './App.vue'
import VueAwesomePaginate from "vue-awesome-paginate"

// import the necessary css file
import "vue-awesome-paginate/dist/style.css"

// Add the necessary CSS
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://localhost:8000"

const app = createApp(App)
app.use(createBootstrap())
app.use(VueAwesomePaginate)
app.use(store)
app.use(router)
app.mount('#app')
