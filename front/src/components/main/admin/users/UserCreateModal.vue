<template>
    <div class="modal fade" id="userCreateModal" tabindex="-1" role="dialog"
             aria-labelledby="userCreateModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title" id="userCreateModalLabel">New user</h4>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p class="card-text">
                            This creates a new user. You can then use theses credentials to connect.
                        </p>
                        <div>
                            <div class="form-group">
                                <label for="userName">User name</label>
                                <input id="userName" v-model="userName" type="text" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label for="userPassword">Password</label>
                                <input id="userPassword" v-model="userPassword" type="password" class="form-control" required>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        <button @click="createUser" type="button" class="btn btn-primary">Create</button>
                        <AuthCheck :loading="loading" :valid="valid" valid-msg="User created"
                                   loading-msg="Creating the user" invalid-msg="Failed to create the user"></AuthCheck>
                    </div>
                </div>
            </div>
</div>
</template>

<script>
    import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../../services/services.js";

    export default {
        name: "UserCreateModal",
        components: {
            AuthCheck
        },
        data() {
          return {
              loading: false,
              valid: null,

              userName: "",
              userPassword: "",

              modal: null,
          }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById("userCreateModal")
            );
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiAdminService(jwt);
        },
        methods: {
            show() {
                this.modal.show()
            },
            createUser() {
                let self = this;
                this.valid = null;
                this.loading = true;
                this.service.userCreate(this.userName, this.userPassword)
                    .then(function(b) {
                        self.loading = false;
                        self.valid = b;
                        if (b) {
                            self.modal.hide();
                            self.$emit('userCreated')
                        }
                    })
            }
        }
    }
</script>

<style scoped>

</style>