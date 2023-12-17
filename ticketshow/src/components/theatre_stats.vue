<template>
    <div>
      <img :src="graphImage" alt="Theatre Statistics Graph" />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        graphImage: "" 
      };
    },
    methods: {
      async fetchTheatreStatistics(theatreId) {
       const response = await axios.get(`http://127.0.0.1:5000/api/theatre-statistics/${theatreId}`)
            console.log(response.data)
            this.graphImage = 'http://127.0.0.1:5000/static/statistics.png';
      }
    },
    mounted() {
        const theatreId = this.$route.params.theatreId
      this.fetchTheatreStatistics(theatreId) 
    }
  };
  </script>