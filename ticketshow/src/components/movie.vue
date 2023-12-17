<template>
    <div class="container">
      <div v-if="movie">
        <h1 style="font-family: 'bluto'; color: #ffffff;">{{ movie.title }}</h1>
        <img :src="`http://127.0.0.1:5000/static/img/Movies/${movie.boxart}`" :alt="movie.title">
        <br><br>
            <div  style="max-width: fit-content; margin: auto;" class="shadow p-3 mb-5 bg-body-tertiary rounded">
            <div class="card">
              
              <div class="card-body-in">
         <br>
        <p><strong>Director:</strong> {{ movie.director }} &nbsp;&nbsp;&nbsp; <strong>Cast:</strong> {{ movie.cast }} &nbsp;&nbsp;&nbsp;
          <strong>Duration:</strong> {{ movie.duration }}</p>
        <p><strong>Description:</strong> {{ movie.description }}</p>
        <p><strong>Language:</strong> {{ movie.language }} &nbsp;&nbsp;&nbsp; <strong>Base Price:</strong> {{ movie.rate }}₹
          &nbsp;&nbsp;&nbsp; <strong>Genre:</strong> {{ movie.genre }}</p>
        <p><strong>Start Date:</strong> {{ formatDate(movie.start_date) }} &nbsp;&nbsp;&nbsp;<strong>End Date:</strong> {{ formatDate(movie.end_date) }}
            &nbsp;&nbsp;&nbsp; <strong>Date Added:</strong> {{ formatDate(movie.date_added) }}</p>
            <div class = 'star-rating-container'>
            Average Rating :<star-rating 
              v-model="movie.rating"
              :star-size="20"
              :read-only="true"
              :increment="0.01"
              :rating="movie.rating"
            ></star-rating>
            </div>
            <br>
        <button class="btn btn-primary" @click="bookTickets(movie.id,movie.rate)">Book Tickets</button>
        <br><br>
      </div>
      
    </div>
  </div>
</div>  
      <div v-else>
        <p>Loading...</p>
      </div>
    </div>
  </template>
  
  <script>
  import StarRating from 'vue-star-rating';
  import axios from 'axios';
  
  export default {
    components: {
    StarRating,
  },
    data() {
      return {
        movie: null,
        title:"",
      };
    },
    async mounted() {
      await this.fetchMovieDetails();
    },
    methods: {
      async fetchMovieDetails() {
        try {
          const movieId = this.$route.params.id;
          console.log(movieId);
          const response = await axios.get(`http://127.0.0.1:5000/api/movie/${movieId}`);
          this.movie = response.data;
          this.title = response.data.title;
          console.log(this.movie);
        } catch (error) {
          console.log(error.response.data.message);
        }
      },
      bookTickets(id,fare) {
        console.log(fare);
        this.$router.push({ name: 'book_tickets', params: { movieID: id }, query: { moviefare: fare } });
      },
      formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    }
  };
  </script>
  
  <style scoped>
  .container {
  text-align: center;
  margin-top: 10px;
  }
  

.container img {
  max-width: 100%;
  height: 250px;
  object-fit: cover; 
  border: 2px solid #ffffff;
  border-radius: 10px;
}
.star-rating-container {
  display: flex;
  justify-content: center;
}

.card{
  max-width: fit-content;
  margin: auto;
  padding: 20px;
}

.card-body-in {
  background-color: #f5f5f5; /* Light background color for the card body */
  padding: 20px;
  border-radius: 8px;
  font-family: 'bluto';
  color: #333;
  font-size: large;
}
  </style>
  