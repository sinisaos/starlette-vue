<template>
    <div class="container">
        <div class="col-md-8 offset-md-2">
            <h4>Result(s) for tag: "{{ this.$route.params.name }}"</h4>
        </div>
        <br />
        <div
            class="col-md-8 offset-md-2"
            v-for="(item, index) in displayedQuestions"
            :key="index"
        >
            <h4>
                <router-link
                    :to="{
                        name: 'question',
                        params: { id: item.id, slug: item.slug }
                    }"
                >
                    <b>{{ item.title }}</b>
                </router-link>
            </h4>
            <span>
                asked on
                <i>{{ formatDate(item.created) }}</i> by
                <b>{{ item.user.username }}</b>
                <b></b>
            </span>
            <hr />
        </div>
        <div class="col-md-8 offset-md-2">
            <ul class="pagination float-end">
                <vue-awesome-paginate
                    :total-items="questions.length"
                    :items-per-page="perPage"
                    :max-pages-shown="5"
                    v-model="currentPage"
                    :onclick="onClickHandler"
                />
            </ul>
            <br />
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
            questions: [],
            perPage: 5,
            currentPage: 1
        }
    },
    computed: {
        displayedQuestions() {
            const startIndex = this.currentPage * this.perPage - this.perPage
            const endIndex = startIndex + this.perPage
            return this.questions.slice(startIndex, endIndex)
        }
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("dddd MMMM D, YYYY")
        },
        getQuestions() {
            const path = "/questions/tags/" + this.$route.params.name
            axios
                .get(path)
                .then((res) => {
                    this.questions = res.data.questions
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

