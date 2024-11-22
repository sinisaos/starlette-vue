<template>
    <div>
        <div class="container">
            <div class="row">
                <div class="col-sm-6 offset-md-3">
                    <b-alert
                        v-model="showDismissibleAlert"
                        variant="danger"
                        dismissible
                        >{{ message }}</b-alert
                    >
                    <h1>Edit question</h1>
                    <br />
                    <form @submit.prevent="updateQuestion" class="w-100">
                        <div class="mb-3">
                            <label for="title">Title</label>
                            <input
                                type="text"
                                v-model="title"
                                id="title"
                                name="title"
                                class="form-control"
                                :class="{ 'is-invalid': v$.title.$error }"
                            />
                            <div
                                v-if="!v$.title.required"
                                class="invalid-feedback"
                            >
                                Title is required
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="content">Content</label>
                            <b-form-textarea
                                id="content"
                                v-model="content"
                                name="content"
                                class="form-control"
                                rows="5"
                                max-rows="10"
                                :class="{ 'is-invalid': v$.content.$error }"
                            ></b-form-textarea>
                            <div
                                v-if="v$.content.$error"
                                class="invalid-feedback"
                            >
                                <span v-if="!v$.content.required"
                                    >Content is required</span
                                >
                            </div>
                        </div>
                        <div class="mb-3">
                            <input
                                type="hidden"
                                name="user"
                                class="form-control"
                                :value="token"
                            />
                        </div>
                        <div class="mb-3">
                            <button class="btn btn-primary">Submit</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"
import { useVuelidate } from "@vuelidate/core"
import { required } from "@vuelidate/validators"
import { defineComponent } from "vue"

export default defineComponent({
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            get token() {
                return localStorage.getItem("token") || 0
            },
            title: this.$route.params.title,
            content: this.$route.params.content,
            showDismissibleAlert: false,
            message: "",
            showMessage: false
        }
    },
    validations() {
        return {
            title: { required },
            content: { required }
        }
    },
    methods: {
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
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        updateQuestion() {
            let data = {
                title: this.title,
                content: this.content
            }
            this.v$.$touch()
            if (this.v$.$invalid) {
                return
            }
            const path = "/questions/" + this.$route.params.id
            axios
                .put(path, data)
                .then((res) => {
                    this.data = res.data
                    this.$router.replace(
                        "/profile/" + this.token + "/questions"
                    )
                })
                .catch((err) => {
                    this.message = err.response.data
                    this.showMessage = true
                    this.showDismissibleAlert = true
                })
        }
    }
})
</script>
