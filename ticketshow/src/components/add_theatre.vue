<template>
  <div class="container mt-5">
    <h1 class="mb-4" style="font-family: 'bluto'; color: #ffffff;" >Add Theatre</h1>
    <div class="shadow p-3 mb-5 bg-body-tertiary rounded" style="width: 900px; margin: auto;">
      <div class="card">
        <div class="card-body">
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="theatreName" class="form-label">Theatre Name</label>
        <input type="text" class="form-control" id="theatreName" v-model="theatreName" required>
      </div>
      <div class="mb-3">
        <label for="city" class="form-label">City</label>
        <input type="text" class="form-control" id="city" v-model="city" required>
      </div>

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
      <button type="button" style="margin: 5px;" class="btn btn-primary mt-3" @click="addScreen">
        Add Screen
      </button>
      <button type="submit" style="margin: 5px;" class="btn btn-success mt-3">Save Theatre</button>
    </form>
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
    async submitForm() {
      try {
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const role = userSession.role;
        console.log(this.screens);
        const response = await axios.post('http://127.0.0.1:5000/api/theatre', {
          name: this.theatreName,
          city: this.city,
          screens: this.screens,
        }, {
          headers: {
            'Content-Type': 'application/JSON',
            'Authorization': `Bearer ${jwtToken}`,
            'Role': JSON.stringify(role),
          }
        })
        if (response.status >= 200 && response.status < 300) {
          this.success = true;
          this.msg = response.data.message;
          this.screens = [];
          alert(response.data.message);
        } else {
          this.error = true;
          alert(response.data.message);
          throw new Error(response.data.message)
        }
      } catch (error) {
        this.error = true;
        this.msg = error.response.data.error_description;
        console.log(error.response.data.error_description);
      }
    },
  },
}
</script>

<style scoped>
.container {
  margin-top: 80px;
}
.card-body{
  /* font-family: 'playfair'; */
  font-family: 'bluto';
  color: #333;
  font-size: large;
}
</style>
