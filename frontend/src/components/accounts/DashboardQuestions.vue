<template>
  <div class="container">
    <div class="row">
      <div class="col-md-3">
        <div class="list-group">
          <router-link
            :to="{ name: 'dashboard'}"
            class="list-group-item list-group-item-action"
          >Users</router-link>
          <router-link
            :to="{ name: 'dashboardQuestions'}"
            class="list-group-item list-group-item-action"
          >Questions</router-link>
          <router-link
            :to="{ name: 'dashboardAnswers'}"
            class="list-group-item list-group-item-action"
          >Answers</router-link>
        </div>
        <br />
        <br />
      </div>
      <div class="col-md-9">
        <paginate name="questions" :list="questions" tag="div">
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Content</th>
                  <th>Created</th>
                  <th>Views</th>
                  <th>Likes</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in paginated('questions')" :key="index">
                  <td>{{ item.title }}</td>
                  <td>
                    <p>{{ item.content.slice(0,50) }}...</p>
                  </td>
                  <td>{{ item.created | dateFormat }}</td>
                  <td>{{ item.view }}</td>
                  <td>{{ item.question_like }}</td>
                  <td>
                    <router-link
                      :to="{ name: 'profileQuestionsEdit', params: { id: item.id, title:item.title, content:item.content}}"
                      class="btn btn-info"
                    >
                      <i class="fa fa-edit"></i>
                    </router-link>
                    <button class="btn btn-danger" @click="questionDelete(item.id, item.slug)">
                      <i class="fa fa-trash"></i>
                    </button>
                    <br />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </paginate>
        <ul class="pagination float-right">
          <paginate-links for="questions" :async="true" :limit="2" :show-step-links="true"></paginate-links>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      get token() {
        return localStorage.getItem("token") || 0;
      },
      title: "",
      content: "",
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
      const path = "/accounts/dashboard";
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
    questionDelete(id, slug) {
      const path = "/questions/" + id + "/" + slug;
      axios
        .delete(path)
        .then(res => {
          this.questions = res.data.questions;
          this.getQuestions();
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

<style lang="css">
.btn {
  margin-right: 5px;
}

.modal-backdrop.show {
  opacity: 0.8;
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
</style>
