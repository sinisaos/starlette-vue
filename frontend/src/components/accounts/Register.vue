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
                    <h1>Register</h1>
                    <br />
                    <b-form @submit.prevent="register" class="w-100">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input
                                type="text"
                                v-model="username"
                                id="username"
                                name="username"
                                class="form-control"
                                :class="{ 'is-invalid': v$.username.$error }"
                            />
                            <div
                                v-if="!v$.username.required"
                                class="invalid-feedback"
                            >
                                Username is required
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="email">Email</label>
                            <input
                                type="email"
                                v-model="email"
                                id="email"
                                name="email"
                                class="form-control"
                                :class="{ 'is-invalid': v$.email.$error }"
                            />
                            <div
                                v-if="v$.email.$error"
                                class="invalid-feedback"
                            >
                                <span v-if="!v$.email.required"
                                    >Email is required</span
                                >
                                <span v-if="!v$.email.email"
                                    >Email is invalid</span
                                >
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input
                                type="password"
                                v-model="password"
                                id="password"
                                name="password"
                                class="form-control"
                                :class="{ 'is-invalid': v$.password.$error }"
                            />
                            <div
                                v-if="v$.password.$error"
                                class="invalid-feedback"
                            >
                                <span v-if="!v$.password.required"
                                    >Password is required</span
                                >
                                <span v-if="!v$.password.minLength"
                                    >Password must be at least 4
                                    characters</span
                                >
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="passwordConfirmation"
                                >Confirm Password</label
                            >
                            <input
                                type="password"
                                v-model="passwordConfirmation"
                                id="passwordConfirmation"
                                name="passwordConfirmation"
                                class="form-control"
                                :class="{
                                    'is-invalid': v$.passwordConfirmation.$error
                                }"
                            />
                            <div
                                v-if="v$.passwordConfirmation.$error"
                                class="invalid-feedback"
                            >
                                <span v-if="!v$.passwordConfirmation.required"
                                    >Confirm Password is required</span
                                >
                                <span
                                    v-else-if="
                                        !v$.passwordConfirmation.sameAsPassword
                                    "
                                    >Passwords must match</span
                                >
                            </div>
                        </div>
                        <div class="form-group">
                            <button class="btn btn-primary">Register</button>
                        </div>
                    </b-form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core"
import { required, email, minLength, sameAs } from "@vuelidate/validators"
import { defineComponent } from "vue"

export default defineComponent({
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            username: "",
            email: "",
            password: "",
            passwordConfirmation: "",
            showDismissibleAlert: false,
            message: "",
            showMessage: false
        }
    },
    validations() {
        return {
            username: { required },
            email: { required, email },
            password: { required, minLength: minLength(8) },
            passwordConfirmation: {
                required,
                sameAsPassword: sameAs(this.password)
            }
        }
    },
    methods: {
        register() {
            let data = {
                username: this.username,
                email: this.email,
                password: this.password
            }
            this.v$.$touch()
            if (this.v$.$invalid) {
                return
            }
            this.$store
                .dispatch("register", data)
                .then(() => this.$router.push("/"))
                .catch((err) => {
                    this.message = err.response.data
                    this.showMessage = true
                    this.showDismissibleAlert = true
                })
        }
    }
})
</script>
