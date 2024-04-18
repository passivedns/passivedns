import { createApp } from 'vue'
import App from './App.vue'
//import VueRouter from "vue-router";
import { createWebHistory, createRouter } from "vue-router";
import Home from "@/components/main/home/Home"
import User from "@/components/main/user/User";
import NotFound from "@/components/NotFound";
import Channels from "@/components/main/channels/Channels";
import Alerts from "@/components/main/alerts/Alerts";
import Admin from "@/components/main/admin/Admin";
import Users from "@/components/main/admin/users/Users";
import DomainNameDetailPage from "@/components/main/home/DomainNameDetailPage";


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
  {path: "/:catchAll(.*)", redirect: "/404"},
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

const app = createApp(App)

app.use(router)

app.mount('#app')
