<template>
    <div class="modal fade" id="schedulerCreateModal" tabindex="-1" role="dialog"
             aria-labelledby="schedulerCreateModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title" id="schedulerCreateModalLabel">New scheduler user</h4>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p class="card-text">
                            This creates a specific user, so that automated scheduler running on your own can register
                            to the API with safe credentials.
                        </p>
                        <div>
                            <div class="form-group">
                                <label for="schedulerName">Scheduler name</label>
                                <input id="schedulerName" v-model="schedulerName" type="text" class="form-control">
                            </div>
                            <div class="form-group">
                                <label for="schedulerPassword">Scheduler password</label>
                                <input id="schedulerPassword" v-model="schedulerPassword" type="password" class="form-control">
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        <button @click="createScheduler" type="button" class="btn btn-primary">Create</button>
                        <AuthCheck :loading="loading" :valid="valid" valid-msg="Scheduler user created"
                                   loading-msg="Creating the scheduler user" invalid-msg="Failed to create the scheduler user"></AuthCheck>
                    </div>
                </div>
            </div>
</div>
</template>

<script>
    import AuthCheck from "@/components/connection/AuthCheck";
    import PfaApiAdmin from "@/services/pfa-api-admin";

    export default {
        name: "SchedulerCreateModal",
        components: {
            AuthCheck
        },
        data() {
          return {
              loading: false,
              valid: null,

              schedulerName: "",
              schedulerPassword: "",

              modal: null,
          }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById("schedulerCreateModal")
            );
            let jwt = localStorage.getItem('jwt');
            this.service = new PfaApiAdmin(jwt);
        },
        methods: {
            show() {
                this.modal.show()
            },
            createScheduler() {
                let self = this;
                this.valid = null;
                this.loading = true;
                this.service.schedulerCreate(this.schedulerName, this.schedulerPassword)
                    .then(function(b) {
                        self.loading = false;
                        self.valid = b;
                        if (b) {
                            self.modal.hide();
                            self.$emit('schedulerCreated')
                        }
                    })
            }
        }
    }
</script>

<style scoped>

</style>