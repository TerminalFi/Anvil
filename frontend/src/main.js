import Vue from 'vue'
import './plugins/vuetify'
import moment from 'moment'
import App from './App.vue'
import store from './store'

Vue.config.productionTip = false


Vue.filter('formatDate', function(value) {
	if (value) {
		return moment(String(value)).format('MM/DD/YYYY hh:mm')
	}
});

new Vue({
	store,
	render: h => h(App),
}).$mount('#app')

