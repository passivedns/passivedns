<template>
  <div class="container">
    <div class="container">
      <img class="light" src="../assets/icons/passive_dns_white.png" alt="main" width="80%">
      <h1>Passive DNS</h1>
      <Ribbon></Ribbon>
      <span>Monitor DNS resolutions</span>
    </div>

    <div class="container login">

      <transition name="fade">
        <div>
          <div class="input-group mb-3">
            <input v-model="identity" type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="button-login">
          </div>
          <div class="input-group mb-3">
            <input v-model="password" type="password" class="form-control" placeholder="Password" aria-label="Password" aria-describedby="button-password" v-on:keyup.enter="login">
          </div>
          <div class="center">
              <button @click="login" class="btn btn-outline-primary" type="button" id="button-password">Login</button>
          </div>
          <AuthCheck :valid="valid" :loading="loading" loading-msg="Checking credentials" valid-msg="Credentials valid" invalid-msg="Invalid credentials" v-if="loading"/>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import Ribbon from "@/components/Ribbon.vue";
import AuthCheck from "@/components/connection/AuthCheck.vue";
import Services from "../services/services.js";

export default {
  name: 'Connection',
  components: {AuthCheck, Ribbon},
  data() {
    return {
      identity: "",
      password: "",

      loading: false,
      valid: null,
    }
  },
  mounted() {
    this.service = Services.getPfaApiPublicService()
  },
  methods: {
    login() {
      let self = this;
      this.loading = true;
      this.valid = null;
      this.service.login(this.identity, this.password)
          .then(function (jwt) {
            self.valid = true;
            self.$emit('connect', jwt);
          })
          .catch(function () {
            self.valid = false;
          })
          .finally(function () {
            setTimeout(function () {
              self.loading = false;
            }, 3000)
          })
      },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .container {
    width: fit-content;
    text-align: center;
  }

  .login {
    margin-top: 30px;
  }

  .sub-action {
    margin-top: 15px;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .25s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }

</style>
