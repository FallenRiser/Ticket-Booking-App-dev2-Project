<template>
    <div class="container mt-5">
      <h1 class="mb-4" style="font-family: 'bluto'; color: #ffffff;">Latest Movies</h1>
      <div v-for="movie in movies" :key="movie.id" class="card mb-3">
        <div class="row g-0">
          <div class="col-md-4">
            <img v-bind:src="getBoxArtUrl(movie.boxart)" class="img-fluid movie-thumbnail" alt="Movie Box Art">
          </div>
          <div class="col-md-8">
            <div class="card-body d-flex flex-column justify-content-between">
              <div class="card">
                <div class="card-body">
                <router-link :to="{ name: 'movie', params: { id: movie.id } }">
              <h3 class="card-title">{{ movie.title }}</h3>
            </router-link>
              <p class="card-text"><strong>Director:</strong> {{ movie.director }}</p>
              <p class="card-text"><strong>Description:</strong> {{ movie.description }}</p>
              <p class="card-text"><strong>Cast:</strong> {{ movie.cast }}</p>
              <p class="card-text"><strong>Duration:</strong> {{ movie.duration }}</p>
              <p class="card-text"><strong>Language:</strong> {{ movie.language }}</p>
              <p class="card-text"><strong>Rate:</strong> {{ movie.rate }} ₹</p>
              <p class="card-text"><strong>Genre:</strong> {{ movie.genre }}</p>
              <p class="card-text"><strong>Start Date:</strong> {{ formatDate(movie.start_date) }}</p>
              <p class="card-text"><strong>End Date:</strong> {{ formatDate(movie.end_date) }}</p>
            </div>
            </div>
            <div class="card-body" v-if="adminparts">
              <button style="margin:5px;" v-if="adminparts" class="btn btn-secondary" @click="editMovie(movie.id)">Edit Movie</button>
              <button style="margin:5px;" v-if="adminparts" class="btn btn-secondary" @click="addTimings(movie.id, movie.title)">Add Timings</button>
              <button style="margin:5px;" v-if="adminparts" class="btn btn-secondary" @click="editTimings(movie.id, movie.title)">Edit Timings</button>
              <button style="margin:5px;" v-if="adminparts" class="btn btn-danger" @click="deleteMovie(movie.id)">Delete Movie</button>
            </div>
          </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapGetters } from 'vuex';
  export default {
    computed: {
      ...mapGetters(['isAuthenticated', 'role', 'user_name', 'user_id']),
      adminparts(){
        return this.isAuthenticated && this.role === 'admin'; 
      },
    },
    data() {
      return {
        movies: [],
      };
    },

    mounted() {
    this.fetchLatestMovies();
  },

  methods: {
    async deleteTimings(movieId) {
      try {
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const role = userSession.role;

        const response = await axios.delete(`http://127.0.0.1:5000/api/movie/${movieId}/timings`, {
          headers: {
            'Content-Type': 'application/JSON',
            'Authorization': `Bearer ${jwtToken}`,
            'Role': JSON.stringify(role),
          },
        });

        if (response.status === 200) {
          console.log('Timings deleted successfully');
        } else {
          console.error('Error deleting timings');
        }
      } catch (error) {
        console.error('Error deleting timings:', error);
      }
    },
    async deleteMovie(movieId) {
      try {
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const role = userSession.role;
        const confirmed = window.confirm('Are you sure you want to delete this movie?');
        if (confirmed) {
        const response = await axios.delete(`http://127.0.0.1:5000/api/movie/${movieId}`, {
          headers: {
            'Content-Type': 'application/JSON',
            'Authorization': `Bearer ${jwtToken}`,
            'Role': JSON.stringify(role),
          },
        });

        if (response.status === 200) {
          this.movies = this.movies.filter((movie) => movie.id !== movieId);
          console.log('Movie deleted successfully');
        } else {
          console.error('Error deleting movie');
        }
      }
      } catch (error) {
        console.error('Error deleting movie:', error);
      }
    },
    editTimings(movieId, movieTitle) {
      this.$router.push({
        name: 'edit_timings',
        params: { movieId: movieId },
        query: { titlemovie: movieTitle },
      });
    },
    editMovie(movieId) {
      this.$router.push({ name: 'edit_movie', params: { movieId: movieId } });
    },
   async fetchLatestMovies() {
        try{
        const response = await axios.get('http://127.0.0.1:5000/api/add-movie',{
            headers: {
              'Content-Type': 'application/JSON', 
            },
          });


          this.movies = response.data;

        }
        catch (error) {
        console.error('Error fetching latest movies:', error);
        this.loading = false;
      }
    },
    getBoxArtUrl(boxart) {
        return `http://127.0.0.1:5000/static/img/Movies/${boxart}`;
      //return `./Server/static/img/Movies/${boxart}`;
    },
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    addTimings(id, title){
      console.log(title);
      this.$router.push({ name: 'add_timings', params: { movieID: id }, query: { titlemovie: title } });
    }
  },
};
</script>
<style scoped>
.movie-thumbnail {

  border: 1px solid black; 
  border-radius: 10px; 
  margin-top: 50px; 
  margin-bottom: 10px; 
  max-width: 100%;
  height: 250px; 
  object-fit: cover; 
}

.card-body{
  /* font-family: 'playfair'; */
  font-family: 'bluto';
  color: #333;
  font-size: large;
}
</style>



  