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
                            <input v-model="channelName" type="text" class="form-control" id="channelCreateName">
                        </div>

                        <div class="form-group">
                            <label for="channelTypeSelect" class="sr-only">Channel type select</label>
                            <select v-model="channelType" class="custom-select" id="channelTypeSelect">
                                <option :value="channelTypeEmail">Email</option>
                                <option :value="channelTypeTelegram">Telegram</option>
                                <option :value="channelTypeDiscord">Discord</option>
                            </select>
                        </div>

                    </div>

                    <form v-if="channelType === channelTypeEmail">
                        <div class="form-group">
                            <label for="smtpHost">SMTP host</label>
                            <input v-model="channelInfos.smtp_host" type="text" class="form-control" id="smtpHost">
                        </div>
                        <div class="form-group">
                            <label for="smtpPort">SMTP port</label>
                            <input v-model="channelInfos.smtp_port" type="text" class="form-control" id="smtpPort">
                        </div>
                        <div class="form-group">
                            <label for="senderEmail">Sender email</label>
                            <input v-model="channelInfos.sender_email" type="email" class="form-control" id="senderEmail">
                        </div>
                        <div class="form-group">
                            <label for="senderPassword">Password</label>
                            <input v-model="channelInfos.sender_password" type="password" class="form-control" id="senderPassword">
                        </div>
                    </form>
                    <form v-else-if="channelType === channelTypeTelegram">
                        <div class="form-group">
                            <label for="botToken">Bot token</label>
                            <input v-model="channelInfos.bot_token" type="text" class="form-control" id="botToken">
                        </div>
                    </form>
                    <form v-else-if="channelType === channelTypeDiscord">
                        <div class="form-group">
                            <label for="discordBotToken">Bot token</label>
                            <input v-model="channelInfos.bot_token" type="text" class="form-control" id="discordBotToken">
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
            channelTypeEmail: String,
            channelTypeTelegram: String,
            channelTypeDiscord: String,
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