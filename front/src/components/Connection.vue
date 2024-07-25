<template>
  <div class="container">
    <div class="container">
      <img class="light" src="../assets/icons/passive_dns_white.png" alt="main">
      <h1>Passive DNS</h1>
      <Ribbon></Ribbon>
      <span>Monitor DNS resolutions</span>
    </div>

    <div class="container login">

      <transition name="fade" @after-leave="toTab">
        <div v-if="tab === tabLogin ">
          <div class="input-group mb-3">
            <input v-model="identity" type="text" class="form-control" placeholder="Username or email" aria-label="Username" aria-describedby="button-login" v-on:keyup="validateEmailAddress">
            <div class="input-group-append">
              <button @click="toTabPassword" class="btn btn-outline-primary" type="button" id="button-login" v-on:click="postEmailAddress">Login</button>
            </div>
          </div>
        </div>
      </transition>

      <transition name="fade" @after-leave="toTab">
        <div v-if="tab === tabPassword ">
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <button @click="toTabLogin" class="btn btn-outline-secondary">&lt;&lt; Back</button>
            </div>
            <input v-model="password" type="password" class="form-control" placeholder="Password" aria-label="Password" aria-describedby="button-password" v-on:keyup="validateEmailAddress">
            <div class="input-group-append">
              <button @click="login" class="btn btn-outline-primary" type="button" id="button-password" v-on:click="postEmailAddress">Login</button>
            </div>
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
      tab: "login",
      nextTab: "",
      tabLogin: "login",
      tabPassword: "password",

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
    toTabPassword() {
      this.tab = null;
      this.nextTab = this.tabPassword;
    },
    toTabLogin() {
      this.tab = null;
      this.nextTab = this.tabLogin
    },
    toTab() {
      this.tab = this.nextTab;
      this.loading = false;
    },
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
