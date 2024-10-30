<template>
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="list-group">
                    <router-link
                        :to="{ name: 'dashboard' }"
                        class="list-group-item list-group-item-action"
                        >Users</router-link
                    >
                    <router-link
                        :to="{ name: 'dashboardQuestions' }"
                        class="list-group-item list-group-item-action"
                        >Questions</router-link
                    >
                    <router-link
                        :to="{ name: 'dashboardAnswers' }"
                        class="list-group-item list-group-item-action"
                        >Answers</router-link
                    >
                </div>
            </div>
            <div class="col-md-9">
                <paginate name="allUsers" :list="allUsers" tag="div">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Username</th>
                                    <th scope="col">Email</th>
                                    <th scope="col">Joined</th>
                                    <th scope="col">Last login</th>
                                    <th scope="col">Login count</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(user, index) in paginated(
                                        'allUsers'
                                    )"
                                    :key="index"
                                >
                                    <td>{{ user.username }}</td>
                                    <td>{{ user.email }}</td>
                                    <td>{{ formatDate(user.joined) }}</td>
                                    <td>{{ formatDate(user.last_login) }}</td>
                                    <td>{{ user.login_count }}</td>
                                    <td>
                                        <button
                                            class="btn btn-danger float-right"
                                            @click="userDelete(user.id)"
                                        >
                                            <i class="fa fa-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </paginate>
                <ul class="pagination float-right">
                    <paginate-links
                        for="allUsers"
                        :async="true"
                        :limit="2"
                        :show-step-links="true"
                    ></paginate-links>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"
import dayjs from "dayjs"
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            allUsers: [],
            paginate: ["allUsers"]
        }
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("dddd MMMM D, YYYY")
        },
        getUsers() {
            const path = "/"
            axios
                .get(path)
                .then((res) => {
                    this.allUsers = res.data.results
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        userDelete(id) {
            const path = "/accounts/" + id
            axios
                .delete(path)
                .then((res) => {
                    this.users = res.data
                    this.getUsers()
                })
                .catch((error) => {
                    console.error(error)
                })
        }
    },
    created() {
        this.getUsers()
    }
})
</script>
