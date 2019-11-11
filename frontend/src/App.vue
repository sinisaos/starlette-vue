<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="dark">
      <b-navbar-brand to="/">StarletteVue</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav></b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item to="/login" v-if="!authUser.username">Login</b-nav-item>
          <b-nav-item to="/register" v-if="!authUser.username">Register</b-nav-item>

          <b-nav-item-dropdown v-if="isLoggedIn && authUser.username" right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <em>Hello {{ authUser.username }}</em>
            </template>
            <!-- change this line to set another authUser.username as admin user -->
            <b-dropdown-item
              v-if="isLoggedIn && authUser.username == 'admin'"
              to="/dashboard"
            >Dashboard</b-dropdown-item>
            <!-- change this line to set another authUser.username as admin user -->
            <b-dropdown-item v-if="isLoggedIn && authUser.username != 'admin'" to="/profile">Profile</b-dropdown-item>
            <b-dropdown-item @click="logout">Logout</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["isLoggedIn", "authUser"])
  },
  methods: {
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/");
      });
    }
  }
};
</script>