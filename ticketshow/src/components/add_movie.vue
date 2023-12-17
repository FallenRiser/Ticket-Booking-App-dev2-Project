<template>
    <div class="container mt-5">
      <h1 class="mb-4" style="font-family: 'bluto'; color: #ffffff;">Add Movie</h1>
      <div class="shadow p-3 mb-5 bg-body-tertiary rounded" style="width: 1000px; margin: auto;">
    <div class="card">
      <div class="card-body">
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <input type="text" class="form-control" id="title" v-model="title" required>
        </div>
  
        <div class="mb-3">
          <label for="boxart" class="form-label">Box Art Image &nbsp;</label>
          <input type="file" ref="boxart" @change="onFileChange" accept="image/*">
        </div>
  
        <div class="mb-3">
          <label for="director" class="form-label">Director</label>
          <input type="text" class="form-control" id="director" v-model="director" required>
        </div>
  
        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea class="form-control" id="description" v-model="description" required></textarea>
        </div>

        <div class="mb-3">
          <label for="cast" class="form-label">Cast</label>
          <input type="text" class="form-control" id="cast" v-model="cast" required>
        </div>

        <div class="mb-3">
          <label for="duration" class="form-label">Duration</label>
          <input type="text" class="form-control" id="duration" v-model="duration" required>
        </div>

        <div class="mb-3">
          <label for="language" class="form-label">Language</label>
          <input type="text" class="form-control" id="language" v-model="language" required>
        </div>

        <div class="mb-3">
          <label for="rate" class="form-label">Base Rate</label>
          <input type="number" class="form-control" id="rate" v-model="rate" required>
        </div>

        <div class="mb-3">
          <label for="genre" class="form-label">Genre</label>
          <input type="text" class="form-control" id="genre" v-model="genre" required>
        </div>

        <div class="mb-3">
          <label for="startDate" class="form-label">Start Date</label>
          <input type="date" class="form-control" v-model="start_date" required>
        </div>

        <div class="mb-3">
          <label for="endDate" class="form-label">End Date</label>
          <input type="date" class="form-control" v-model="end_date" required>
        </div>

      <button type="submit" class="btn btn-primary mt-3">
        Add Movie
      </button>
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
        title: "",
        boxart: null,
        director: "",
        description: "",
        cast: "",
        duration: "",
        rate: "",
        language: "",
        genre: "",
        start_date: "",
        end_date: "",
      };
    },

 methods: {

      onFileChange(event) {
        this.boxart = event.target.files[0];
      },


      async submitForm() {

        const formData = new FormData();
        formData.append('title', this.title);
        formData.append('director', this.director);
        formData.append('boxart', this.boxart);
        formData.append('description', this.description)
        formData.append('cast', this.cast)
        formData.append('duration', this.duration)
        formData.append('language', this.language)
        formData.append('rate', this.rate)
        formData.append('genre', this.genre)
        formData.append('start_date', this.start_date)
        formData.append('end_date', this.end_date)

  
        try {
          const userSession = JSON.parse(localStorage.getItem('userSession'));
          const jwtToken = userSession.token;
          const role = userSession.role;
          const response = await axios.post('http://127.0.0.1:5000/api/add-movie', formData, {
            headers: {
              'Authorization': `Bearer ${jwtToken}`,
              'Role': JSON.stringify(role),
            },
          });
  
          alert(response.data.message);
          console.log(response);
          //this.clearForm();
        } catch (error) {
          alert(error.response.data.message);
        }
      },
      clearForm() {
        this.title = "";
        this.boxart = null;
        this.director = "";
        
        this.selectedTheater = null;
        this.selectedScreen = null;
        
        this.boxart.value = null;
      },
    },
  };
 </script> 

 <style scoped>
 .card-body{
 /*  font-family: 'playfair'; */
  font-family: 'bluto';
  color: #333;
  font-size: large;
}
</style>
  