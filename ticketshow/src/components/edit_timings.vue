<template>
    <div class="container mt-5">
      <h2 class="mb-4" style="font-family: 'bluto'; color: #ffffff;" >Movie Timings</h2>
      <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
      <div class="card">
          <div class="card-body">

         
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Theatre</th>
            <th>Screen No</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(timing, index) in movieTimings" :key="index">
            <td>{{ timing.id }}</td>
            <td>{{ timing.theatre }}</td>
            <td>{{ timing.screen_no }}</td>
            <td>
              <input type="date" v-model="timing.start_date" class="form-control" >
            </td>
            <td><input type="date" v-model="timing.end_date" class="form-control" ></td>
            <td>
              <input type="time" v-model="timing.start_time" class="form-control" >
            </td>
            <td><input type="time" v-model="timing.end_time" class="form-control" ></td>
            <td>
              <button class="btn btn-primary" style="margin:5px;" @click="submitTiming(timing.id, timing.start_date, timing.end_date, timing.start_time, timing.end_time)">
                Submit
              </button>
              <button class="btn btn-danger" style="margin:5px;" @click="deleteTiming(timing.id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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
      movieTimings: [],
      movieId: null,
    };
  },
  mounted() {
    this.movieId = this.$route.params.movieId;
    this.fetchMovieTimings();
  },
  methods: {
    async deleteTiming(id) {
      try {
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const role = userSession.role;
        const response = await axios.delete(`http://127.0.0.1:5000/api/movie/timings/${id}`,{
          headers: {
            'Content-Type': 'application/JSON',
            'Authorization': `Bearer ${jwtToken}`,
            'Role': JSON.stringify(role),
          }
        });

        if (response.status === 200) {
          alert('Movie timing deleted successfully');
          this.$router.push({ name: 'all-movies'});
        } else {
          alert('Error deleting movie timing');
        }
      } catch (error) {
        alert('Error deleting movie timing:', error.response.data.message);
      }
    },
    async fetchMovieTimings() {
      try {
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const role = userSession.role;
        const response = await axios.get(`http://127.0.0.1:5000/api/movie/${this.movieId}/timings`,{
          headers: {
            'Content-Type': 'application/JSON',
            'Authorization': `Bearer ${jwtToken}`,
            'Role': JSON.stringify(role),
          }
        });

        // Update the movieTimings array with the response data
        this.movieTimings = response.data;
        console.log("this.movieTimings: " + this.movieTimings);
      } catch (error) {
        console.error('Error fetching movie timings:', error);
      }
    },
    async submitTiming(id, start_date, end_date, start_time, end_time) {
      try {
        

  
        const updatedTimingData = {
          slot_id : id,
          start_date: start_date,
          end_date: end_date,
          start_time: start_time,
          end_time: end_time,
        };

        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const role = userSession.role;
        const response = await axios.put(`http://127.0.0.1:5000/api/movie/timings/${id}`, updatedTimingData,{
          headers: {
            'Content-Type': 'application/JSON',
            'Authorization': `Bearer ${jwtToken}`,
            'Role': JSON.stringify(role),
          }
        });

        if (response.status === 200) {
          alert('Movie timing updated successfully');
          console.log(response.data.message);
          // You can also update the local movieTimings array to reflect the changes immediately
           //this.movieTimings[index] = response.data;
        } else {
          alert('Error updating movie timing');
        }
      } catch (error) {
        alert('Error updating movie timing:', error.response.data.message);
      }
    },
  },
};
</script>
  