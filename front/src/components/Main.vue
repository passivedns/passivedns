<template>
  <div>
    <Navbar @toggleTheme="toggleTheme"/>
    <div id="main">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>

import Navbar from "@/components/main/Navbar";
export default {
name: "Main",
  components: {Navbar},
  data() {
    return {
    }
  },
  mounted() {

  },
  methods: {
    toggleTheme() {
      this.$emit('toggleTheme')
    }
  }
}

</script>

<style scoped>

  #main {
    margin-top: 50px;
  }

</style>