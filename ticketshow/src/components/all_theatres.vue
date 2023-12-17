<template>
    <div class="container mt-5">
      <h2 class="mb-4" style="font-family: 'bluto'; color: #ffffff;" >Theaters and Screens</h2>
      <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
      <div v-for="theater in theaters" :key="theater.id" class="card mb-3">
        <div class="card-body">
        <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
          <router-link :to="{ name: 'theatre', params: { theatreId: theater.id } }">
          <h3 class="card-title">{{ theater.name }} ({{ theater.city }})</h3>
          </router-link>
          <button style="margin:5px;" v-if="adminparts" class="btn btn-primary" @click="editTheater(theater.id)">
          Edit
        </button>
        <button style="margin:5px;" v-if="adminparts" class="btn btn-danger ml-2" @click="removeTheater(theater.id)">
          Remove
        </button>
        <button style="margin:5px;" v-if="adminparts" class="btn btn-secondary ml-2" @click="exportTheatre(theater.id)">
              Export
        </button>
          <p class="card-text">
          <ul class="list-group">
            <li v-for="screen in theater.screens" :key="screen.id" class="list-group-item">
              <h6 class="mb-0"><strong>Screen {{ screen.number }}</strong></h6>
              <p class="mb-0"><strong>Technology:</strong> {{ screen.technology }}</p>
              <p class="mb-0"><strong>Seat Capacity:</strong> {{ screen.seat_capacity }}</p>
              <p class="mb-0"><strong>Premium:</strong> {{ screen.premium }}</p>
            </li>
          </ul>
        </p>
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
        theaters: [],
      };
    },
  
    mounted() {
      this.fetchTheaters();
    },
  
    methods: {
        
        async exportTheatre(theaterId) {
        var theatre_id = theaterId
        var user_id = this.$store.getters.user_id
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;


        const response = await axios.get(`http://127.0.0.1:5000/api/${user_id}/export-csv/${theatre_id}`,{
          headers: {
                        "Content-Type": "application/JSON",
                        'Authorization': `Bearer ${jwtToken}`
                    },
        })
        console.log(response.data)
        alert('export job initiated')
        
        },

        editTheater(theaterId) {
        this.$router.push(`/edit-theater/${theaterId}`);
        },

        async removeTheater(theaterId) {
          try {
            const userSession = JSON.parse(localStorage.getItem('userSession'));
            const jwtToken = userSession.token;
            const role = userSession.role;
            const confirmed = window.confirm('Are you sure you want to delete this theatre?');
            if (confirmed) {
            const response = await axios.delete(`http://127.0.0.1:5000/api/theatre/${theaterId}`, {
              headers: {
                'Content-Type': 'application/JSON',
                'Authorization': `Bearer ${jwtToken}`,
                'Role': JSON.stringify(role),
              },
            });

            if (response.status >= 200 && response.status < 300) {
              this.theaters = this.theaters.filter(theater => theater.id !== theaterId);
            } else {
              throw new Error(response.data.error_description);
            }
          }
          } catch (error) {
            console.error(error.response.data.error_description);
          }
        },

        async fetchTheaters() {
        try{
        const response = await axios.get('http://127.0.0.1:5000/api/theatre',{
            headers: {
              'Content-Type': 'application/JSON', 
            },
          });


          this.theaters = response.data;
      } catch (error) {
        console.error(error.response.data.message);
      }
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