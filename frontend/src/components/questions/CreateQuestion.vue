<template>
  <div>
    <div class="container">
      <div class="row">
        <div class="col-sm-6 offset-md-3">
          <b-alert v-model="showDismissibleAlert" variant="danger" dismissible>{{ message }}</b-alert>
          <h1>Create question</h1>
          <br />
          <b-form @submit.prevent="createQuestion" class="w-100">
            <div class="form-group">
              <label for="title">Title</label>
              <input
                type="text"
                v-model="title"
                id="title"
                name="title"
                class="form-control"
                :class="{ 'is-invalid': $v.title.$error }"
              />
              <div v-if="!$v.title.required" class="invalid-feedback">Title is required</div>
            </div>
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
              <label for="tags">Tags</label>
              <input
                type="text"
                v-model="tags"
                id="tags"
                name="tags"
                class="form-control"
                :class="{ 'is-invalid': $v.tags.$error }"
              />
              <div v-if="$v.tags.$error" class="invalid-feedback">
                <span v-if="!$v.tags.required">Tags is required</span>
              </div>
            </div>
            <div class="form-group">
              <input type="hidden" name="user" class="form-control" :value="authUser.username" />
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
import { mapGetters } from "vuex";
import axios from "axios";

export default {
  data() {
    return {
      title: "",
      content: "",
      tags: "",
      showDismissibleAlert: false,
      message: "",
      showMessage: false
    };
  },
  validations: {
    title: { required },
    content: { required },
    tags: { required }
  },
  computed: {
    ...mapGetters(["isLoggedIn", "authUser"])
  },
  methods: {
    createQuestion() {
      let data = {
        title: this.title,
        content: this.content,
        tags: this.tags
      };
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      const path = "/questions/create";
      axios
        .post(path, data)
        .then(res => {
          this.data = res.data;
          // eslint-disable-next-line
          console.log(res.data);
          this.$router.push("/questions");
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
