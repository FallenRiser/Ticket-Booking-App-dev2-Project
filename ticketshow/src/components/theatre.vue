<template>
    <div class="container">
        <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
            <div class="card-body">

      <h2 style="font-family: 'bluto'; color;">{{ theatre.name }} ({{ theatre.city }})  &nbsp;&nbsp;&nbsp;&nbsp; <button v-if="adminparts" 
        class="btn btn-dark" @click="fetchAnalysisData()">Statistics</button> </h2>

        <p class="card-text">
          <ul class="list-group" style="font-family:'bluto'; color: #333; font-size: large;">
            <li v-for="screen in theatre.screens" :key="screen.id" class="list-group-item">
              <h6 class="mb-0"><strong>Screen {{ screen.number }}</strong></h6>
              <p class="mb-0"><strong>Technology:</strong> {{ screen.technology }}</p>
              <p class="mb-0"><strong>Seat Capacity:</strong> {{ screen.seat_capacity }}</p>
              <p class="mb-0"><strong>Premium:</strong> {{ screen.premium }}</p>
            </li>
          </ul>
        </p>
        
            </div>
        </div>

        <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
        <div v-if="timeSlots.length > 0" class="card-body" style="font-family:'bluto'; color: #333; font-size: large;">

        <div  v-for="timeSlot in timeSlots" :key="timeSlot.id">
          <h2><router-link :to="{name: 'movie', params: { id: timeSlot.movie_id }}">{{ timeSlot.title }}</router-link></h2>
          <p class="mb-0"><strong>Director:</strong> {{ timeSlot.director }} &nbsp;&nbsp; <strong>Cast:</strong> {{ timeSlot.cast }}</p>
          <p class="mb-0"><strong>Duration:</strong> {{ timeSlot.duration }}&nbsp;&nbsp; 
            <strong> Language:</strong> {{ timeSlot.language }} &nbsp;&nbsp; <strong>Rate:</strong> {{ timeSlot.rate }}₹</p>
          <p>Time: {{ timeSlot.start_time }} - {{ timeSlot.end_time }}</p>
        </div>
        </div>
        <div v-else class="card-body">
          <h2 style="font-family: 'bluto';">This Theatre is not currently screening any movies.</h2>
        </div>
        </div>
  
      <div class="analysis-graph">
        <canvas id="barplot"></canvas>
      </div>
      
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex';
  import axios from 'axios';
  
  export default {
    computed: {
      ...mapGetters(['isAuthenticated', 'role', 'user_name', 'user_id']),
      adminparts(){
        return this.isAuthenticated && this.role === 'admin'; 
      },
    },
    data() {
      return {
        theatre: {},
        timeSlots: {},
      };
    },
    async created() {
      try {
        const theatreId = this.$route.params.theatreId;
        const response = await axios.get(`http://127.0.0.1:5000/api/theatre/${theatreId}`);
        this.theatre = response.data;
        console.log(this.theatre);
  
        const timeSlotsResponse = await axios.get(`http://127.0.0.1:5000/api/moviefromtheatre/${theatreId}`);

        this.timeSlots = timeSlotsResponse.data
  
      } catch (error) {
        console.error(error);
      }
    },
    methods: {
      async fetchAnalysisData() {
        const theatreId = this.$route.params.theatreId;
        this.$router.push({ name: "theatre_stats" , params: { theatreId: theatreId}});     
      },
    },
  };
  </script>
  
  <style scoped>
    .container {
      margin-top: 50px;
    }
  </style>