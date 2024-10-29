import { createStore } from 'vuex'
import VuexPersistence from 'vuex-persist'
import axios from 'axios'

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})


const store = createStore({
    state() {
        return {
            status: '',
            token: localStorage.getItem('token') || '',
            user: [],
        }
    },
    mutations: {
        AUTH_REQUEST(state) {
            state.status = 'loading'
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
        DELETE_USER(state) {
            state.user = ''
        }
    },
    actions: {
        login({ commit }, user) {
            return new Promise((resolve, reject) => {
                commit('AUTH_REQUEST')
                axios({
                    url: '/accounts/login',
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
                    url: '/accounts/register',
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
        logout({ commit }, user) {
            return new Promise((resolve, reject) => {
                axios({
                    url: '/accounts/logout',
                    data: user,
                    method: 'POST'
                })
                    .then(resp => {
                        commit('LOGOUT')
                        localStorage.removeItem('token')
                        delete axios.defaults.headers.common['Authorization']
                        resolve(resp)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        delete_user({ commit, state, token, dispatch }) {
            const auth_token = localStorage.getItem('token', token)
            return new Promise((resolve, reject) => {
                if (confirm("Are you sure you want to delete the account!"))
                    axios({
                        url: '/accounts/' + state.token.id,
                        data: token,
                        headers: { Authorization: 'Token ' + auth_token },
                        method: 'DELETE'
                    }
                    )
                        .then(resp => {
                            commit('DELETE_USER')
                            commit('LOGOUT')
                            const token = resp.data.token
                            localStorage.removeItem('token', token)
                            dispatch('logout')
                            resolve(resp)
                        })
                        .catch(err => {
                            console.log(auth_token);
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
    },
    plugins: [vuexLocal.plugin]
})

export default store

