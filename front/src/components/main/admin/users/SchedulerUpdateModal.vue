<template>
    <div class="modal fade" id="schedulerUpdateModal" tabindex="-1" role="dialog"
         aria-labelledby="schedulerUpdateModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title" id="schedulerUpdateModalLabel">{{schedulerName}}</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div>
                        <div class="form-group">
                            <label for="schedulerNewPassword">New password</label>
                            <input id="schedulerNewPassword" v-model="schedulerPassword" type="password" class="form-control">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button @click="updateScheduler" type="button" class="btn btn-primary">Create</button>
                    <AuthCheck :loading="loading" :valid="valid" valid-msg="Password changed"
                               loading-msg="Changing password" invalid-msg="Failed to change the password"></AuthCheck>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../../services/services.js";

    export default {
        name: "SchedulerUpdateModal",
        components: {
            AuthCheck
        },
        data() {
            return {
                schedulerPassword: "",

                loading: false,
                valid: null,

                schedulerName: "",
            }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById('schedulerUpdateModal')
            );

            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiAdminService(jwt)
        },
        methods: {
            show(schedulerName) {
                this.schedulerName = schedulerName;
                this.modal.show()
            },
            updateScheduler() {
                let self = this;
                self.loading = true;
                self.valid = null;
                this.service.schedulerUpdate(this.schedulerName, this.schedulerPassword)
                    .then(function(b) {
                        self.valid = b;
                        self.loading = false;
                        if (b) {
                            self.modal.hide();
                        }

                    })
            }
        }
    }
</script>

<style scoped>

</style>