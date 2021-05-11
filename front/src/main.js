import Vue from 'vue'
import App from './App.vue'
import VueRouter from "vue-router";
import Home from "@/components/main/home/Home"
import User from "@/components/main/user/User";
import NotFound from "@/components/NotFound";
import Channels from "@/components/main/channels/Channels";
import Alerts from "@/components/main/alerts/Alerts";
import Admin from "@/components/main/admin/Admin";
import Users from "@/components/main/admin/users/Users";
import DomainNameDetailPage from "@/components/main/home/DomainNameDetailPage";

Vue.config.productionTip = false;


Vue.use(VueRouter);
const routes = [
  {path: "/", component: Home},
  {path: "/dn/:dn", component: DomainNameDetailPage},
  {path: "/user", component: User},
  {path: "/alerts", component: Alerts},
  {path: "/channels", component: Channels},
  {path: "/admin", component: Admin},
  {path: "/users", component: Users},
  {path: "/user", component: User},
  {path: "/404", component: NotFound},
  {path: "*", redirect: "/404"},
];

const router = new VueRouter({
  mode: "history",
  routes: routes,
});

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
