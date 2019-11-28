<template>
  <div class="container">
    <div class="col-md-8 offset-md-2">
      <h4>Result(s) for tag: "{{ this.$route.params.name }}"</h4>
    </div>
    <br />
    <paginate name="questions" :list="questions" tag="div">
      <div
        class="col-md-8 offset-md-2"
        v-for="(item, index) in paginated('questions')"
        :key="index"
      >
        <h4>
          <router-link :to="{ name: 'question', params: { id: item.id, slug: item.slug }}">
            <b>{{ item.title }}</b>
          </router-link>
        </h4>
        <span>
          asked on
          <i>{{ item.created | dateFormat }}</i> by
          <b>{{ item.user.username }}</b>
          <b></b>
        </span>
        <hr />
      </div>
    </paginate>
    <div class="col-md-8 offset-md-2">
      <ul class="pagination">
        <paginate-links for="questions" :async="true" :limit="2" :show-step-links="true"></paginate-links>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      questions: [],
      paginate: ["questions"]
    };
  },
  filters: {
    dateFormat: function(value) {
      let date = new Date(value);
      return date.toString().slice(4, 24);
    }
  },
  methods: {
    getQuestions() {
      const path =
        "http://localhost:8000/questions/tags/" + this.$route.params.name;
      axios
        .get(path)
        .then(res => {
          this.questions = res.data.questions;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getQuestions();
  }
};
</script>

<style lang="css" scoped>
.btn {
  margin-right: 5px;
}
</style>
