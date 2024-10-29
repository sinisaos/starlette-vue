<template>
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="list-group">
                    <router-link
                        :to="{ name: 'profile' }"
                        class="list-group-item list-group-item-action"
                        >Profile</router-link
                    >
                    <router-link
                        :to="{ name: 'profileQuestions' }"
                        class="list-group-item list-group-item-action"
                        >Questions</router-link
                    >
                    <router-link
                        :to="{ name: 'profileAnswers' }"
                        class="list-group-item list-group-item-action"
                        >Answers</router-link
                    >
                </div>
                <br />
                <br />
            </div>
            <div class="col-md-9">
                <paginate name="answers" :list="answers" tag="div">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Content</th>
                                    <th>Created</th>
                                    <th>Likes</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(item, index) in paginated(
                                        'answers'
                                    )"
                                    :key="index"
                                >
                                    <td>
                                        <p>
                                            {{ item.content.slice(0, 50) }}...
                                        </p>
                                    </td>
                                    <td>{{ formatDate(item.created) }}</td>
                                    <td>{{ item.answer_like }}</td>
                                    <td>
                                        <router-link
                                            :to="{
                                                name: 'profileAnswersEdit',
                                                params: {
                                                    id: item.id,
                                                    content: item.content
                                                }
                                            }"
                                            class="btn btn-info"
                                        >
                                            <i class="fa fa-edit"></i>
                                        </router-link>
                                        <button
                                            class="btn btn-danger"
                                            @click="answerDelete(item.id)"
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
                        for="answers"
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
            answers: [],
            paginate: ["answers"]
        }
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("dddd MMMM D, YYYY")
        },
        getAnswers() {
            const path = "/questions/user-answers/" + this.token
            axios
                .get(path)
                .then((res) => {
                    this.answers = res.data.answers
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        answerDelete(id) {
            const path = "/questions/answer/" + id
            axios
                .delete(path)
                .then((res) => {
                    this.answers = res.data
                    this.getAnswers()
                })
                .catch((error) => {
                    console.error(error)
                })
        }
    },
    created() {
        this.getAnswers()
    }
})
</script>

