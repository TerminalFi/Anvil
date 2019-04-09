<template>
  <v-app>
    <v-content>
      <ScanStats/>
      <ScanList/>
    </v-content>
  </v-app>
</template>

<script>
import ScanList from './components/ScanList'
import ScanStats from './components/ScanStats'

export default {
  name: 'App',
  components: {
    ScanList,
    ScanStats
  },
  data () {
    return {
      //
    }
  }
}
</script>
