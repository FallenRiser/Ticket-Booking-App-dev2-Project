<template>
  <div>
    <div class="container">
    <h1 style="font-family: 'bluto'; color: #ffffff;">Add Timings for Movie: {{ this.$route.query.titlemovie }}</h1>
    <form>
      <div class="shadow p-3 mb-5 bg-body-tertiary rounded" style="width:800px; margin: auto;">
      <div class="card">
        
        <div class="card-body" style="" >
          
    <div class="mb-3">
          <label for="start_date" class="form-label">Start Date</label>
          <input type="date" class="form-control" id="start_date" v-model="start_date" required>
    </div>

    <div class="mb-3">
          <label for="end_date" class="form-label">End Date</label>
          <input type="date" class="form-control" id="end_date" v-model="end_date" required>
    </div>

    <div class="mb-3">
          <label for="start_time" class="form-label">Start Time</label>
          <input type="time" class="form-control" id="start_time" v-model="start_time" required>
    </div>

    <div class="mb-3">
          <label for="end_time" class="form-label">End Time</label>
          <input type="time" class="form-control" id="end_time" v-model="end_time" required>
    </div>
    <button class="btn btn-primary" @click.prevent="availableTheatre(movieID)">Fetch Theatres</button>
  </div>
</div>
</div>



  <div v-if="this.theaters.length > 0" style="width: 800px; margin: auto;">
    <h2 class="mb-4" style="font-family: 'bluto'; color: #ffffff;" >Theaters and Screens</h2>
      <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
      <div v-for="theater in theaters" :key="theater.id" class="card mb-3">
        <div class="card-body">
        <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
          <h5 class="card-title">{{ theater.name }} ({{ theater.city }})</h5>
          <p class="card-text">
          <ul class="list-group">
            <li v-for="screen in theater.screens" :key="screen.id" class="list-group-item">
              <h6 class="mb-0"><strong>Screen {{ screen.number }}</strong></h6>
              <p class="mb-0"><strong>Technology:</strong> {{ screen.technology }}</p>
              <p class="mb-0"><strong>Seat Capacity:</strong> {{ screen.seat_capacity }}</p>
              <p class="mb-0"><strong>Premium:</strong> {{ screen.premium ? 'Yes' : 'No' }}</p>
              <input type="checkbox" v-model="screen.selected" :value="screen.id">
            </li>
          </ul>
        </p>
        </div>
        </div>
      </div>
    </div>
    <button class="btn btn-primary" @click.prevent="submitTimings()">Submit</button>
  </div>


    </form>
</div>
</div>
</template>

<script>
import axios from 'axios';
export default {
    props: ['movieID'],
    data(){
        return{
            start_time: '',
            end_time: '',
            start_date: '',
            end_date: '',
            theaters : [],
        }
    },
    methods: {
      async availableTheatre(id){
      const formData = new FormData();
        formData.append('start_date', this.start_date);
        formData.append('end_date', this.end_date);
        formData.append('start_time', this.start_time);
        formData.append('end_time', this.end_time)

        try {
          const userSession = JSON.parse(localStorage.getItem('userSession'));
          const jwtToken = userSession.token;
          const role = userSession.role;
          const response = await axios.post('http://127.0.0.1:5000/api/movie-timings', formData, {
            headers: {
              'Authorization': `Bearer ${jwtToken}`,
              'Role': JSON.stringify(role),
            },
          });
          console.log(response)
          console.log(id)

          this.theaters = response.data;
          
      }
      catch (error) {
          //console.error('Error adding movie:', error);
          alert(error.response.data.message)
        }
    },

    async submitTimings() {
      const selectedTheaters = this.theaters.filter(theater => theater.screens.some(screen => screen.selected));

      const theaterScreenDict = {};
      selectedTheaters.forEach(theater => {
        const selectedScreens = theater.screens.filter(screen => screen.selected);
        theaterScreenDict[theater.id] = selectedScreens.map(screen => screen.id);
      });

  const data = {
    movieID: this.movieID,
    start_date: this.start_date,
    end_date: this.end_date,
    start_time: this.start_time,
    end_time: this.end_time,
    theater_screen_dict: theaterScreenDict
  };
  console.log(data);

  try {

const userSession = JSON.parse(localStorage.getItem('userSession'));
const jwtToken = userSession.token;
const role = userSession.role;
const response = await axios.post('http://127.0.0.1:5000/api/add-time-slot', data, {
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${jwtToken}`,
    'Role': JSON.stringify(role),
  },
});

console.log(response.data.message);
alert(response.data.message)
} catch (error) {
console.log(error.response.data.message);
}
} 

},
};
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