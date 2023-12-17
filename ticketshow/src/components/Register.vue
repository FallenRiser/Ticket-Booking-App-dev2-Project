import { mapMutations } from 'vuex';

<template>
  <div class="container">
    <div class="row justify-content-center g-2">
      <h1 style="font-family: 'bluto'; color: #ffffff;" class="display-4" v-if="register">Sign up</h1>
      <h1 style="font-family: 'bluto'; color: #ffffff;" class="display-4" v-else>Log in</h1>
  
      <div class="col-12 col-sm-4 col-md-8 align-self-center ">
  
        <div class="shadow p-3 mb-5 bg-body-tertiary rounded">

  
          <div class="card">
  
            <div class="card-body">
              
                <div class="input-group mb-3" v-if="register">
                  <input
                    class="form-control"
                    type="name"
                    name="name"
                    placeholder="Username"
                    v-model="form.name"
                    required
                  />
                </div>
                <div class="mb-3">
                  <input
                    class="form-control"
                    type="email"
                    name="email"
                    placeholder="Email"
                    v-model="form.email"
                    required
                    minlength="5"
                  />
                </div>
                <div class="input-group mb-3">
                  <input 
                    class="form-control"
                    type="password"
                    name="password"
                    placeholder="Password"
                    v-model="form.password"
                    required
                    minlength="8"
                  />

                  <div class="input-group-append">
                        <button class="btn btn-outline-secondary" type="button" data-toggle="tooltip" data-placement="right" title="Password needs to be atleast 8 characters long, 1 lowercase, 1 uppercase, 1 number and 1 special character." >
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-question-lg" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M4.475 5.458c-.284 0-.514-.237-.47-.517C4.28 3.24 5.576 2 7.825 2c2.25 0 3.767 1.36 3.767 3.215 0 1.344-.665 2.288-1.79 2.973-1.1.659-1.414 1.118-1.414 2.01v.03a.5.5 0 0 1-.5.5h-.77a.5.5 0 0 1-.5-.495l-.003-.2c-.043-1.221.477-2.001 1.645-2.712 1.03-.632 1.397-1.135 1.397-2.028 0-.979-.758-1.698-1.926-1.698-1.009 0-1.71.529-1.938 1.402-.066.254-.278.461-.54.461h-.777ZM7.496 14c.622 0 1.095-.474 1.095-1.09 0-.618-.473-1.092-1.095-1.092-.606 0-1.087.474-1.087 1.091S6.89 14 7.496 14Z"/>
                            </svg>
                        </button>
                  </div>

                  <!--div class="form-text" id="basic-addon4">Password needs to be atleast 8 characters long, 1 lowercase, 1 uppercase, 1 number and 1 special character.</div-->
                </div>
                <div class="mb-3" v-if="register">
                  <input
                    class="form-control"
                    type="password"
                    name="password2"
                    placeholder="Re-enter Password"
                    v-model="form.password2"
                    required
                    minlength="8"
                  />
                  <div class="form-text" id="basic-addon4" v-if="this.form.password === this.form.password2 && this.form.password2.length>7">Password Matches!!!</div>
                </div>
                <div class="mb-3">
                  <button
                    class="btn btn-primary"
                    type = "submit" @click="submit_details()" v-if="register">Submit</button>
                    <button
                    class="btn btn-primary"
                    type = "submit" @click="login" v-else>Login</button>  
                 </div>
                </div> 

                <div class="card-body">
                  <div class="card-text alert alert-danger" v-if="this.form.error">
                {{ this.form.errmsg }}
              </div>
              <div class="card-text alert alert-success" v-if="this.success" >
                {{ this.succmsg }}
              </div>
                </div>

                </div>
        <div class="card" style="margin-top: 20px;">
          <div class = "card-body">
            <p class="text-muted" v-if="register">
                  Have an account? <a @click="state" href="#">Log in</a>
                </p>
                <p class="text-muted" v-else>
                  Not a member? <a @click="state"  href="#">Register</a>
                </p>
          </div>
        </div>        

      </div> 
    </div>
  </div>  
  </div>            
</template>

