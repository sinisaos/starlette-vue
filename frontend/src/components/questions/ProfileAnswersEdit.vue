<template>
  <div>
    <div class="container">
      <div class="row">
        <div class="col-sm-6 offset-md-3">
          <b-alert v-model="showDismissibleAlert" variant="danger" dismissible>{{ message }}</b-alert>
          <h1>Edit answer</h1>
          <br />
          <b-form @submit.prevent="updateAnswer" class="w-100">
            <div class="form-group">
              <label for="content">Content</label>
              <b-form-textarea
                id="content"
                v-model="content"
                name="content"
                class="form-control"
                rows="5"
                max-rows="10"
                :class="{ 'is-invalid': $v.content.$error }"
              ></b-form-textarea>
              <div v-if="$v.content.$error" class="invalid-feedback">
                <span v-if="!$v.content.required">Content is required</span>
              </div>
            </div>
            <div class="form-group">
              <input type="hidden" name="user" class="form-control" :value="token" />
            </div>
            <div class="form-group">
              <button class="btn btn-primary">Submit</button>
            </div>
          </b-form>
        </div>
      </div>
    </div>
    <br />
    <hr />
    <footer class="container">
      <p>&copy; StarletteVue 2019</p>
    </footer>
  </div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import axios from "axios";

export default {
  data() {
    return {
      get token() {
        return localStorage.getItem("token") || 0;
      },
      content: this.$route.params.content,
      showDismissibleAlert: false,
      message: "",
      showMessage: false
    };
  },
  validations: {
    content: { required }
  },
  methods: {
    getQuestion() {
      const path =
        "http://localhost:8000/questions/" +
        this.$route.params.id +
        "/" +
        this.$route.params.slug;
      axios
        .get(path)
        .then(res => {
          this.answers = res.data.answers;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    updateAnswer() {
      let data = {
        content: this.content
      };
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      const path =
        "http://localhost:8000/questions/answer-edit/" + this.$route.params.id;
      axios
        .post(path, data)
        .then(res => {
          this.data = res.data;
          this.$router.push("/profile/" + this.token + "/answers");
        })
        .catch(err => {
          this.message = err.response.data;
          this.showMessage = true;
          this.showDismissibleAlert = true;
        });
    }
  }
};
</script>
