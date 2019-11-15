<template>
  <div class="container">
    <div class="col-md-8 offset-md-2">
      <h4>
        <b>{{ question[0].title }}</b>
      </h4>
      <span>
        asked on
        <i>{{ question[0].created | dateFormat }}</i> by
        <b>{{ question[0].username }}</b>
        <b></b>
      </span>
      <hr />
      <p class="mb-1">{{ question[0].content }}</p>
      <br />
      <div class="btn-group" v-for="(tag,idx) in splitTags(question[0].tags)" :key="idx">
        <router-link
          :to="{ name: 'questionsByTag', params: { name: tag }}"
          tag="button"
          class="btn btn-primary"
        >{{ tag }}</router-link>
      </div>
      <br />
      <br />
      <i class="fa fa-eye" aria-hidden="true" title="Views">&ensp;{{ question[0].view }}</i>&ensp;
      <i
        class="fa fa-comment"
        aria-hidden="true"
        title="Answers"
      >&ensp;{{ question[0].answer_count }}</i>&ensp;
      <i
        class="fa fa-thumbs-up"
        aria-hidden="true"
        title="Likes"
      >&ensp;{{ question[0].question_like }}</i>
      &ensp;
      <hr />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      question: {}
    };
  },
  filters: {
    dateFormat: function(value) {
      let sec = value * 1000;
      let date = new Date(sec);
      return date.toString().slice(4, 24);
    }
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
          this.question = res.data.question;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    splitTags(value) {
      return value.split(",");
    }
  },
  created() {
    this.getQuestion();
  }
};
</script>

<style lang="css" scoped>
.btn {
  margin-right: 5px;
}
</style>
