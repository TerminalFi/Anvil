import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

const URI = "/api/scans/";

export default new Vuex.Store({
  state: {
    scans: [],
    total_list: 0,
    completed_scans: 0,
    running_scans: 0,
    terminated_scans: 0,
    total_scans: 14
  },
  mutations: {
    addScan({ scans }, scan) {
      scans.push(scan);
    },
    addCompleted(state) {
    	state.running_scans--;
    	state.completed_scans++;
    },
    addRunning(state) {
    	state.total_scans++;
    	state.running_scans++;
    },
    addTerminated(state) {
    	state.running_scans--;
    	state.terminated_scans++;
    },
    addTotal(state) {
      state.total_scans++;
    },
    setCompleted(state, total) {
      state.completed_scans = total;
    },
    setRunning(state, total) {
      state.running_scans = total;
    },
    setTerminated(state, total) {
      state.terminated_scans = total;
    },
    setTotal(state, total) {
      state.total_scans = total;
    },
    setTotalList(state, total) {
      state.total_list = total;
    },
    clearScans(state) {
      state.scans = [];
    }
  },
  actions: {
  	getScanStats({ commit }) {
  		axios.get('/scan/stats').then(response => {
        if (response.status == 200) {
        	console.o
          commit("setCompleted", response.data.completed_scans.value);
          commit("setRunning", response.data.running_scans.value);
          commit("setTerminated", response.data.terminated_scans.value);
          commit("setTotal", response.data.total_scans.value);
        }
      });
  	},
    getScansFromApi({ commit }, parameters) {
      const { sortBy, descending, page, rowsPerPage } = parameters[0]
      let orderBy = (descending === true) ? `-${sortBy}` : `${sortBy}`;
      let requestURL = `${URI}?limit=${rowsPerPage}&offset=${page *
        rowsPerPage - rowsPerPage}&search=${parameters[1]}&ordering=${orderBy}`;
      axios.get(requestURL).then(response => {
        if (response.status == 200) {
          let jobs = response.data.results;
          commit("clearScans");
          commit("setTotalList", response.data.count);
          jobs.forEach(item => {
            commit("addScan", item);
          });
        }
      });
    },
    addCompletedScan({ commit }) {
    	commit('addCompleted')
    },
    addRunningScan({ commit }) {
    	commit('addRunning')
    },
    addTerminatedScan({ commit }) {
    	commit('addTerminated')
    },
    addTotalScan({ commit }) {
    	commit('addTotal')
    }
  },
  getters: {
    scanList: state => state.scans,
    totalCompleted: state => state.completed_scans,
    totalRunning: state => state.running_scans,
    totalTerminated: state => state.terminated_scans,
    totalScans: state => state.total_scans,
    totalList: state => state.total_list
  }
});
