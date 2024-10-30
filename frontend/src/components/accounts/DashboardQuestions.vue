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
                <br />
                <br />
            </div>
            <div class="col-md-9">
                <paginate name="questions" :list="questions" tag="div">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Title</th>
                                    <th>Content</th>
                                    <th>Created</th>
                                    <th>Views</th>
                                    <th>Likes</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(item, index) in paginated(
                                        'questions'
                                    )"
                                    :key="index"
                                >
                                    <td>{{ item.title }}</td>
                                    <td>
                                        <p>
                                            {{ item.content.slice(0, 50) }}...
                                        </p>
                                    </td>
                                    <td>{{ formatDate(item.created) }}</td>
                                    <td>{{ item.view }}</td>
                                    <td>{{ item.question_like }}</td>
                                    <td>
                                        <router-link
                                            :to="{
                                                name: 'profileQuestionsEdit',
                                                params: {
                                                    id: item.id,
                                                    title: item.title,
                                                    content: item.content
                                                }
                                            }"
                                            class="btn btn-info"
                                        >
                                            <i class="fa fa-edit"></i>
                                        </router-link>
                                        <button
                                            class="btn btn-danger"
                                            @click="
                                                questionDelete(
                                                    item.id,
                                                    item.slug
                                                )
                                            "
                                        >
                                            <i class="fa fa-trash"></i>
                                        </button>
                                        <br />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </paginate>
                <ul class="pagination float-right">
                    <paginate-links
                        for="questions"
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
            get token() {
                return localStorage.getItem("token") || 0
            },
            title: "",
            content: "",
            questions: [],
            paginate: ["questions"]
        }
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("dddd MMMM D, YYYY")
        },
        getQuestions() {
            const path = "/accounts/dashboard"
            axios
                .get(path)
                .then((res) => {
                    this.questions = res.data.questions
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        questionDelete(id, slug) {
            const path = "/questions/" + id + "/" + slug
            axios
                .delete(path)
                .then((res) => {
                    this.questions = res.data.questions
                    this.getQuestions()
                })
                .catch((error) => {
                    console.error(error)
                })
        }
    },
    created() {
        this.getQuestions()
    }
})
</script>
