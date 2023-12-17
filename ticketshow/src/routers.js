import { createRouter, createWebHistory } from "vue-router"
import Home from './components/Home.vue'
import Register from './components/Register.vue'
import store from './store/store';
import add_theatre from './components/add_theatre.vue'
import add_movie from './components/add_movie.vue'
import all_movies from './components/all_movies.vue'
import all_theatres from './components/all_theatres.vue'
import add_timings from './components/add_timings.vue'
import movie from './components/movie.vue'
import book_tickets from './components/book_tickets.vue'
import booking_contd from './components/booking_contd.vue'
import profile from './components/profile.vue'
import edit_user from './components/edit_user.vue'
import edit_theatre from './components/edit_theatre.vue'
import edit_movie from './components/edit_movie.vue'
import edit_timings from './components/edit_timings.vue'
import theatre from './components/theatre.vue'
import search from './components/search.vue'
import theatre_stats from './components/theatre_stats.vue'

const routes = [

    {
        path:'/',
        name:'home',
        component:Home,
    },
    {

        path:'/login',
        name:'register',
        component:Register

    },
    {

        path:'/add-theatre',
        name:'add-theatre',
        component:add_theatre,
        meta: {
            requiresAuth: true,
            requiresAdmin: true,
        }

    },
    {

      path:'/add-movie',
      name:'add-movie',
      component:add_movie,
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
    }
  },
  {

    path:'/all-movies',
    name:'all-movies',
    component:all_movies,
},
{

  path:'/all-theatres',
  name:'all-theatres',
  component:all_theatres,
},
{
  path: '/add-timings/:movieID',
  name: 'add_timings',
  component: add_timings,
  props: true, 
  meta: {
    requiresAuth: true,
    requiresAdmin: true,
}
},
{

  path:'/movie/:id',
  name:'movie',
  component:movie,

},
{
  path: '/book-tickets/:movieID',
  name: 'book_tickets',
  component: book_tickets,
  props: true, 
  meta: {
    requiresAuth: true,
}
},
{
  path: '/booking/:movieid',
  name: 'booking',
  component: booking_contd,
  props: true,
  meta: {
    requiresAuth: true,
}
},
{
  path: '/profile/:userid',
  name: 'profile',
  component: profile,
  props: true,
  meta: {
    requiresAuth: true,
}
},
{
  path: '/edit-profile/:userid',
  name: 'edit_user',
  component: edit_user,
  meta: {
    requiresAuth: true,
}
},
{

  path:'/edit-theater/:theaterId',
  name:'edit_theater',
  component:edit_theatre,
  meta: {
      requiresAuth: true,
      requiresAdmin: true,
  }

},
{

  path:'/edit-movie/:movieId',
  name:'edit_movie',
  component:edit_movie,
  meta: {
      requiresAuth: true,
      requiresAdmin: true,
  }

},
{

  path:'/edit-timings/:movieId',
  name:'edit_timings',
  component:edit_timings,
  meta: {
      requiresAuth: true,
      requiresAdmin: true,
  }

},
{

  path:'/theatre/:theatreId',
  name:'theatre',
  component:theatre,
},
{

  path:'/search',
  name:'search',
  component:search

},
{

  path:'/theatre-stats/:theatreId',
  name:'theatre_stats',
  component:theatre_stats,
  meta: {
    requiresAuth: true,
    requiresAdmin: true,
}
},
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
  });


  router.beforeEach((to, from, next) => {
    const isAuthenticated = store.state.isAuthenticated;
    const role = store.state.role;
  
    if (to.meta.requiresAuth && !isAuthenticated) {
      next({ name: 'register' });
    } else if (to.meta.requiresAdmin && role !== 'admin') {
      next({ name: 'home' }); 
    } else {
      next();
    }
  });  

export default router;