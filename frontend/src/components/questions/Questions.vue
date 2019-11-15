<template>
  <div class="container">
    <div class="col-md-8 offset-md-2">
      <div class="form-group">
        <input type="text" v-model="search" class="form-control" placeholder="Search questions" />
        <i class="fa fa-search errspan" aria-hidden="true"></i>
      </div>
    </div>
    <br />
    <paginate name="questions" :list="filterQuestions" tag="div">
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
      search: "",
      questions: [],
      paginate: ["questions"]
    };
  },
  filters: {
    dateFormat: function(value) {
      let sec = value * 1000;
      let date = new Date(sec);
      return date.toString().slice(4, 24);
    }
  },
  computed: {
    filterQuestions() {
      return this.questions.filter(question => {
        return (
          question.title.toLowerCase().includes(this.search.toLowerCase()) ||
          question.username.toLowerCase().includes(this.search.toLowerCase()) ||
          question.tags.toLowerCase().includes(this.search.toLowerCase()) ||
          question.content.toLowerCase().includes(this.search.toLowerCase())
        );
      });
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

<style lang="css">
.btn {
  margin-right: 5px;
}

.errspan {
  float: right;
  margin-right: 12px;
  margin-top: -27px;
  position: relative;
  z-index: 2;
}

ul {
  list-style-type: none;
  padding: 0;
  cursor: pointer;
  border: 1px black;
}

li {
  display: inline-block;
  margin: 0 10px;
}

ul.paginate-links > li.active > a {
  background-color: #007bff;
  padding: 0.375rem 0.75rem;
  border-radius: 0.25rem;
  color: white;
}
</style>
