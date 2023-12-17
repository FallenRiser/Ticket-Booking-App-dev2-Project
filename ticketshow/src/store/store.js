import { createStore } from 'vuex';

const store = createStore({
    state: {
      isAuthenticated: false,
      role: null,
      user_id: null,
      selectedTheaterId: null,
      selectedScreenId: null,
      selectedScreenNo : null,
      selectedTheaterName: '',
      selectedTheaterTime: '',
      selectedScreenTech: '',
      selectedDate: null,
      selectedPrice: null,
      selectedAvailability: null,
      user_name: null,
    },
    getters:{
      isAuthenticated: state => state.isAuthenticated,
      role: state => state.role,
      user_id: state => state.user_id,
      user_name: state => state.user_name,
      selectedTheaterId: state => state.selectedTheaterId,
      selectedScreenId: state => state.selectedScreenId,
      selectedScreenNo: state => state.selectedScreenNo,
      selectedScreenTech: state => state.selectedScreenTech,
      selectedTheaterName: state => state.selectedTheaterName,
      selectedTheaterTime: state => state.selectedTheaterTime,
      selectedAvailability: state => state.selectedAvailability,
      selectedDate: state => state.selectedDate,
      selectedPrice: state => state.selectedPrice,
    },
    mutations: {
      setAuthentication(state, isAuthenticated) {
        state.isAuthenticated = isAuthenticated;
      },
      setRole(state, role) {
        state.role = role;
      },
      setUser_id(state, id) {
        state.user_id = id;
      },
      setUser_name(state, username) {
        state.user_name = username;
      },
      setSelectedTheaterId(state, theaterId) {
        state.selectedTheaterId = theaterId;
      },
      setSelectedScreenId(state, screenId) {
        state.selectedScreenId = screenId;
      },
      setSelectedScreenNo(state, screenno) {
        state.selectedScreenNo = screenno;
      },
      setSelectedScreenTech(state, screentech) {
        state.selectedScreenTech = screentech;
      },
      setSelectedTheaterName(state, theaterName) {
        state.selectedTheaterName = theaterName;
      },
      setSelectedTheaterTime(state, theaterTime) {
        state.selectedTheaterTime = theaterTime;
      },
      setSelectedDate(state, date) { 
        state.selectedDate = date;
      },
      setSelectedPrice(state, Price) { 
        state.selectedPrice = Price;
      },
      setSelectedAvailability(state, seats) { 
        state.selectedAvailability = seats;
      },
      logout(state){
        state.isAuthenticated = false;
        state.role = null;
        state.user_id = null;
        state.user_name = null;
        localStorage.removeItem('userSession');
      },
  }, 
  });

  const userSessionString = localStorage.getItem('userSession');
  const userSession = JSON.parse(userSessionString);
  
  if (userSession && userSession.token) {
    const { token, role, exp, userid, username } = userSession;
  
    console.log('Token:', token);
    console.log('Role:', role);
    console.log('Expiration timestamp:', exp);
  
    const expTimestampSeconds = parseInt(exp, 10); 
    const expTimestamp = expTimestampSeconds * 1000;
    const currentTimestamp = Date.now();
    
    const currentTimestampUTC = Date.UTC(
      new Date(currentTimestamp).getUTCFullYear(),
      new Date(currentTimestamp).getUTCMonth(),
      new Date(currentTimestamp).getUTCDate(),
      new Date(currentTimestamp).getUTCHours(),
      new Date(currentTimestamp).getUTCMinutes(),
      new Date(currentTimestamp).getUTCSeconds(),
      new Date(currentTimestamp).getUTCMilliseconds()
    );

    const timezoneOffsetInMilliseconds = new Date().getTimezoneOffset() * 60 * 1000;
    const adjustedCurrentTimestampUTC = currentTimestampUTC + timezoneOffsetInMilliseconds;

    console.log('current tmpstmp:', currentTimestamp);
    if (adjustedCurrentTimestampUTC < expTimestamp) {
      console.log('Token is still valid');
     
      store.commit('setAuthentication', true);
      store.commit('setRole', role);
      store.commit('setUser_id', userid);
      store.commit('setUser_name', username);
    } else {
      console.log('Token has expired');
   
      localStorage.removeItem('userSession');
      store.commit('setAuthentication', false);
      store.commit('setRole', null);
      store.commit('setUser_id', null);
      store.commit('setUser_name', null);
    }
  } else {
    console.log('Token not found in local storage');
   
    store.commit('setAuthentication', false);
    store.commit('setRole', null);
    store.commit('setUser_id', null);
    store.commit('setUser_name', null);
  }
  


export default store;    