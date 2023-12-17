<template>
    <div class="container">
      <div class="card booking-card">
        <div class="row g-0">
          <div class="col-md-3">
            <img :src="`http://127.0.0.1:5000/static/img/Movies/${movieBoxart}`" alt="Movie Boxart" class="movie-boxart">
          </div>
          <div class="col-md-9">
            <div class="card">
            <div class="card-body">
              <h3 class="card-title"><strong>{{ movieTitle }}</strong></h3>
              <p class="card-text">{{ theaterName }}</p>
              <p class="card-text" v-if="technology == 'None'">{{ `Screen ${screenNumber}` }}</p>
              <p class="card-text" v-else>{{ `Screen ${screenNumber} - ${technology}` }}</p>
              <p class="card-text">{{`Date: ${date} &nbsp;  Time: ${theaterTime} `}}</p>
              <div class="fare-counter">
                <label>Number of People:</label>
                <input type="number" v-model="numPeople">
                <p>{{ `Fare: ₹ ${fare}` }}</p>
              </div>
              <button class="btn btn-outline-danger btn-book" @click="confirmBooking">Book Tickets</button>
            </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        movieTitle: '',
        movieBoxart: '',
        theaterName: '',
        screenNumber: '',
        technology: '',
        theaterTime: '',
        numPeople: 1,
        fare: 0,
        date:'',
      };
    },
    mounted() {
      this.fetchMovieDetails();
    },
    methods: {
      async fetchMovieDetails() {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/movie/${this.$route.params.movieid}`);
          const movieData = response.data;
          console.log("movie id",this.$route.params.movieid);
          this.movieTitle = movieData.title;
          this.movieBoxart = movieData.boxart;
          this.screenNumber = this.$store.getters.selectedScreenNo
          this.technology = this.$store.getters.selectedScreenTech
          this.fare = this.$store.getters.selectedPrice
          this.theaterTime = this.$store.getters.selectedTheaterTime
          this.date = this.$store.getters.selectedDate
          console.log(this.theaterTime);
        } catch (error) {
          console.error('Error fetching movie details:', error);
        }
      },
      updateFare() {
        const price = this.$store.getters.selectedMoviePrice;
        this.fare = this.numPeople * price;
      },
      async confirmBooking() {
        const bookingData = {
          movieId: this.$route.params.movieid,
          theaterId: this.$store.getters.selectedTheaterId,
          screenId: this.$store.getters.selectedScreenId,
          numPeople: this.numPeople,
          fare: this.fare,
          time: this.theaterTime,
          date: this.date,
          user_id : this.$store.getters.user_id,
        };
        try {
          if(this.$store.getters.selectedAvailability >= this.numPeople) {
            const userSession = JSON.parse(localStorage.getItem('userSession'));
            const jwtToken = userSession.token;  
            const response = await axios.post('http://127.0.0.1:5000/api/booking', bookingData,{
                      headers: {
                          "Content-Type": "application/JSON",
                          'Authorization': `Bearer ${jwtToken}`
                      },
                      });
          
            console.log(response)
            alert('Booking Successful!');
        } 
        else{
          alert('Not Enough seats available')
        }
      }catch (error) {
          console.error('Error booking tickets:', error.response.data.message);
          alert('Booking Failed!');
        }
      },
    },
    watch: {
    numPeople(newValue){
        const price = this.$store.getters.selectedPrice;
        this.fare = newValue * price;

    },
  },
  };
  </script>
  
  <style scoped>

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
}
  
  .booking-card {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 20px;
    max-width: 600px;
  }
  
  .movie-boxart {
    width: 100%;
    border: 2px solid black;
    border-radius: 10px;
  }
  

  .fare-counter {
    margin-top: 10px;
  }
  
  .btn-book {
    margin-top: 20px;
  }

  .card-body{
  /* font-family: 'playfair'; */
  font-family: 'bluto';
  color: #333;
  font-size: large;
}
  </style>