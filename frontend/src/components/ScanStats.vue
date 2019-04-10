<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap >
      <v-flex
        d-flex
        xs12
        md6
        lg3
        >
        <v-card >
         <v-card-text>
            <v-layout align-center justify-center row fill-height>
              <v-flex
                grow
                pa-1
                >
                <div class="text-xs font-weight-bold text-uppercase success--text mb-1">Completed Scans</div>
                <div class="scans-completed h5 mb-0 font-weight-bold text-gray-800">{{ completed_scans }}</div>
              </v-flex>
              <v-flex
                shrink
                pa-1
                >
                <i class="fas fa-2x fa-circle-notch success--text"></i>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex
        d-flex
        xs12
        md6
        lg3
        >
        <v-card >
         <v-card-text>
            <v-layout align-center justify-center row fill-height>
              <v-flex
                grow
                pa-1
                >
                <div class="text-xs font-weight-bold text-uppercase warning--text mb-1">Running Scans</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ running_scans }}</div>
              </v-flex>
              <v-flex
                shrink
                pa-1
                >
                <i class="fas fa-2x fa-undo-alt warning--text"></i>
              </v-flex>
            </v-layout>
            <v-layout v-if="running_scans > 0">
              <v-progress-linear :indeterminate="true" color="warning"></v-progress-linear>
            </v-layout>
            <v-layout v-else>
              <v-progress-linear :indeterminate="false" color="transparent"></v-progress-linear>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex
        d-flex
        xs12
        md6
        lg3
        >
        <v-card >
         <v-card-text>
            <v-layout align-center justify-center row fill-height>
              <v-flex
                grow
                pa-1
                >
                <div class="text-xs font-weight-bold text-uppercase error--text mb-1">Terminated Scans</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ terminated_scans }}</div>
              </v-flex>
              <v-flex
                shrink
                pa-1
                >
                <i class="fas fa-2x fa-ban error--text"></i>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex
        d-flex
        xs12
        md6
        lg3
        >
        <v-card >
         <v-card-text>
            <v-layout align-center justify-center row fill-height>
              <v-flex
                grow
                pa-1
                >
                <div class="text-xs font-weight-bold text-uppercase info--text mb-1">Total Scans</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ total_scans }}</div>
              </v-flex>
              <v-flex
                shrink
                pa-1
                >
                <i class="fas fa-2x fa-arrow-up info--text"></i>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <button @click="addCompletedScan">scan_completed</button>
    <button @click="addRunningScan">scan_running</button>
    <button @click="addTerminatedScan">scan_terminated</button>
  </v-container>
</template>

<script>
  import { mapGetters, mapState, mapActions } from 'vuex';

  export default {
    data: () => ({
      stats: []
      }),
    computed: {
      ...mapState(['completed_scans']),
      ...mapState(['running_scans']),
      ...mapState(['terminated_scans']),
      ...mapState(['total_scans']),
      ...mapGetters(['totalScans'])
    },
    mounted () {
      this.getScanStats();
    },
    methods: {
      ...mapActions(['getScanStats']),
      ...mapActions(['addCompletedScan']),
      ...mapActions(['addRunningScan']),
      ...mapActions(['addTerminatedScan']),
      ...mapActions(['addTotalScan'])
    },
  }
</script>

<style>

</style>
