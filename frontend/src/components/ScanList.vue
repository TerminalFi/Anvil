<template>
    <v-app id="inspire">
      <v-container fluid>
        <v-card>
          <v-card-title>
            <v-btn color="success" @click="new_scan = true"><i class="fas fa-plus-square fa-2x"></i></v-btn>
            <v-btn color="error" @click="stop_scan = true"><i class="fas fa-ban fa-2x"></i></v-btn>
            <v-btn color="info" @click="archive_scan = true"><i class="fas fa-archive fa-2x"></i></v-btn>
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
            <v-data-table
              v-model="selected" 
              item-key="job_uuid" 
              :headers="headers" 
              :items="scans" 
              :total-items="totalList"  
              :pagination.sync="pagination" 
              :hide-headers="isMobile" 
              :class="{mobile: isMobile}"
              select-all>
              <template v-slot:items="props">
                <tr v-if="!isMobile" :id="props.item.job_uuid">
                  <td>
                    <v-checkbox
                      v-model="props.selected"
                      primary
                      hide-details
                    ></v-checkbox>
                  </td>
                  <td >{{ props.item.job_start_time | formatDate }}</td>
                  <td >{{ props.item.job_uuid }}</td>
                  <td >{{ props.item.job_name }}</td>
                  <td v-if="props.item.job_status === 'initialization'">
                    <v-chip color="info" text-color="white">{{ props.item.job_status }}</v-chip>
                  </td>
                  <td v-else-if="props.item.job_status === 'running'">
                    <v-chip color="warning" text-color="white">{{ props.item.job_status }}</v-chip>
                  </td>
                  <td v-else-if="props.item.job_status === 'completed'">
                    <v-chip color="success" text-color="white">{{ props.item.job_status }}</v-chip>
                  </td>
                  <td v-else-if="props.item.job_status === 'terminated'">
                    <v-chip color="error" text-color="white">{{ props.item.job_status }}</v-chip>
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
        <v-dialog v-model="new_scan" persistent max-width="600px">
          <v-card>
            <v-toolbar color="success" dark>

              <v-toolbar-title>New scan?</v-toolbar-title>

            </v-toolbar>
            <v-card-text>
              <v-container grid-list-md>
                <v-layout wrap>
                  <v-flex xs12>
                    <v-text-field label="Scan name*" required></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field label="Target*"required></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <span class="title">Scan Type*</span>
                    <v-radio-group v-model="new_scan" row required>
                      <v-flex column>
                      <v-radio label="Staged" value="1"></v-radio>
                      <v-radio label="Basic Discovery" value="2"></v-radio>
                      <v-radio label="Basic TCP" value="3"></v-radio>
                      <v-radio label="Intense TCP" value="4"></v-radio>
                    </v-flex>
                    <v-flex column>
                      <v-radio label="Basic UDP" value="5"></v-radio>
                      <v-radio label="Intense UDP" value="6"></v-radio>
                    </v-flex>
                  </v-radio-group>
                </v-flex>
                </v-layout>
              </v-container>
              <p class="caption text-xs-left">*indicates required field</p>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" flat @click="new_scan = false">Cancel</v-btn>
              <v-btn color="green darken-1" flat @click="new_scan = false">Confirm</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="stop_scan" persistent max-width="600px">
          <v-card>
            <v-toolbar color="error" dark>

              <v-toolbar-title>Terminate scans?</v-toolbar-title>

            </v-toolbar>
            <v-list>
              <template v-for="(item, index) in selected">
                <v-divider
                ></v-divider>

                <v-list-tile
                  :key="item.job_uuid"
                >
                <v-list-tile-action>
                  <v-list-tile-title v-html=""></v-list-tile-title>
                </v-list-tile-action>
                  <v-list-tile-content>
                    <v-list-tile-title v-html="item.job_name"></v-list-tile-title>
                    <v-list-tile-sub-title v-html="item.job_uuid"></v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
              </template>
            </v-list>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" flat @click="stop_scan = false">Cancel</v-btn>
              <v-btn color="green darken-1" flat @click="stop_scan = false">Confirm</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="archive_scan" persistent max-width="600px">
          <v-card>
            <v-toolbar color="info" dark>

              <v-toolbar-title>Archive scans?</v-toolbar-title>

            </v-toolbar>
            <v-list>
              <template v-for="(item, index) in selected">
                <v-divider
                ></v-divider>

                <v-list-tile
                  :key="item.job_uuid"
                >
                <v-list-tile-action>
                  <v-list-tile-title v-html=""></v-list-tile-title>
                </v-list-tile-action>
                  <v-list-tile-content>
                    <v-list-tile-title v-html="item.job_name"></v-list-tile-title>
                    <v-list-tile-sub-title v-html="item.job_uuid"></v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
              </template>
            </v-list>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" flat @click="archive_scan = false">Cancel</v-btn>
              <v-btn color="green darken-1" flat @click="archive_scan = false">Confirm</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-container>
    </v-app>
</template>

<script>
  import { mapGetters, mapState, mapActions } from 'vuex';

  export default {
  data: () => ({
      new_scan: false,
      stop_scan: false,
      archive_scan: false,
        pagination: {
          rowsPerPage: 5
        },
        selected: [],
        search: '',
        isMobile: false,
        loading: false,
        headers: [{
            text: 'Scan Start Time',
            align: 'left',
            sortable: false,
            value: 'job_start_time'
          },
          {
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
        totalItems: 0,
        items: []
      }),
    watch: {
      pagination: {
        handler () {
          this.getScansFromApi([this.pagination, this.search])
        },
        deep: true
      },
      search() {
        if(this.search) {
          this.getScansFromApi([this.pagination, this.search])
        } 
        else {
          this.getScansFromApi([this.pagination, ''])
        }
      }
    },
    mounted () {
      if(this.search) {
        this.getScansFromApi([this.pagination, this.search])
      } 
      else {
        this.getScansFromApi([this.pagination, ''])
      }
    },
    computed: {
      ...mapState(['scans']),
      ...mapGetters(['totalList'])
    },
    methods: {
      ...mapActions(['getScansFromApi']),
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
