<template>
    <div class="container mt-5">
      <h1 style="font-family: 'bluto'; color: #ffffff;">Profile Details</h1>
      <div class="shadow p-3 mb-5 bg-body-tertiary rounded" style="width: 900px; margin: auto;">
      <div class="card">
        <div class="card-body">
          
          <p><strong>Name:</strong> {{ user.user_name }}</p>
          <p><strong>Email:</strong> {{ user.user_email }}</p>
          <p><strong>Role:</strong> {{ this.role }}</p>
          <p><strong>Date Joined:</strong> {{ formatDate(user.user_date_joined) }}</p>
          <button style="margin:5px;" class="btn btn-primary" @click="editUser()">Edit</button>
          <button style="margin:5px;" class="btn btn-danger" @click="deleteUser()">Delete</button>
        </div>
      </div>
      </div>
  
      <div v-if="bookings.length > 0">
        <h1 style="font-family: 'bluto'; color: #ffffff;" >Bookings</h1>
        <div class="card"  style="width: 900px; margin: auto;">
        <div v-for="booking in bookings" :key="booking.id" >
          <div class="card-body">

            <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
              <div class="card">
                <div class="card-body">

            <p style="text-align: center;"><strong><h2>{{ booking.movie_name }}</h2></strong></p>
            <p><strong>Theater Name:</strong> {{ booking.theatre_name }} {{ booking.theatre_city }}</p>
            <p v-if="booking.screen_tech == 'None'"><strong>Screen Number:</strong> {{ booking.screen_number }} </p>
            <p v-else><strong>Screen Number:</strong> {{ booking.screen_number }} {{ booking.screen_tech }}</p>
            <p><strong>Date:</strong> {{ formatDate(booking.booking_date) }}</p>
            <p><strong>Time:</strong> {{ booking.booking_time }}</p>
            <p><strong>Tickets Booked:</strong> {{ booking.booked_tickets }}<strong> &nbsp; Amount:</strong> {{ booking.amount }}₹‎</p>
            <p><strong>Rate the Movie:</strong></p>
            <div class = 'star-rating-container'>
            <star-rating 
              v-model="booking.rating"
              :star-size="20"
              :read-only="false"
              :increment="1"
              :rating="  booking.rating "
              @update:rating ="setRating"
              @click="submitRating(booking)"
            ></star-rating>
          </div>
            </div>
            </div>
            </div>            
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapMutations } from 'vuex';
  import StarRating from 'vue-star-rating';
  export default {
    components: {
    StarRating,
  },
    data() {
      return {
        user: {},
        bookings: [],
        role: null,
        Rating: null,
      };
    },
    async created() {
      try {
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const userId = this.$store.getters.user_id; 
        const response = await axios.get(`http://127.0.0.1:5000/api/user/${userId}`,{
          headers: {
                        "Content-Type": "application/JSON",
                        'Authorization': `Bearer ${jwtToken}`
                    },
        });
        this.user = response.data;
        this.role = response.data.user_role[0];
        console.log(this.user);
        
        const bookingsResponse = await axios.get(`http://127.0.0.1:5000/api/user/${userId}/bookings`,{
          headers: {
                        "Content-Type": "application/JSON",
                        'Authorization': `Bearer ${jwtToken}`
                    },
        });
        this.bookings = bookingsResponse.data;
        console.log(this.bookings);
      } catch (error) {
        console.log(error.response.data.message);
        console.log(error.bookingsResponse.data.message);
      }
    },
    methods: {
      ...mapMutations(['logout']),
      handleLogout() {
        this.logout();
        this.$router.push({ name: 'register' });
      },

      setRating(rating){
      this.Rating= rating;
      console.log(this.Rating);
      },

      formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },

      async deleteUser(){
      try{
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const userId = this.$store.getters.user_id; 
        const confirmed = window.confirm('Are you sure you want to delete your account?');
        if (confirmed){
        const response = await axios.delete(`http://127.0.0.1:5000/api/user/${userId}`,{
          headers: {
                        "Content-Type": "application/JSON",
                        'Authorization': `Bearer ${jwtToken}`
                    },
        });
        console.log(response.data.message);
        this.handleLogout();
        this.$router.push('/');
      }
    }
      catch (error) {
        console.log(error.response.data.message); 
      }
    },

    editUser() {
      const userid = this.$store.getters.user_id; 
      this.$router.push(`/edit-profile/${userid}`);
    },

    async submitRating(booking) {
      try {
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        console.log(booking.movie_id)
        const ratingData = {
          user_id: this.$store.getters.user_id,
          movie_id: booking.movie_id, 
          rating: this.Rating,
        };

        const response = await axios.put('http://127.0.0.1:5000/api/add-movie', ratingData, {
          headers: {
            'Content-Type': 'application/JSON',
            Authorization: `Bearer ${jwtToken}`,
          },
        });

        console.log(response.data.message);
      } catch (error) {
        console.log(error.response.data.message);
      }
    },

    },
  };
  </script>
  
  <style scoped>
  .star-rating-container {
  display: flex;
  justify-content: center;
}

.card-body{
  /* font-family: 'playfair'; */
  font-family: 'bluto';
  color: #333;
  font-size: large;
}

  </style>