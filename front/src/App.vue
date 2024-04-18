<template>
  <div id="app">
    <AuthCheck :valid="null" :loading="connected === null"
               loading-msg="Checking credentials" invalid-msg="Invalid credentials"
               valid-msg="Credentials valid" v-if="connected === null"/>
    <Connection @connect="connect" v-else-if="connected === false"/>
    <Main @toggleTheme="toggleTheme" v-else/>
  </div>
</template>

<script>
import Connection from './components/Connection.vue'
import Main from "@/components/Main.vue";
import AuthCheck from "@/components/connection/AuthCheck.vue";
import Services from "./services/services.js";

export default {
  name: 'App',
  components: {
    AuthCheck,
    Main,
    Connection
  },
  data() {
    return {
      connected: null,

      themeKey: 'theme',
      themeDark: 'dark',
      themeLight: 'light',
      lightThemeCss: "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
      darkThemeCss: "https://bootswatch.com/4/cyborg/bootstrap.min.css"

    }
  },
  mounted() {

    if (process.env.VUE_APP_DEMO === 'true') {
      console.log(" == DEMO FRONTEND == ")
    }

    let token = localStorage.getItem('jwt');
    let self = this;

    this.service = Services.getPfaApiPublicService();
    this.service.checkJwt(token)
      .then(function(b) {
        self.connected = b
      });

    this.initTheme();
  },

  methods: {
    connect(jwt) {
      localStorage.setItem('jwt', jwt);
      this.connected = true;
    },

    initTheme() {
      let theme = localStorage.getItem(this.themeKey);
      if (theme === null) {
        theme = this.themeDark;
      }

      this.setTheme(theme);
    },

    setTheme(theme) {

      let main_theme = document.getElementById("main-css");
      let add_light_theme = document.getElementById("light-theme-additional");
      let add_dark_theme = document.getElementById("dark-theme-additional");

      if (theme === this.themeLight) {
        // go light
        localStorage.setItem(this.themeKey, this.themeLight);
        main_theme.href = this.lightThemeCss;
        add_light_theme.disabled = false;
        add_dark_theme.disabled = true;

      } else if (theme === this.themeDark) {
        // go dark
        localStorage.setItem(this.themeKey, this.themeDark);
        main_theme.href = this.darkThemeCss;
        add_light_theme.disabled = true;
        add_dark_theme.disabled = false;
      }
    },
    toggleTheme() {

      let theme = localStorage.getItem(this.themeKey);
      if (theme === this.themeDark) {
        this.setTheme(this.themeLight)

      } else if (theme === this.themeLight) {
        this.setTheme(this.themeDark)

      }
    }
  }
}
</script>

<style>

</style>
