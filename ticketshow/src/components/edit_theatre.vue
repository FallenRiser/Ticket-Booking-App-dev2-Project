<template>
    <div class="container mt-5">
      <h2 class="mb-4" style="font-family: 'bluto'; color: #ffffff;" >Edit Theatre</h2>
      <form @submit.prevent="submitForm">
        <div class="card">
          <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
            <div class="card">
          <div class="card-body" style="padding: 20px">
        <div class="mb-3">
          <label for="theatreName" class="form-label">Theatre Name</label>
          <input type="text" class="form-control" id="theatreName" v-model="theatreName" required>
        </div>
        <div class="mb-3">
          <label for="city" class="form-label">City</label>
          <input type="text" class="form-control" id="city" v-model="city" required>
        </div>
      </div>
      </div>
      </div>
  

          <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
            <div class="card">
          <div class="card-body" style="padding: 20px">
        <h4 class="mt-4 mb-3">Screens</h4>
        <div v-for="(screen, index) in screens" :key="index">
          <div class="row mb-2">
            <div class="col">
              <label for="screenNumber" class="form-label">Screen Number</label>
              <input type="number" class="form-control" v-model="screen.screenNumber" required>
            </div>
            <div class="col">
              <label for="technology" class="form-label">Technology</label>
              <input type="text" class="form-control" v-model="screen.technology" required>
            </div>
            <div class="col">
              <label for="seatCapacity" class="form-label">Seat Capacity</label>
              <input type="number" class="form-control" v-model="screen.seatCapacity" required>
            </div>
            <div class="col">
              <label for="availableCapacity" class="form-label">Available Capacity</label>
              <input type="number" class="form-control" v-model="screen.availableCapacity" required>
            </div>
            <div class="col">
              <label for="premium" class="form-label">Premium</label>
              <input type="number" class="form-control" v-model="screen.premium">
            </div>
            <div class="col">
              <button type="button" class="btn btn-danger" @click="removeScreen(index)">
                Remove
              </button>
            </div>
          </div>
        </div>
        <button type="button" style="margin:5px;" class="btn btn-primary mt-3" @click="addScreen">
          Add Screen
        </button>
        <button type="submit" style="margin:5px;" class="btn btn-success mt-3">Save Theatre</button>
        </div>
        </div>
        </div>
      </div> 
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        theatreName: "",
        city: "",
        screens: [
          {
            screenNumber: null,
            technology: "",
            seatCapacity: null,
            premium: null,
          },
        ],
        msg: "",
        error: false,
        success: false,
      };
    },
    created() {
      const { theaterId } = this.$route.params;
      if (theaterId) {
        this.fetchTheaterData(theaterId);
      }
    },
    methods: {
      addScreen() {
        this.screens.push({
          screenNumber: null,
          technology: "",
          seatCapacity: null,
          premium: null,
        });
      },
      removeScreen(index) {
        this.screens.splice(index, 1);
      },
      async fetchTheaterData(theaterId) {
        try {
          const userSession = JSON.parse(localStorage.getItem('userSession'));
          const jwtToken = userSession.token;
          const role = userSession.role;
  
          const response = await axios.get(`http://127.0.0.1:5000/api/theatre/${theaterId}`, {
            headers: {
              'Content-Type': 'application/JSON',
              'Authorization': `Bearer ${jwtToken}`,
              'Role': JSON.stringify(role),
            },
          });
  
          if (response.status === 200) {
            console.log(response.data.name)
            this.theatreName = response.data.name;

            this.city = response.data.city;
            const transformedScreens = response.data.screens.map(screen => ({
            screenid: screen.id,
            screenNumber: screen.number,
            technology: screen.technology,
            seatCapacity: screen.seat_capacity,
            availableCapacity: screen.available_capacity,
            premium: screen.premium,
            }));
            this.screens = transformedScreens;

            console.log(this.theatreName, this.city, this.screens)
          } else {
            throw new Error(response.data.message);
          }
        } catch (error) {
          console.error(error.message);
        }
      },
      async submitForm() {
        try {
          const userSession = JSON.parse(localStorage.getItem('userSession'));
          const jwtToken = userSession.token;
          const role = userSession.role;
          const { theaterId } = this.$route.params;
  
          const response = await axios.put(`http://127.0.0.1:5000/api/theatre/${theaterId}`, {
            name: this.theatreName,
            id: theaterId,
            city: this.city,
            screens: this.screens,
          }, {
            headers: {
              'Content-Type': 'application/JSON',
              'Authorization': `Bearer ${jwtToken}`,
              'Role': JSON.stringify(role),
            }
          });
  
          if (response.status >= 200 && response.status < 300) {
            this.success = true;
            this.msg = response.data.message;
            this.screens = [];
            alert('theatre edited successfully');
          } else {
            this.error = true;
            throw new Error(response.data.error_description)
          }
        } catch (error) {
          this.error = true;
          this.msg = error.message;
          console.error(error.message);
        }
      },
    },
  }
  </script>
  
  <style scoped>
  .container {
    margin-top: 110px;
  }

  .card{
  margin: auto;
  padding: 20px;  
}

.card-body {
  background-color: #f5f5f5; /* Light background color for the card body */
  padding: 20px;
  border-radius: 8px;
  /* font-family: 'playfair'; */
  font-family: 'bluto';
  color: #333;
  font-size: large;
}

  </style>
  