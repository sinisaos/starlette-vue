<template>
  <div class="container">
    <div class="col-md-8 offset-md-2" v-if="empty">
      <div class="form-group">
        <input type="text" v-model="search" class="form-control" placeholder="Search questions" />
        <i class="fa fa-search errspan" aria-hidden="true"></i>
      </div>
    </div>
    <div class="col-md-8 offset-md-2" v-if="!search">
      <button class="btn btn-link" @click="getQuestions">All questions</button>
      <button class="btn btn-link" @click="getQuestionsUnsolved">Unsolved</button>
      <button class="btn btn-link" @click="sortOldest">Oldest</button>
      <button class="btn btn-link" @click="sortNewest">Newest</button>
      <button class="btn btn-link" @click="sortMostViewed">Most viewed</button>
      <button class="btn btn-link" @click="sortMostLiked">Most popular</button>
    </div>
    <br />
    <div class="col-md-12" v-if="filterQuestions.length !== 0">
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
            <b>{{ item.user.username }}</b>
            <b></b>
          </span>
          <span
            v-if="item.accepted_answer"
            class="badge badge-badge-pill-lg badge-success float-right"
          >Solved</span>
          <hr />
          <p class="mb-1">{{ item.content }}</p>
          <br />
          <div class="btn-group" v-for="(tag,idx) in item.tags" :key="idx">
            <router-link
              :to="{ name: 'questionsByTag', params: { name: tag.name }}"
              tag="button"
              class="btn btn-primary"
            >{{ tag.name }}</router-link>
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
          <br />
          <hr />
        </div>
      </paginate>
      <div class="col-md-8 offset-md-2">
        <ul class="pagination float-right">
          <paginate-links for="questions" :async="true" :limit="2" :show-step-links="true"></paginate-links>
        </ul>
      </div>
    </div>
    <div class="col-md-8 offset-md-2" v-else>
      <h3>No results.</h3>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      empty: true,
      search: "",
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
  computed: {
    filterQuestions() {
      return this.questions.filter(question => {
        return (
          question.title.toLowerCase().includes(this.search.toLowerCase()) ||
          question.user.username
            .toLowerCase()
            .includes(this.search.toLowerCase()) ||
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
    getQuestionsUnsolved() {
      const path = "http://localhost:8000/questions/unsolved";
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
    },
    sortOldest() {
      this.questions.sort((a, b) => (a.id > b.id ? 1 : -1));
    },
    sortNewest() {
      this.questions.sort((a, b) => (a.id < b.id ? 1 : -1));
    },
    sortMostViewed() {
      this.questions.sort((a, b) => (a.view < b.view ? 1 : -1));
    },
    sortMostLiked() {
      this.questions.sort((a, b) =>
        a.question_like < b.question_like ? 1 : -1
      );
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

ul.paginate-links {
  border: 3.5px solid #ced4da;
  border-radius: 0.25rem;
}

ul.paginate-links > li.active > a {
  background-color: #ced4da;
  padding: 0.375rem 0.75rem;
  border-radius: 0.25rem;
  color: white;
  border: 1px solid #ced4da;
}
</style>
