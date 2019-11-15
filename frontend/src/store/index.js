import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: [],
    users: [],
  },
  mutations: {
    AUTH_REQUEST(state, users) {
      state.status = 'loading'
      state.users = users
    },
    AUTH_SUCCES(state, token, user) {
      state.status = 'success'
      state.token = token
      state.user = user
    },
    AUTH_ERROR(state) {
      state.status = 'error'
    },
    LOGOUT(state) {
      state.status = ''
      state.token = ''
    },
    DELETE_USER(state, id) {
      const users = state.users.filter(user => user.id == id)
      state.users = users
    }
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('AUTH_REQUEST')
        axios({
          url: 'http://localhost:8000/accounts/login',
          data: user,
          method: 'POST'
        })
          .then(resp => {
            const token = resp.data.auth_user
            const user = resp.data.result
            const users = resp.data.results
            localStorage.setItem('token', token)
            axios.defaults.headers.common['Authorization'] = token
            commit('AUTH_SUCCES', token)
            commit('AUTH_SUCCES', user)
            commit('AUTH_REQUEST', users)
            resolve(resp)
          })
          .catch(err => {
            commit('AUTH_ERROR')
            localStorage.removeItem('token')
            reject(err)
          })
      })
    },
    register({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('AUTH_REQUEST')
        axios({
          url: 'http://localhost:8000/accounts/register',
          data: user,
          method: 'POST'
        })
          .then(resp => {
            const token = resp.data.auth_user
            const user = resp.data.result
            localStorage.setItem('token', token)
            axios.defaults.headers.common['Authorization'] = token
            commit('AUTH_SUCCES', token)
            commit('AUTH_SUCCES', user)
            resolve(resp)
          })
          .catch(err => {
            commit('AUTH_ERROR', err)
            localStorage.removeItem('token')
            reject(err)
          })
      })
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('LOGOUT')
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    },
    delete_user({ commit, state, dispatch }, user) {
      return new Promise((resolve, reject) => {
        if (confirm("Are you sure you want to delete the account!"))
          axios({
            url: 'http://localhost:8000/accounts/delete/' + state.token[0].id,
            data: user,
            method: 'GET'
          })
            .then(resp => {
              commit('DELETE_USER')
              commit('LOGOUT')
              dispatch('logout')
              resolve(resp)
            })
            .catch(err => {
              reject(err)
            })
      })
    }
  },
  getters: {
    authUser: state => state.token,
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    allUsers: state => state.users,
  }
})

