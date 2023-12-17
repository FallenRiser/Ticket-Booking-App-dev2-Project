<template>
    <div class="container mt-5">
      <h2 class="mb-4" style="font-family: 'bluto'; color: #ffffff;">Edit Movie</h2>
      <div class="card" style="max-width: 1000px; margin: auto;">
        <div class="card-body">
      <form @submit.prevent="submitForm">
        <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
        <div class="card">
          <div class="card-body">
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <input type="text" class="form-control" id="title" v-model="title" required>
        </div>
        
        <div class="mb-3">
          <label for="boxart" class="form-label">Box Art Image</label>
          <input type="file" ref="boxart"  @change="onFileChange" accept="image/*">
        </div>
  
        <div class="mb-3">
          <label for="director" class="form-label">Director</label>
          <input type="text" class="form-control" id="director" v-model="director" required>
        </div>
  
        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea class="form-control" id="description" v-model="description" required></textarea>
        </div>

        <div class="mb-3">
          <label for="cast" class="form-label">Cast</label>
          <input type="text" class="form-control" id="cast" v-model="cast" required>
        </div>

        <div class="mb-3">
          <label for="duration" class="form-label">Duration</label>
          <input type="text" class="form-control" id="duration" v-model="duration" required>
        </div>

        <div class="mb-3">
          <label for="language" class="form-label">Language</label>
          <input type="text" class="form-control" id="language" v-model="language" required>
        </div>

        <div class="mb-3">
          <label for="rate" class="form-label">Base Rate</label>
          <input type="number" class="form-control" id="rate" v-model="rate" required>
        </div>

        <div class="mb-3">
          <label for="genre" class="form-label">Genre</label>
          <input type="text" class="form-control" id="genre" v-model="genre" required>
        </div>

        <div class="mb-3">
          <label for="startDate" class="form-label">Start Date</label>
          <input type="date" class="form-control" v-model="start_date">
        </div>

        <div class="mb-3">
          <label for="endDate" class="form-label">End Date</label>
          <input type="date" class="form-control" v-model="end_date">
        </div>
  
        <button type="submit" class="btn btn-primary mt-3">
          Save Changes
        </button>
      </div>
      </div>
    </div>
      </form>
    </div>
    </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        title: "",
        boxart: null,
        director: "",
        description: "",
        cast: "",
        duration: "",
        rate: "",
        language: "",
        genre: "",
        start_date: "",
        end_date: "",
      };
    },
  
    mounted() {
      this.fetchMovieDetails();
    },
  
    methods: {
      onFileChange(event) {
        this.boxart = event.target.files[0];
      },
      async fetchMovieDetails() {
        try {
          const movieId = this.$route.params.movieId;
  
          const userSession = JSON.parse(localStorage.getItem('userSession'));
          const jwtToken = userSession.token;
          const role = userSession.role;
  
          const response = await axios.get(`http://127.0.0.1:5000/api/movie/${movieId}`, {
            headers: {
              'Content-Type': 'application/JSON',
              'Authorization': `Bearer ${jwtToken}`,
              'Role': JSON.stringify(role),
            },
          });
  
            this.title = response.data.title;
            this.director = response.data.director;
            this.description = response.data.description;
            this.cast = response.data.cast;
            this.duration = response.data.duration;
            this.rate = response.data.rate;
            this.language = response.data.language;
            this.genre = response.data.genre;
            this.start_date = this.formatDate(response.data.start_date);
            this.end_date = this.formatDate(response.data.end_date);
            console.log(this.start_date, this.end_date)
        } catch (error) {
          console.error('Error fetching movie details:', error);
        }
      },
      async submitForm() {
  const formData = new FormData();
  formData.append('title', this.title);
  formData.append('director', this.director);
  formData.append('boxart', this.boxart);
  formData.append('description', this.description)
  formData.append('cast', this.cast)
  formData.append('duration', this.duration)
  formData.append('language', this.language)
  formData.append('rate', this.rate)
  formData.append('genre', this.genre)
  formData.append('start_date', this.start_date)
  formData.append('end_date', this.end_date)
  try {
    const userSession = JSON.parse(localStorage.getItem('userSession'));
    const jwtToken = userSession.token;
    const role = userSession.role;

    const movieId = this.$route.params.movieId;

    const response = await axios.put(`http://127.0.0.1:5000/api/movie/${movieId}`, formData, {
      headers: {
        'Authorization': `Bearer ${jwtToken}`,
        'Role': JSON.stringify(role),
      },
    });

    if (response.status === 200) {
      alert('Movie details updated successfully');
      this.$router.push({ name: 'all-movies' });
    } else {
      alert('Error updating movie details');
    }
  } catch (error) {
    alert('Error updating movie details:', error.response.data.message);
  }
},
/*       async submitForm() {
        const formData = new FormData();
        formData.append('title', this.title);
        formData.append('director', this.director);
        formData.append('boxart', this.boxart);
        formData.append('description', this.description)
        formData.append('cast', this.cast)
        formData.append('duration', this.duration)
        formData.append('language', this.language)
        formData.append('rate', this.rate)
        formData.append('genre', this.genre)
        formData.append('start_date', this.start_date)
        formData.append('end_date', this.end_date)
        try {
          const userSession = JSON.parse(localStorage.getItem('userSession'));
          const jwtToken = userSession.token;
          const role = userSession.role;
  
          const movieId = this.$route.params.movieId;
  
          const response = await axios.put(`http://127.0.0.1:5000/api/movie/${movieId}`, formData, {
            headers: {
              'Authorization': `Bearer ${jwtToken}`,
              'Role': JSON.stringify(role),
            },
          });
  
          if (response.status === 200) {
            alert('Movie details updated successfully');
            this.$router.push({ name: 'all-movies' });
          } else {
            alert('Error updating movie details');
          }
        } catch (error) {
          alert('Error updating movie details:', error.response.data.message);
        }
      }, */
      formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    },
  };
  </script>
  
  <style scoped>
  .card-body{
  /* font-family: 'playfair'; */
  font-family: 'bluto';
  color: #333;
  font-size: large;
}
  </style>
  