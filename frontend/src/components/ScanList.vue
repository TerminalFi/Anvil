<template>
    <v-app id="inspire">
      <v-container fluid>
        <v-card>
          <v-card-title>
            <h3>Filter</h3>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-layout v-resize="onResize" column >
            <v-data-table :headers="headers" :items="jobs" :search="search" :pagination.sync="pagination" :hide-headers="isMobile" :class="{mobile: isMobile}">
              <template v-slot:items="props">
                <tr v-if="!isMobile" :id="props.item.job_uuid">
                  <td >{{ props.item.job_uuid }}</td>
                  <td >{{ props.item.job_name }}</td>
                  <td v-if="props.item.job_status === 'initialization'">
                    <v-chip color="blue" text-color="white">{{ props.item.job_status }}</v-chip>
                  </td>
                  <td v-else-if="props.item.job_status === 'running'">
                    <v-chip color="orange" text-color="white">{{ props.item.job_status }}</v-chip>
                  </td>
                  <td v-else-if="props.item.job_status === 'completed'">
                    <v-chip color="green" text-color="white">{{ props.item.job_status }}</v-chip>
                  </td>
                  <td v-else-if="props.item.job_status === 'terminated'">
                    <v-chip color="red" text-color="white">{{ props.item.job_status }}</v-chip>
                  </td>
                  <td v-else>
                    <v-chip color="orange" text-color="white">{{ props.item.job_status }}</v-chip>
                  </td>
                </tr>
                <tr v-else>
                  <td>
                    <ul class="flex-content">
                      <li class="flex-item" data-label="Job UUID">{{ props.item.job_uuid }}</li>
                      <li class="flex-item" data-label="Job Name">{{ props.item.job_name }}</li>
                      <li class="flex-item" data-label="Job Status">{{ props.item.job_status }}</li>
                    </ul>
                  </td>
                </tr>
              </template>
              <v-alert slot="no-results" :value="true" color="error" icon="warning">
                Your search for "{{ search }}" found no results.
              </v-alert>
            </v-data-table>
          </v-layout>
        </v-card>
      </v-container>
    </v-app>
</template>

<script>
  export default {
    data: () => ({
        pagination: {
          sortBy: 'name',
          rowsPerPage: 5
        },
        selected: [],
        search: '',
        isMobile: false,
        headers: [{
            text: 'Scan UUID',
            align: 'left',
            value: 'job_uuid'
          },
          {
            text: 'Scan Name',
            align: 'left',
            value: 'job_name'
          },
          {
            text: 'Scan Status',
            align: 'left',
            value: 'job_status'
          }
        ],
        jobs: []
      }),
    created:function() {
      fetch('/api/scans/')
      .then(res => res.json())
      .then(res => {
        this.jobs = res;
      })
    },
      methods: {
        onResize() {
          if (window.innerWidth < 769)
            this.isMobile = true;
          else
            this.isMobile = false;
        },
        toggleAll() {
          if (this.selected.length) this.selected = []
          else this.selected = this.desserts.slice()
        },
        changeSort(column) {
          if (this.pagination.sortBy === column) {
            this.pagination.descending = !this.pagination.descending
          } else {
            this.pagination.sortBy = column
            this.pagination.descending = false
          }
        }
      }
  }
</script>

<style>

</style>
