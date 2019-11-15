<template>
  <div class="container">
    <div class="col-md-8 offset-md-2" v-for="(item, index) in questions" :key="index">
      <h4>
        <router-link :to="{ name: 'question', params: { id: item.id, slug: item.slug }}">
          <b>{{ item.title }}</b>
        </router-link>
      </h4>
      <span>
        asked on
        <i>{{ item.created | dateFormat }}</i> by
        <b>{{ item.username }}</b>
        <b></b>
      </span>
      <hr />
      <p class="mb-1">{{ item.content }}</p>
      <br />
      <div class="btn-group" v-for="(tag,idx) in splitTags(item.tags)" :key="idx">
        <router-link
          :to="{ name: 'questionsByTag', params: { name: tag }}"
          tag="button"
          class="btn btn-primary"
        >{{ tag }}</router-link>
      </div>
      <br />
      <br />
      <i class="fa fa-eye" aria-hidden="true" title="Views">&ensp;{{ item.view }}</i>&ensp;
      <i
        class="fa fa-comment"
        aria-hidden="true"
        title="Answers"
      >&ensp;{{ item.answer_count }}</i>&ensp;
      <i
        class="fa fa-thumbs-up"
        aria-hidden="true"
        title="Likes"
      >&ensp;{{ item.question_like }}</i>
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
      questions: []
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
    getQuestions() {
      const path = "http://localhost:8000/questions";
      axios
        .get(path)
        .then(res => {
          this.questions = res.data.questions;
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
    this.getQuestions();
  }
};
</script>

<style lang="css" scoped>
.btn {
  margin-right: 5px;
}
</style>
