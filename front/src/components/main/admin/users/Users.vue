<template>
    <div class="container">
        <div class="container">
            <UsersList @remove="removeUser" :user-list="userList" @schedulerCreated="refreshList" @userCreated="refreshList"/>
        </div>
    </div>
</template>

<script>
import UsersList from "@/components/main/admin/users/UsersList.vue";
    import Services from "../../../../services/services.js";

    export default {
        name: "Users",
        components: {UsersList},
        data() {
            return {
                userList: [],
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiAdminService(jwt);
            this.refreshList();
        },
        methods: {
            refreshList() {
                let self = this;
                this.service.userList()
                    .then(function(d) {
                        self.userList = d
                    })
            },

            removeUser(username) {
                let self = this;
                this.service.userDelete(username)
                    .then(function() {
                        self.refreshList()
                    })
            },
        }
    }
</script>

<style scoped>

</style>