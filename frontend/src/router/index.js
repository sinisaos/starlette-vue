import Vue from 'vue'
import Router from 'vue-router'
import store from '../store/index.js'
import Home from '../views/Home.vue'
import Login from '../components/accounts/Login.vue'
import Register from '../components/accounts/Register.vue'
import Dashboard from '../components/accounts/Dashboard.vue'
import Profile from '../components/accounts/Profile.vue'
import Questions from '../components/questions/Questions.vue'
import Question from '../components/questions/Question.vue'
import CreateQuestion from '../components/questions/CreateQuestion.vue'
import QuestionsByTag from '../components/questions/QuestionsByTag.vue'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/questions',
      name: 'questions',
      component: Questions
    },
    {
      path: '/questions/:id/:slug',
      name: 'question',
      component: Question
    },
    {
      path: '/create',
      name: 'createQuestion',
      component: CreateQuestion,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/questions/tags/:name',
      name: 'questionsByTag',
      component: QuestionsByTag
    },
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/')
  } else {
    next()
  }
})


export default router
