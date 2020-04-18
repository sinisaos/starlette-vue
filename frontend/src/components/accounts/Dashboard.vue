<template>
  <div class="container">
    <div class="col-md-12">
      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Joined</th>
              <th scope="col">Last login</th>
              <th scope="col">Login count</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in allUsers" :key="index">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.joined | dateFormat }}</td>
              <td>{{ user.last_login | dateFormat}}</td>
              <td>{{ user.login_count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["allUsers"])
  },
  // format date
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
