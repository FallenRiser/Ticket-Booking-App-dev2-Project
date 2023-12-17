<template>
  <div class="container">
    <h1 style="font-family: 'bluto'; color: #ffffff;">Welcome to Ticket Show!</h1>
    <h2>Latest Movies</h2>
    <div class="movie-grid">
      <div v-for="movie in displayedMovies" :key="movie.id" class="movie-item">
        <router-link :to="`/movie/${movie.id}`">
          <img :src="`http://127.0.0.1:5000/static/img/Movies/${movie.boxart}`" :alt="movie.title">
          <p>{{ movie.title }}</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      movies: [],
      displayedMovies: []
    };
  },
  async mounted() {
    await this.fetchLatestMovies();
  },
  methods: {
    async fetchLatestMovies() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/movie-home');
        this.movies = response.data;
        this.displayedMovies = this.movies;
        console.log(this.displayedMovies)
      } catch (error) {
        console.error('Error fetching latest movies:', error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  font-family: 'bluto'; 
  color: #ffffff;
  text-align: center;
  margin-top: 10px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-gap: 20px;
  margin-bottom: 20px;
}

.movie-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.movie-item img {
  max-width: 100%;
  height: 250px; 
  object-fit: cover; 
  border: 2px solid rgba(255,255,255,0.8);
  border-radius: 10px;
  padding: 5px;
}

.movie-item a {
  margin-top: 10px;
  font-family: 'bluto'; 
  color: #00d4f0;
}
</style>

<style>
.container {
  font-family: 'bluto'; 
  color: #161a42;
}
body {  
  background: #161a42;
  font-family: 'bluto';
}
.card-body {
  font-family: 'bluto';
}
</style>