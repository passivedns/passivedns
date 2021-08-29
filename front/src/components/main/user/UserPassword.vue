<template>
    <div class="container-sm" >
        <h3>Change password</h3>
        <form>
            <div class="form-group">
                <label for="currentPassword">Current password</label>
                <input v-model="currentPasswordInput" type="password" class="form-control" id="currentPassword">
            </div>
            <div class="form-group">
                <label for="newPassword">New password</label>
                <input v-model="newPasswordInput" type="password" class="form-control" id="newPassword">
            </div>
            <div class="form-group">
                <label for="newPasswordConfirm">Confirm</label>
                <input v-model="newPasswordConfirmInput" type="password" class="form-control" id="newPasswordConfirm">
            </div>
            <button @click="changePassword" type="button" class="btn btn-primary">Change password</button>
        </form>
        <AuthCheck
                valid-msg="Password changed"
                loading-msg="Changing password"
                :invalid-msg="invalidMessage"
                :valid="valid"
                :loading="loading"
        />
    </div>
</template>

<script>
    import AuthCheck from "@/components/connection/AuthCheck";
    import Services from "../../../services/services";
    export default {
        name: "UserPassword",
        components: {AuthCheck},
        data() {
            return {
                loading: false,
                valid: null,

                currentPasswordInput: "",
                newPasswordInput: "",
                newPasswordConfirmInput: "",

                invalidMessageDefault: "Failed to change password",
                invalidMessage: ""
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);
            this.invalidMessage = this.invalidMessageDefault;
        },
        methods: {
            changePassword() {
                let self = this;
                self.loading = true;
                self.valid = null;
                this.service.changePassword(this.currentPasswordInput, this.newPasswordConfirmInput)
                    .then(function(res) {
                        self.valid = res.b;
                        if (!res.b) {
                            self.invalidMessage = res.msg;
                        }
                        setTimeout(function() {
                            self.loading = false;
                        }, 2000)
                    })
            }
        }
    }
</script>

<style scoped>

</style>