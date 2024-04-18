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
          <div class="sub-action">
            <div>Not registered yet ?</div>
            <div><button @click="toTabRequestAccess" class="btn btn-primary">Request access</button></div>
          </div>
          <div class="sub-action">
            <div>Received a code ?</div>
            <div><button @click="toTabEnterToken" class="btn btn-primary">Register</button></div>
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

      <transition name="fade" @after-leave="toTab">
        <div v-if="tab === tabRequestAccess">
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <button @click="toTabLogin" class="btn btn-outline-secondary">&lt;&lt; Back</button>
            </div>
            <input v-model="requestEmail" type="text" class="form-control" placeholder="Email" aria-label="Email" aria-describedby="button-request-access">
            <div class="input-group-append">
              <button @click="requestAccess" class="btn btn-outline-primary" type="button" id="button-request-access">Request access</button>
            </div>
          </div>
          <AuthCheck :valid="valid" :loading="loading" invalid-msg="Cannot send request access" loading-msg="Sending request" valid-msg="Request access sent to admin"></AuthCheck>
        </div>
      </transition>

      <transition name="fade" @after-leave="toTab">
        <div v-if="tab === tabEnterToken">
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <button @click="toTabLogin" class="btn btn-outline-secondary">&lt;&lt; Back</button>
            </div>
            <input v-model="registerToken" type="password" class="form-control" placeholder="Token" aria-label="Token" aria-describedby="button-enter-token">
            <div class="input-group-append">
              <button @click="checkToken" class="btn btn-outline-primary" type="button" id="button-enter-token">Check token</button>
            </div>
          </div>
          <AuthCheck :valid="valid" :loading="loading" invalid-msg="Invalid token" loading-msg="Checking token" valid-msg="Token valid"></AuthCheck>
        </div>
      </transition>

      <transition name="fade" @after-leave="toTab">
        <div v-if="tab === tabRegister">
          <div class="form-group">
            <label for="register-username" class="sr-only">Username</label>
            <input type="text" v-model="registerUsername" class="form-control" placeholder="Enter username" id="register-username" v-on:keyup="validateEmailAddress">
          </div>

          <div class="form-group">
            <label for="register-password" class="sr-only">Password</label>
            <input type="password" v-model="registerPassword" class="form-control" placeholder="Enter password" id="register-password">
          </div>

          <div class="form-group">
            <label for="register-password-confirm" class="sr-only">Confirm</label>
            <input type="password" v-model="registerPasswordConfirm" class="form-control" placeholder="Confirm password" id="register-password-confirm">
          </div>

          <div class="btn-group" role="group" aria-label="Basic example">
            <button @click="toTabEnterToken" type="button" class="btn btn-outline-secondary">&lt;&lt; Back</button>
            <button @click="register" type="button" class="btn btn-outline-primary">Register</button>
          </div>

          <AuthCheck :valid="valid" :loading="loading" invalid-msg="Registration failed" loading-msg="Registering" valid-msg="Registration complete"></AuthCheck>
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
      tabRequestAccess: "requestAccess",
      tabEnterToken: "enterToken",
      tabRegister: "register",

      identity: "",
      password: "",
      requestEmail: "",

      registerToken: "",
      registerUsername: "",
      registerPassword: "",
      registerPasswordConfirm: "",


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
    toTabRequestAccess() {
      this.tab = null;
      this.nextTab = this.tabRequestAccess;
    },
    toTabLogin() {
      this.tab = null;
      this.nextTab = this.tabLogin
    },
    toTabEnterToken() {
      this.tab = null;
      this.nextTab = this.tabEnterToken;
    },
    toTabRegister() {
      this.tab = null;
      this.nextTab = this.tabRegister;
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
    requestAccess() {
      let self = this;
      this.loading = true;
      this.valid = null;
      this.service.requestAccess(this.requestEmail)
          .then(function () {
            self.valid = true;
          })
          .catch(function (err) {
            console.log(err.response.data.msg);
            self.valid = false;
          })
          .finally(function () {
            setTimeout(function () {
              self.loading = false;
            }, 3000)
          })
    },
    checkToken() {
      let self = this;
      this.loading = true;
      this.service.checkRegisterToken(this.registerToken)
          .then(function (b) {
            self.valid = b;
            if (b) {
              self.toTabRegister();
            }
          })
          .finally(function () {
            setTimeout(function () {
              self.loading = false;
            }, 3000)
          })

    },
    register() {
      let self = this;
      this.loading = true;
      this.service.register(this.registerToken, this.registerUsername, this.registerPassword)
          .then(function (b) {
            self.valid = b;
            if (b) {
              self.toTabLogin();
            }
          })
          .finally(function () {
            setTimeout(function () {
              self.loading = false;
            }, 3000)
          })
    },
      validateEmailAddress: function (e) {
        if (e.keyCode === 13) {
          this.toTabPassword();
          this.login();
        }
        this.log += e.key;
      },

      postEmailAddress: function () {
        this.log += '\n\nPosting';
      }
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
