<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap >
      <v-flex
        d-flex
        xs12
        md6
        lg3
        v-for="stat in stats"
        :key="stat.name"
        >
        <v-card >
         <v-card-text>
            <v-layout align-center justify-center row fill-height>
              <div class="col mr-2">
                <div :class="{ 'text-success' : stat.name == 'Completed Scans', 'text-warning' : stat.name == 'Running Scans', 'text-danger' : stat.name == 'Terminated Scans', 'text-info' : stat.name == 'Total Scans'}" class="text-xs font-weight-bold text-uppercase mb-1">{{ stat.name }}</div>
                <div class="scans-completed h5 mb-0 font-weight-bold text-gray-800">{{ stat.value }}</div>
              </div>
              <div class="col-auto">
                <i :class="{ 'fa-circle-notch text-success' : stat.name == 'Completed Scans', 'fa-undo-alt text-warning' : stat.name == 'Running Scans', 'fa-ban text-danger' : stat.name == 'Terminated Scans', 'fa-arrow-up text-info' : stat.name == 'Total Scans'}" class="fas fa-2x text-success"></i>
              </div>
            </v-layout>
             <v-layout v-if="stat.name === 'Running Scans' && stat.value > 0">
              <v-progress-linear :indeterminate="true" color="orange"></v-progress-linear>
            </v-layout>
            <v-layout v-else-if="stat.name === 'Running Scans'">
              <v-progress-linear :indeterminate="false" color="transparent"></v-progress-linear>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <button @click="scan_completed">scan_completed</button>
    <button @click="scan_running">scan_running</button>
    <button @click="scan_terminated">scan_terminated</button>
  </v-container>
</template>

<script>
  export default {
    data: () => ({
      stats: []
      }),
    methods: {
      scan_completed () {
        this.stats.running_jobs.value--;
        this.stats.completed_jobs.value++;
      },
      scan_running () {
        this.stats.running_jobs.value++;
      },
      scan_terminated () {
        this.stats.running_jobs.value--;
        this.stats.terminated_jobs.value++;
      }
    },
    created:function() {
      fetch('/scan/stats/')
      .then(res => res.json())
      .then(res => {
        this.stats = res;
      })
    },
  }
</script>

<style>

</style>
