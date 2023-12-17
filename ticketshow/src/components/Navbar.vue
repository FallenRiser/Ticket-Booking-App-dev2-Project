<template>
  <nav class="navbar navbar-expand-lg" style="background-color: #020024; color: white;">
    <div class="container-fluid">
      <router-link to="/" style="color: yellow; font-family: 'showtime'; font-size: 25px" class="navbar-brand">Ticket_Show</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/all-movies" style="color: white;"  class="nav-link">All Movies</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/all-theatres" style="color: white;"  class="nav-link">All Theatres</router-link>
          </li>
          <li class="nav-item" v-if="!isAuthenticated">
            <router-link to="/login" style="color: white;" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item" v-if="adminparts">
            <router-link to="/add-theatre" style="color: white;" v-if="adminparts" class="nav-link">Add Theatre</router-link>
          </li>
          <li class="nav-item" v-if="adminparts">
            <router-link to="/add-movie" style="color: white;" v-if="adminparts" class="nav-link">Add Movie</router-link>
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <router-link to="/logout" style="color: white;" @click="handleLogout()" class="nav-link">Logout</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/search">
              <button class="btn btn-info"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
              <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
              </svg></button>
            </router-link>
          </li>  
        </ul>
      </div>
    

    <div v-if="isAuthenticated" class="navbar-item">
      <router-link :to="{ name: 'profile', params: {userid : user_id} }" class="nav-link">Hello, {{ user_name }}</router-link>
    </div>
  </div>
  </nav>
</template>
  
  <script>
  import { mapGetters, mapMutations } from 'vuex';
  export default {

    computed: {
      ...mapGetters(['isAuthenticated', 'role', 'user_name', 'user_id']),
      adminparts(){
        return this.isAuthenticated && this.role === 'admin'; 
      },
    },
    methods: {
      ...mapMutations(['logout']),
      handleLogout() {
        this.logout();
        this.$router.push({ name: 'register' });
      },
    },
  }
  </script>
  
  <style>
  nav {
  box-shadow: 0 2px 4px 0 rgba(0,0,0,.2);
}
  </style>