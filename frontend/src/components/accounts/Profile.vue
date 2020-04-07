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
        <b-list-group>
          <b-list-group-item>
            <span class="float-left">
              <strong>Username</strong>
            </span>
            <span class="float-right">{{ authUser.username }}</span>
          </b-list-group-item>
          <b-list-group-item>
            <span class="float-left">
              <strong>Email</strong>
            </span>
            <span class="float-right">{{ authUser.email }}</span>
          </b-list-group-item>
          <b-list-group-item>
            <span class="float-left">
              <strong>Joined</strong>
            </span>
            <span class="float-right">{{ authUser.joined | dateFormat }}</span>
          </b-list-group-item>
          <b-list-group-item>
            <span class="float-left">
              <strong>
                Last
                login
              </strong>
            </span>
            <span class="float-right">{{ authUser.last_login | dateFormat }}</span>
          </b-list-group-item>
          <b-list-group-item>
            <span class="float-left">
              <strong>
                Login
                count
              </strong>
            </span>
            <span class="float-right">{{ authUser.login_count }}</span>
          </b-list-group-item>
        </b-list-group>
        <br />
        <button
          class="btn btn-danger float-right"
          v-if="authUser.login_count > 1"
          @click="delete_user(authUser.id)"
        >Delete account</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters(["authUser"])
  },
  filters: {
    dateFormat: function(value) {
      let date = new Date(value);
      return date.toString().slice(0, 24);
    }
  },
  methods: {
    delete_user: function() {
      this.$store.dispatch("delete_user").then(() => {
        this.$router.push("/");
      });
    }
  }
};
</script>