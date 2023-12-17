<template>
  <div>
    <div class="container">
      <div class="row justify-content-center g-2">
        <div class="centered-div">
          <h1 class="display-4" style="font-family: 'bluto'; color: #ffffff;">Book Tickets</h1>
          <div style="max-width: fit-content; margin: auto;" class="shadow p-3 mb-5 bg-body-tertiary rounded">
            <div class="card">
              <div class="card-body">
                <div class="input-group mb-3">
                  <label class="input-group-text">City</label>
                  <input
                    class="form-control"
                    type="City"
                    name="city"
                    placeholder="Enter your city name"
                    v-model="city"
                    required
                  />

                  <label class="input-group-text">Date</label>
                  <input
                    class="form-control"
                    type="date"
                    name="date"
                    placeholder="Enter the date you want tickets for"
                    v-model="date"
                    required
                  />

                  <button class="btn btn-secondary" @click="fetchBook()">Fetch</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div style="max-width: fit-content; margin: auto;" class="shadow p-3 mb-5 bg-body-tertiary rounded" v-if="theatresAndScreens">
          <div class="card" style="width: 629.67px; padding: 20px;">
            <div class="card-body" style="width: 588.08px; padding: 16px;">
              <div v-for="theatre in theatresAndScreens" :key="theatre.theater_id">
                <h3>{{ theatre.theater_name }} ({{ theatre.theatre_city }})</h3>
                <div v-for="screen in theatre.screens" :key="screen.screen_id">
                  <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
                    <div class="card-body">
                      <p>
                        Screen {{ screen.screen_number }} &nbsp;&nbsp;
                        {{ screen.start_time }} - {{ screen.end_time }} &nbsp;&nbsp;
                        {{ screen.technology }}
                      </p>
                      <p>
                        Available Capacity: {{ screen.available_capacity }} &nbsp;&nbsp;
                        Price: {{ calculatePrice(screen.premium) }} ₹ 
                      </p>
                      <button class="btn btn-outline-dark" @click="bookTicket(theatre.theater_id, screen.screen_id, theatre.theater_name, screen.start_time, screen.end_time, screen.premium, screen.screen_number, screen.technology,date, screen.available_capacity)">Book Tickets</button>
                    </div>
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
import { mapMutations } from 'vuex';
import axios from 'axios';
export default {
    data(){
        return {
            date: '',
            city: '',
            movieid:'',
            theatresAndScreens: null,
        }
    },
    methods: {
      ...mapMutations(['setSelectedTheaterId', 'setSelectedScreenId', 'setSelectedTheaterName', 
      'setSelectedTheaterTime','setSelectedPrice', 'setSelectedScreenNo','setSelectedScreenTech', 'setSelectedDate','setSelectedAvailability']),
      selectedTicket(theatreid, screenid, theatrename, theatretime, theatreprice,screenno, screentech,date, seats){
        this.setSelectedTheaterId(theatreid);
        this.setSelectedScreenId(screenid);
        this.setSelectedTheaterName(theatrename);
        this.setSelectedTheaterTime(theatretime);
        this.setSelectedPrice(theatreprice);
        this.setSelectedScreenNo(screenno);
        this.setSelectedScreenTech(screentech);
        this.setSelectedDate(date);
        this.setSelectedAvailability(seats);
       },

        async fetchBook() {
            const formData = new FormData();
            formData.append('date', this.date);
            formData.append('city', this.city);
            formData.append('movieid', this.$route.params.movieID)
            console.log(this.$route.params.movieID)


            try {
                const userSession = JSON.parse(localStorage.getItem('userSession'));
                const jwtToken = userSession.token;
                /* if(this.datecheck(this.date)){
                    const response = await axios.post(`http://127.0.0.1:5000/api/book-tickets/${this.$route.params.movieID}`, formData, {
                    headers: {
                        "Content-Type": "application/JSON",
                        'Authorization': `Bearer ${jwtToken}`
                    },
                     }); */
                     const response = await axios.post(`http://127.0.0.1:5000/api/book-tickets/${this.$route.params.movieID}`, formData, {
                    headers: {
                        "Content-Type": "application/JSON",
                        'Authorization': `Bearer ${jwtToken}`
                    },
                     });     
                    
                      
                alert('Theatre fetched successfully');
                console.log(this.response)
                this.theatresAndScreens = response.data;
                    
          //this.clearForm();
        } catch (error) {
          console.log(error.response.data.message);
          alert(error.response.data.message)
        }

        }, 
        
            datecheck(inputDate) {
            const date = new Date(inputDate);
            const today = new Date();
            return date >= today;
        },

        bookTicket(theatre_id,screen_id, theater_name, start_time, end_time, premium,screenno,screentech,date,seats) {
          var time = start_time + '-' + end_time 
          var price = this.calculatePrice(premium)
          var movieid = `${this.$route.params.movieID}`
          console.log("movie id:",movieid)
          this.selectedTicket(theatre_id, screen_id, theater_name, time, price, screenno,screentech,date,seats);
          this.$router.push({ name: "booking" , params: { movieid: movieid}});
        },

    calculatePrice(premium) {
      console.log(this.$route.query.moviefare)  
      console.log(premium)  
      console.log(typeof(parseInt(this.$route.query.moviefare,10)))  
      console.log(typeof(premium))
      var num1 = parseInt(this.$route.query.moviefare,10);
      var num2 = premium;

      var sum = num1 + num2;
      return sum;
  },

    },

}
</script>

<style scoped>
.container{
  margin-top: 80px;
}

.card-body{
  /* font-family: 'playfair'; */
  font-family: 'bluto';
  color: #333;
  font-size: large;
}

.card{
  max-width: fit-content;
  margin: auto;
  padding: 20px;
}

.centered-div {
  text-align: center;
  margin: auto;
}

</style>