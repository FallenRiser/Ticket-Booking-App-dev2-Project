<template>
<div id="app">
  <div id="page-container">
 <Navbar></Navbar>
 <router-view></router-view>
   <div id="content-wrap">

   </div>
   <Footer></Footer>
 </div>
</div>
 </template>
 <script>
 import Navbar from './components/Navbar.vue';
 import Footer from './components/Footer.vue';
 
 export default {
   name: 'App',
   components: {
     Navbar,
     Footer
   }
 }
 </script>
 
 <style>
 #app {
   text-align: center;
 }

 #page-container {
  position: relative;
  min-height: 100vh;
}

#content-wrap {
  padding-bottom: 2.5rem;   
}

 </style>