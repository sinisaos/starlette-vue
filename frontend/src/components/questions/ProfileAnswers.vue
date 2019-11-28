<template>
  <div class="container">
    <div class="row">
      <div class="col-md-3">
        <div class="list-group">
          <router-link
            :to="{ name: 'profile'}"
            class="list-group-item list-group-item-action"
          >Profile</router-link>
          <router-link
            :to="{ name: 'profileQuestions'}"
            class="list-group-item list-group-item-action"
          >Questions</router-link>
          <router-link
            :to="{ name: 'profileAnswers'}"
            class="list-group-item list-group-item-action"
          >Answers</router-link>
        </div>
        <br />
        <br />
      </div>
      <div class="col-md-9">
        <paginate name="answers" :list="answers" tag="div">
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Content</th>
                  <th>Created</th>
                  <th>Likes</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in paginated('answers')" :key="index">
                  <td>
                    <p>{{ item.content.slice(0,50) }}...</p>
                  </td>
                  <td>{{ item.created | dateFormat }}</td>
                  <td>{{ item.answer_like }}</td>
                  <td>
                    <router-link
                      :to="{ name: 'profileAnswersEdit', params: { id: item.id, content:item.content}}"
                      class="btn btn-info"
                    >
                      <i class="fa fa-edit"></i>
                    </router-link>
                    <button class="btn btn-danger" @click="answerDelete(item.id)">
                      <i class="fa fa-trash"></i>
                    </button>
                    <br />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </paginate>
        <ul class="pagination">
          <paginate-links for="answers" :async="true" :limit="2" :show-step-links="true"></paginate-links>
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
      answers: [],
      paginate: ["answers"]
    };
  },
  filters: {
    dateFormat: function(value) {
      let date = new Date(value);
      return date.toString().slice(4, 24);
    }
  },
  methods: {
    getAnswers() {
      const path = "http://localhost:8000/questions/user-answers/" + this.token;
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
    answerDelete(id) {
      const path = "http://localhost:8000/questions/answer-delete/" + id;
      axios
        .get(path)
        .then(res => {
          this.answers = res.data;
          this.getAnswers();
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getAnswers();
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
