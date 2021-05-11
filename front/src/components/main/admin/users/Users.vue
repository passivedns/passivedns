<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="btn-group btn-group-toggle" data-toggle="buttons">
                <label class="btn btn-primary active">
                    <input type="radio" name="options" id="option1" @click="tab = tabUsers" checked> Users
                </label>
                <label class="btn btn-primary">
                    <input type="radio" name="options" id="option2" @click="tab = tabInvitations"> Invitations
                </label>
                <label class="btn btn-primary">
                    <input type="radio" name="options" id="option3" @click="tab = tabRequests"> Requests
                    <span v-if="requestList.length > 0" class="badge badge-light">{{requestList.length}}</span>
                </label>
            </div>
        </div>
        <div class="container">
            <UsersList v-if="tab === tabUsers" @remove="removeUser" :user-list="userList" @schedulerCreated="refreshList"/>
            <UsersInvite v-else-if="tab === tabInvitations" @invite="invite" :invite-list="inviteList"/>
            <UsersRequest v-else-if="tab === tabRequests" @remove="removeRequest" @verify="verify" :request-list="requestList"/>
        </div>
    </div>
</template>

<script>
    import PfaApiAdmin from "@/services/pfa-api-admin";
    import UsersList from "@/components/main/admin/users/UsersList";
    import UsersInvite from "@/components/main/admin/users/UsersInvite";
    import UsersRequest from "@/components/main/admin/users/UsersRequest";

    export default {
        name: "Users",
        components: {UsersRequest, UsersInvite, UsersList},
        data() {
            return {
                userList: [],
                requestList: [],
                inviteList: [],

                tabUsers: "users",
                tabInvitations: "invitations",
                tabRequests: "requests",
                tab: "users"
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = new PfaApiAdmin(jwt);
            this.refreshList();
        },
        methods: {
            refreshList() {
                let self = this;
                this.service.inviteList()
                    .then(function(d) {
                        self.inviteList = d
                    });

                this.service.requestList()
                    .then(function(d) {
                        self.requestList = d
                    });

                this.service.userList()
                    .then(function(d) {
                        self.userList = d
                    })
            },

            verify(email) {
                let self = this;
                this.service.verify(email)
                    .then(function() {
                        self.refreshList();
                    })
            },

            invite(email) {
                let self = this;
                this.service.invite(email)
                    .then(function() {
                        self.refreshList()
                    })
            },

            removeUser(username) {
                let self = this;
                this.service.userDelete(username)
                    .then(function() {
                        self.refreshList()
                    })
            },

            removeRequest(email) {
                let self = this;
                this.service.requestDelete(email)
                    .then(function() {
                        self.refreshList()
                    })
            },
        }
    }
</script>

<style scoped>

</style>