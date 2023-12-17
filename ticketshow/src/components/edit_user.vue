<template>
  <div class="container mt-5">
    <h1 style="font-family: 'bluto'; color: #ffffff;">Edit Profile</h1>
    <div class="shadow p-3 mb-5 bg-body-tertiary rounded" style="width: 700px; margin: auto;">
    <div class="card">
      <div class="card-body">

        <form @submit.prevent="updateUser">
          <div class="form-group">
            <label for="name">Name:</label>
            <input v-model="name" type="text" class="form-control" id="name" required>
          </div>
          <div class="form-group">
            <label for="email">Email:</label>
            <input v-model="email" type="email" class="form-control" id="email" required>
          </div>
          <div class="form-group">
            <label for="password">New Password:</label>
            <input v-model="password" type="password" class="form-control" id="password">
          </div>
          <div class="form-group">
            <label for="password2">Confirm New Password:</label>
            <input v-model="password2" type="password" class="form-control" id="password2">
          </div>
          <br><br>
          <button type="submit" class="btn btn-primary">Update Profile</button>
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
      name: '',
      email: '',
      password: '',
      password2: ''
    };
  },
  async created() {
    try {
      const userSession = JSON.parse(localStorage.getItem('userSession'));
      const jwtToken = userSession.token;
      const userId = this.$store.getters.user_id;

      const response = await axios.get(`http://127.0.0.1:5000/api/user/${userId}`, {
        headers: {
          "Content-Type": "application/JSON",
          'Authorization': `Bearer ${jwtToken}`
        },
      });

      this.name = response.data.user_name;
      this.email = response.data.user_email;
      console.log(this.name, this.email);

    } catch (error) {
      console.log(error.response.data.message);
    }
  },
  methods: {
    async updateUser() {
      try {
        const userSession = JSON.parse(localStorage.getItem('userSession'));
        const jwtToken = userSession.token;
        const userId = this.$store.getters.user_id;

        const userData = {
          name: this.name,
          email: this.email,
          password: this.password,
          password2: this.password2
        };

        await axios.put(`http://127.0.0.1:5000/api/user/${userId}`, userData, {
          headers: {
            "Content-Type": "application/JSON",
            'Authorization': `Bearer ${jwtToken}`
          },
        });

        this.$router.push(`/profile/${userId}`);
        alert('please log out and login for changes to take effect')

      } catch (error) {
        console.log(error.response.data.message);
      }
    }
  }
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
