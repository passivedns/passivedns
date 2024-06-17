import { createApp } from 'vue'
import App from './App.vue'
//import VueRouter from "vue-router";
import { createWebHistory, createRouter } from "vue-router";
import Home from "@/components/main/home/Home.vue";
import User from "@/components/main/user/User.vue";
import NotFound from "@/components/NotFound.vue";
import Channels from "@/components/main/channels/Channels.vue";
import Alerts from "@/components/main/alerts/Alerts.vue";
import Admin from "@/components/main/admin/Admin.vue";
import Users from "@/components/main/admin/users/Users.vue";
import DomainNameDetailPage from "@/components/main/home/DomainNameDetailPage.vue";
import ExternApis from "@/components/main/ExternApis/ExternApis.vue";


const routes = [
  {path: "/", component: Home},
  {path: "/dn/:dn", component: DomainNameDetailPage},
  {path: "/user", component: User},
  {path: "/alerts", component: Alerts},
  {path: "/channels", component: Channels},
  {path: "/externApis", component: ExternApis},
  {path: "/admin", component: Admin},
  {path: "/users", component: Users},
  {path: "/user", component: User},
  {path: "/404", component: NotFound},
  {path: "/:catchAll(.*)", redirect: "/404"},
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

const app = createApp(App)

app.use(router)

app.mount('#app')