<script>
import axios from 'axios';
import { mapMutations } from 'vuex';
export default {
data(){
  return {
    form: {
      name: "",
      email: "",
      password: "",
      password2: "",
      lowercheck:false,
      uppercheck:false,
      specialcheck:false,
      numcheck:false,
      error: false,
      errmsg:""
    },
    session: JSON.parse(localStorage.getItem("userSession")) || null,
    token: "",
    exp: "",
    register: false,
    succmsg: "",
    success: false,
    flag: 0,
  };
},
methods: {
  ...mapMutations(['setUser_id']),
  user_id(id){
    this.setUser_id(id);
  },  
    home(){
      this.$router.push('/');
    },
    EmailCheck(str){
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(str);
    },
    NameCheck(str){
      return str.length > 0;
    },
    
    PasswordMatch(str1, str2){
      return str1 === str2
    },

    PasswordCheck(str1){
      return (str1.length > 8 && this.form.uppercheck === true && this.form.lowercheck === true && this.form.numcheck === true && this.form.specialcheck === true)
    },
    state() {
      this.form.error = false;
      this.register = !this.register;
    },
    async submit_details(){
      if (
        this.EmailCheck(this.form.email) &&
        this.NameCheck(this.form.name) &&
        this.PasswordCheck(this.form.password) &&
        this.PasswordMatch(this.form.password, this.form.password2)
      )

    {
      try{
        const response = await axios.post('http://127.0.0.1:5000/api/registration', this.form, {
          headers: {
                      "Content-Type": "application/JSON"
                    }
        });
        if (response.data.message === 'Admin Role Created successfully') {
        this.success = true;
        this.succmsg = 'Admin created successfully';
      }

      if (response.data.error) {
        throw new Error(response.data.error_description);
      } else {
        this.form.error = false;
        this.token = response.data.access_token;
        this.exp = response.data.exp;
        this.role = response.data.role[0];
        this.userid = response.data.user_id
        this.username = response.data.user_name
      }

      if (!this.form.error) {
        this.userSession = {
          token: this.token,
          exp: this.exp,
          role: this.role,
          userid: this.userid,
          username: this.username
        };
        localStorage.setItem('userSession', JSON.stringify(this.userSession));

        if (this.success === false) {
          this.success = true;
          this.succmsg = 'Registration Successful';
        }
      }
    } catch (error) {
      this.form.error = true;
      this.form.errmsg = error.response.data.error_description;
      console.log(error);
    }

      }
    else{

        if(!this.NameCheck(this.form.name)){
            this.form.error = true;
            this.form.errmsg = "Please enter a valid name";
          }
        else if(!this.EmailCheck(this.form.email)){
           this.form.error = true;
           this.form.errmsg = "Please enter a valid email";
          }
        else if(!this.PasswordCheck(this.form.password)){
          this.form.error = true;
          this.form.errmsg = "Please enter a valid password";
        }
        else if(!this.PasswordMatch(this.form.password, this.form.password2)){
           this.form.error = true;
            this.form.errmsg = "Passwords do not match";
           }
      }
  },

 
  async login() {
      this.form.error = false;
      this.flag = 0;
      if (
        this.EmailCheck(this.form.email) &&
        this.PasswordCheck(this.form.password)
      )
 
    {
      try{
        const response = await axios.post('http://127.0.0.1:5000/api/login', this.form, {
                  headers: {
                              "Content-Type": "application/JSON",
                            }
                });
                console.log(response);
                if (response.status >= 200 && response.status < 300) {
                  this.token = response.data.access_token;
                  this.exp = response.data.exp;
                  console.log(this.exp);
                  this.role = response.data.role;
                  this.userSession = {
                      token: response.data.access_token,
                      role: response.data.role[0],
                      exp: response.data.exp,
                      userid: response.data.user_id,
                      username: response.data.user_name,
                  };
                  localStorage.setItem('userSession', JSON.stringify(this.userSession));
                  const isAuthenticated = true;
                  const role = response.data.role[0];
                  var id = response.data.user_id;
                  var username = response.data.user_name;
                  this.$store.commit('setAuthentication', isAuthenticated);
                  this.$store.commit('setRole', role);
                  this.$store.commit('setUser_id', id);
                  this.$store.commit('setUser_name', username);
                  this.home();
                
                }
                else{
                  this.form.error = true;
                  throw new Error(response.data.error_description)
                }
    }
    catch (error) {
      this.form.error = true;
      this.form.errmsg = error.response.data.error_description;
      console.log(error.response.data.error_description);
    }
  }
 

    else{
      if(!this.EmailCheck(this.form.email)){
           this.form.error = true;
           this.form.errmsg = "Please enter a valid email";
           console.log("emailcheckfailed");
          }
      else if(!this.PasswordCheck(this.form.password)){
          this.form.error = true;
          this.form.errmsg = "Please enter a valid password";
          console.log("passcheckfailed");
        }
    }

  }

  },

  watch: {
    "form.password"(newValue){

      this.form.lowercheck=false;
      this.form.uppercheck=false;
      this.form.specialcheck=false;
      this.form.numcheck=false;

      for(let z=0; z<newValue.length;z++){
          let a = newValue[z];
          let b = newValue.charCodeAt(z);

          if (a >= 'a' && a <= 'z'){
            this.form.lowercheck = true ;
          }

          else if(a >= 'A' && a <= 'Z'){
            this.form.uppercheck = true;
          }

          else if(a >= '0' && a <= '9'){
            this.form.numcheck = true;
          }

          else if((b >= 32 && b<= 47) || (b >= 58 && b <= 64)){
             this.form.specialcheck = true;
          }

      }
    },
  },
};
</script>

<style scoped>
.container {
  text-align: center;
  margin-top: 110px;
}

</style>