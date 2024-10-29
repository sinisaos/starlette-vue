<template>
    <div class="container">
        <div class="col-md-8 offset-md-2" v-if="empty">
            <div class="form-group">
                <input
                    type="text"
                    v-model="search"
                    class="form-control"
                    placeholder="Search questions"
                />
            </div>
        </div>
        <div class="col-md-8 offset-md-2" v-if="!search">
            <button class="btn btn-link" @click="getQuestions">
                All questions
            </button>
            <button class="btn btn-link" @click="getQuestionsUnsolved">
                Open
            </button>
            <button class="btn btn-link" @click="getQuestionsSolved">
                Solved
            </button>
            <button class="btn btn-link" @click="sortOldest">Oldest</button>
            <button class="btn btn-link" @click="sortMostViewed">
                Most viewed
            </button>
            <button class="btn btn-link" @click="sortMostLiked">
                Most popular
            </button>
        </div>
        <br />
        <div class="col-md-12" v-if="filterQuestions.length !== 0">
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
                <p class="mb-1">{{ item.content }}</p>
                <br />
                <div
                    class="btn-group"
                    v-for="(tag, idx) in item.tags"
                    :key="idx"
                >
                    <router-link
                        :to="{
                            name: 'questionsByTag',
                            params: { name: tag.name }
                        }"
                        class="btn btn-primary"
                        >{{ tag.name }}</router-link
                    >
                </div>
                <span
                    v-if="item.accepted_answer"
                    class="badge rounded-pill bg-success float-end"
                    >Solved</span
                >
                <br />
                <br />
                <i class="fa fa-eye" aria-hidden="true" title="Views"
                    >&ensp;{{ item.view }}</i
                >&ensp;
                <i class="fa fa-comment" aria-hidden="true" title="Answers"
                    >&ensp;{{ item.answer_count }}</i
                >&ensp;
                <i class="fa fa-thumbs-up" aria-hidden="true" title="Likes"
                    >&ensp;{{ item.question_like }}</i
                >
                &ensp;
                <br />
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
            </div>
        </div>
        <div class="col-md-8 offset-md-2" v-else>
            <h3>No results.</h3>
        </div>
        <br />
    </div>
</template>

<script>
import axios from "axios"
import dayjs from "dayjs"
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            empty: true,
            search: "",
            questions: [],
            perPage: 5,
            currentPage: 1
        }
    },
    computed: {
        filterQuestions() {
            return this.questions.filter((question) => {
                return (
                    question.title
                        .toLowerCase()
                        .includes(this.search.toLowerCase()) ||
                    question.user.username
                        .toLowerCase()
                        .includes(this.search.toLowerCase()) ||
                    question.content
                        .toLowerCase()
                        .includes(this.search.toLowerCase())
                )
            })
        },
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
            const path = "/questions/"
            axios
                .get(path)
                .then((res) => {
                    this.questions = res.data.questions
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        getQuestionsUnsolved() {
            const path = "/questions/unsolved"
            axios
                .get(path)
                .then((res) => {
                    this.questions = res.data.questions
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        getQuestionsSolved() {
            const path = "/questions/solved"
            axios
                .get(path)
                .then((res) => {
                    this.questions = res.data.questions
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        splitTags(value) {
            return value.split(",")
        },
        sortOldest() {
            this.questions.sort((a, b) => (a.id > b.id ? 1 : -1))
        },
        sortMostViewed() {
            this.questions.sort((a, b) => (a.view < b.view ? 1 : -1))
        },
        sortMostLiked() {
            this.questions.sort((a, b) =>
                a.question_like < b.question_like ? 1 : -1
            )
        }
    },
    created() {
        this.getQuestions()
    }
})
</script>

<style>
.btn-primary {
    margin-right: 5px;
}

.pagination-container {
    display: flex;
    column-gap: 10px;
}

.paginate-buttons {
    height: 40px;
    width: 40px;
    border-radius: 20px;
    cursor: pointer;
    background-color: rgb(242, 242, 242);
    border: 1px solid rgb(217, 217, 217);
    color: black;
}

.paginate-buttons:hover {
    background-color: #d8d8d8;
}

.active-page {
    background-color: #3498db;
    border: 1px solid #3498db;
    color: white;
}

.active-page:hover {
    background-color: #2988c8;
}
</style>