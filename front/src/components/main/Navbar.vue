<template>
    <nav id="navbar" class="navbar navbar-expand-lg sticky-top justify-content-between light">
        <router-link to="/">
            <img class="navbar-brand light" src="../../assets/icons/passive_dns_white_32.png" alt="icon">
        </router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="nav nav-pills nav-fill">
                <li class="nav-item">
                    <router-link class="nav-link" to="/" exact-active-class="active">
                        <img class="light mr-1" src="../../assets/icons/icons8-home-24.png" alt="home">
                        Home
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/alerts" exact-active-class="active">
                        <img class="light mr-1" src="../../assets/icons/icons8-clock-alert-50.png" alt="alerts">
                        Alerts
                        <span v-if="alertCount > 0" class="badge badge-light">{{alertCount}}</span>
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/channels" exact-active-class="active">
                        <img class="light" src="../../assets/icons/icons8-conv-48.png" alt="conv">
                        Channels
                    </router-link>
                </li>
                <li class="nav-item" v-if="role === 'admin'">
                    <router-link class="nav-link" to="/admin" exact-active-class="active">
                        <img class="light" src="../../assets/icons/icons8-microsoft-admin-32.png" alt="admin">
                        Settings
                    </router-link>
                </li>
                <li class="nav-item" v-if="role === 'admin'">
                    <router-link class="nav-link" to="/users" exact-active-class="active">
                        <img class="light" src="../../assets/icons/icons8-microsoft-admin-32.png" alt="admin">
                        Users
                    </router-link>
                </li>
            </ul>
        </div>
        <div class="dropdown">
            <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <img src="../../assets/icons/icons8-male-user-24.png" alt="user">
            </button>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
                <h6 class="dropdown-header">Logged as {{user}}</h6>
                <button class="dropdown-item" @click="setTheme">
                    <img class="light" src="../../assets/icons/icons8-day-and-night-24.png" alt="night">
                    Toggle theme
                </button>
                <router-link class="dropdown-item" to="/user" exact-active-class="active">
                    <img class="light" src="../../assets/icons/icons8-settings-24.png" alt="settings">
                    Settings
                </router-link>
                <div class="dropdown-divider"></div>
                <button @click="logout" class="dropdown-item">
                    <img class="light" src="../../assets/icons/icons8-logout-rounded-left-24.png" alt="logout">
                    Logout
                </button>
            </div>
        </div>
    </nav>
</template>

<script>
    import * as jwt from "jsonwebtoken";
    import PfaApi from "@/services/pfa-api";

    export default {
        name: "Navbar",
        data() {
            return {
                user: "",
                role: "",
                alertCount: 0,
            }
        },
        mounted() {
            let token = localStorage.getItem('jwt');
            let payload = jwt.decode(token);
            this.user = payload.sub;
            this.role = payload.role;

            this.service = new PfaApi(token);
            let self = this;
            this.service.getAlertList("", "", "domainName", 100)
                .then(function(d) {
                    let dn_list = d.dn_list;
                    if (dn_list.length >= 100) {
                        self.alertCount = "99+";
                    } else {
                        self.alertCount = dn_list.length;
                    }
                })
        },
        methods: {
            logout() {
                localStorage.removeItem('jwt');
                window.location.replace('/');
            },

            setTheme() {
                this.$emit('toggleTheme');
            }
        }
    }
</script>

<style scoped>
    #navbar {
        border-bottom: solid 1px var(--border-color);
        background-color: var(--bg-color);
    }
</style>