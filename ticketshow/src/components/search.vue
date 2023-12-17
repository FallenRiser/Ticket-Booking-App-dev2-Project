<template>
    <div class="container mt-5">
      <h2 class="mb-4" style=" font-family: 'bluto'; color: #ffffff;">Search</h2>
      <div class="input-group mb-3">
        <input v-model="searchQuery" class="form-control" type="text" placeholder="Search query" />
        <div class="input-group-append">
          <button class="btn btn-primary" @click="search">Search</button>
        </div>
      </div>
        <div class="row justify-content-center g-2" style=" font-family: 'bluto'; color: #ffffff;">
            <div class="form-check custom-radio">
    <input class="form-check-input" type="radio" id="searchMovie" value="movie" v-model="searchType">
    <label class="form-check-label custom-radio-label" for="searchMovie">Search Movies</label>
  </div>
  <div class="form-check custom-radio" style=" font-family: 'bluto'; color: #ffffff;">
    <input class="form-check-input" type="radio" id="searchTheatre" value="theatre" v-model="searchType">
    <label class="form-check-label custom-radio-label" for="searchTheatre">Search Theatres</label>
  </div>
</div>
      <div v-if="searchResults.length > 0" style=" font-family: 'bluto'; color: #ffffff;">
        <div class="card">
        <h4>Search Results:</h4>
        <div v-for="result in searchResults" :key="result.id" @click="navigateToResult(result)">
          <div class="card-body">
         <p> {{ result.name || result.title || result.cast}} - {{ result.city || result.director }}</p>
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
        searchQuery: '',
        searchType: '', // 'movie' or 'theatre'
        searchResults: [],
      };
    },
    methods: {
      async search() {
        if (!this.searchType) {
          alert('Please select a search type (movie or theatre)');
          return;
        }
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/search', {
            params: {
              type: this.searchType,
              q: this.searchQuery,
            },
          });
          this.searchResults = response.data;
        } catch (error) {
          console.error(error);
        }
      },
      navigateToResult(result) {
        if (this.searchType === 'movie') {
          this.$router.push(`/movie/${result.id}`);
        } else if (this.searchType === 'theatre') {
          this.$router.push(`/theatre/${result.id}`);
        }
      },
    },
  };
  </script>
  <style scoped>
.custom-radio {
  display: flex;
  align-items: center;
  margin-bottom: 10px; /* Adjust the spacing as needed */
}

.custom-radio-input {
  margin: 0;
}

.custom-radio-label {
  margin: 0;
}
  </style>
  