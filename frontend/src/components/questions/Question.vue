<template>
    <div class="container">
        <div class="col-md-8 offset-md-2">
            <h4>
                <b>{{ question.title }}</b>
            </h4>
            <span>
                asked on
                <i>{{ formatDate(question.created) }}</i> by
                <b>{{ question.user.username }}</b>
                <b></b>
            </span>
            <hr />
            <p class="mb-1">{{ question.content }}</p>
            <br />
            <div
                class="btn-group"
                v-for="(tag, idx) in question.tags"
                :key="idx"
            >
                <router-link
                    :to="{ name: 'questionsByTag', params: { name: tag.name } }"
                    class="btn btn-primary"
                    >{{ tag.name }}</router-link
                >
            </div>
            <router-link
                v-if="!isLoggedIn"
                to="/login"
                class="float-end"
                style="color:#33cc33cursor:pointer"
            >
                <i
                    class="fa fa-thumbs-up"
                    aria-hidden="true"
                    title="Question likes"
                    >&ensp;{{ question.question_like }}&ensp;</i
                >
            </router-link>
            <form
                method="POST"
                v-else
                @click="questionLike(question.id)"
                class="float-end"
                style="color:#33cc33 cursor:pointer"
            >
                <i
                    class="fa fa-thumbs-up"
                    aria-hidden="true"
                    title="Question likes"
                ></i>
                &ensp;{{ question.question_like }}&ensp;
            </form>
            <br />
            <hr />
        </div>
        <div class="col-md-8 offset-md-2">
            <span v-if="!isLoggedIn">*Must be logged in to post answer</span>
            <b-form @submit.prevent="create" v-else class="w-100">
                <div class="form-group">
                    <b-form-textarea
                        id="content"
                        v-model="content"
                        name="content"
                        class="form-control"
                        placeholder="Answer..."
                        rows="5"
                        max-rows="10"
                        :class="{ 'is-invalid': v$.content.$error }"
                    ></b-form-textarea>
                    <div v-if="v$.content.$error" class="invalid-feedback">
                        <span v-if="!v$.content.required"
                            >Content is required</span
                        >
                    </div>
                </div>
                <br />
                <div class="form-group">
                    <button class="btn btn-primary">Submit</button>
                </div>
            </b-form>
            <br />
            <br />
            <h3>{{ answerCount }} answer(s)</h3>
            <br />
            <hr />
            <div v-for="(item, index) in answers" :key="index">
                <span>
                    Answered on
                    <i>{{ formatDate(item.created) }}</i> by
                    <b>{{ item.ans_user.username }}</b>
                    <br />
                    <br />
                </span>
                <p class="mb-1">{{ item.content }}</p>
                <router-link
                    v-if="!isLoggedIn"
                    to="/login"
                    class="float-end"
                    style="color:#33cc33 cursor:pointer"
                >
                    <i
                        class="fa fa-thumbs-up"
                        aria-hidden="true"
                        title="Answer likes"
                        >&ensp;{{ item.answer_like }}&ensp;</i
                    >
                </router-link>
                <form
                    v-else
                    @click="answerLike(item.id)"
                    class="float-end"
                    style="color:#33cc33 cursor:pointer"
                >
                    <i
                        class="fa fa-thumbs-up"
                        aria-hidden="true"
                        title="Answer likes"
                    ></i>
                    &ensp;{{ item.answer_like }}&ensp;
                </form>
                <div>
                    <div
                        v-if="
                            token == question.user.username &&
                            question.accepted_answer == 0 &&
                            item.is_accepted_answer == 0
                        "
                    >
                        <form
                            @click="answerAccept(item.id)"
                            class="btn btn-success"
                        >
                            Accept Answer
                        </form>
                        <br />
                    </div>
                    <div
                        v-else-if="
                            question.user.username == token &&
                            item.is_accepted_answer == 1
                        "
                    >
                        <span class="badge rounded-pill bg-success"
                            >Accepted answer</span
                        >
                    </div>
                    <div v-else-if="item.is_accepted_answer == 1">
                        <span class="badge rounded-pill bg-success"
                            >Accepted answer</span
                        >
                    </div>
                    <div v-else></div>
                </div>
                <br />
                <hr />
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"
import dayjs from "dayjs"
import { mapGetters } from "vuex"
import { useVuelidate } from "@vuelidate/core"
import { required } from "@vuelidate/validators"
import { defineComponent } from "vue"

export default defineComponent({
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            content: "",
            answers: [],
            answerCount: "",
            question: {},
            get token() {
                return localStorage.getItem("token") || 0
            }
        }
    },
    validations() {
        return {
            content: { required }
        }
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("dddd MMMM D, YYYY")
        },
        getQuestion() {
            const path =
                "/questions/" +
                this.$route.params.id +
                "/" +
                this.$route.params.slug
            axios
                .get(path)
                .then((res) => {
                    this.question = res.data.question
                    this.answers = res.data.answers
                    this.answerCount = res.data.answer_count
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error)
                })
        },
        create() {
            let data = {
                id: this.qid,
                content: this.content
            }
            this.v$.$touch()
            if (this.v$.$invalid) {
                return
            }
            const path = "/questions/answer-create/" + this.question.id
            axios
                .post(path, data)
                .then((res) => {
                    this.getQuestion()
                    this.data = res.data
                    this.$router.push(
                        "/questions/" +
                            this.$route.params.id +
                            "/" +
                            this.$route.params.slug
                    )
                })
                .catch((err) => {
                    this.message = err.response.data
                    this.showMessage = true
                    this.showDismissibleAlert = true
                })
        },
        questionLike(id) {
            const path = "/questions/question-like/" + id
            axios.post(path).then((res) => {
                this.data = res.data
                this.getQuestion()
            })
        },
        answerLike(id) {
            const path = "/questions/answer-like/" + id
            axios.post(path).then((res) => {
                this.data = res.data
                this.getQuestion()
            })
        },
        answerAccept(id) {
            const path = "/questions/answer-accept/" + id
            axios.post(path).then((res) => {
                this.data = res.data
                this.getQuestion()
            })
        }
    },
    computed: {
        ...mapGetters(["isLoggedIn", "authUser"])
    },
    created() {
        this.getQuestion()
    }
})
</script>

<style scoped>
.btn-primary {
    margin-right: 5px;
}
</style>