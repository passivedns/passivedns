<template>
    <div class="modal fade" id="channelModalCreate" tabindex="-1" role="dialog"
         aria-labelledby="channelModalCreateLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title" id="channelModalCreateLabel">Channel creation</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div>
                        <div class="form-group">
                            <label for="channelCreateName">Channel name</label>
                            <input v-model="channelName" type="text" class="form-control" id="channelCreateName" required>
                        </div>

                        <div class="form-group">
                            <label for="channelTypeSelect" class="sr-only">Channel type select</label>
                            <select v-model="channelType" class="custom-select" id="channelTypeSelect">
                                <option :value="channelTypeRedis">Redis</option>
                            </select>
                        </div>

                    </div>

                    <form v-if="channelType === channelTypeRedis">
                        <div class="form-group">
                            <label for="database">Database</label>
                            <input v-model="channelInfos.db" type="text" class="form-control" id="database" required>
                        </div>
                        <div class="form-group">
                            <label for="host">Host</label>
                            <input v-model="channelInfos.host" type="text" class="form-control" id="host" value="redis" required>
                        </div>
                        <div class="form-group">
                            <label for="senderEmail">Port</label>
                            <input v-model="channelInfos.port" type="text" class="form-control" id="senderEmail" value="6379" required>
                        </div>
                        <div class="form-group">
                            <label for="queueName">Queue name</label>
                            <input v-model="channelInfos.queue_name" type="text" class="form-control" id="queueName" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input v-model="channelInfos.password" type="password" class="form-control" id="password">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button @click="createChannel" type="button" class="btn btn-primary">Create</button>
                    <AuthCheck :loading="loading" :valid="valid" valid-msg="Channel created" invalid-msg="Failed to create channel" loading-msg="Creating channel"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../../services/services.js";

    export default {
        name: "AdminChannelModalCreate",
        components: {
            AuthCheck
        },
        props: {
            channelTypeRedis: String
        },
        data() {
            return {
                loading: false,
                valid: null,

                channelName: "",
                channelInfos: {},
                channelType: "",

                modal: null,
            }
        },
        mounted() {
            this.channelType = this.channelTypeEmail;

            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiAdminService(jwt);

            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById('channelModalCreate')
            )

        },
        methods: {
            createChannel() {
                let self = this;
                this.loading = true;
                this.valid = null;
                this.service.channelCreate(this.channelName, this.channelInfos, this.channelType)
                    .then(function(b) {
                        self.valid = b;

                        if (b) {
                            self.loading = false;
                            self.modal.hide();
                            self.$emit('created')
                        }
                    })
            },
            show() {
                this.modal.show();
            }
        }
    }
</script>

<style scoped>

</style>