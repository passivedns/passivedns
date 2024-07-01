<template>
    <div class="modal fade" id="channelModalUpdate" tabindex="-1" role="dialog"
         aria-labelledby="channelModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content" v-if="channel !== null">
                <div class="modal-header">
                    <span class="mr-2">
                        <img class="light" src="../../../../assets/icons/icons8-mail-48.png" alt="mail">
                    </span>
                    <h4 class="modal-title" id="channelModalLabel">{{channel._key}}</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form v-if="channel.type === channelTypeEmail">
                        <div class="form-group">
                            <label for="smtpHost">SMTP host</label>
                            <input v-model="channel.infos.smtp_host" type="text" class="form-control" id="smtpHost">
                        </div>
                        <div class="form-group">
                            <label for="smtpPort">SMTP port</label>
                            <input v-model="channel.infos.smtp_port" type="text" class="form-control" id="smtpPort">
                        </div>
                        <div class="form-group">
                            <label for="senderEmail">Sender email</label>
                            <input v-model="channel.infos.sender_email" type="email" class="form-control" id="senderEmail">
                        </div>
                        <div class="form-group">
                            <label for="senderPassword">Password</label>
                            <input v-model="channel.infos.sender_password" type="password" class="form-control" id="senderPassword">
                        </div>
                    </form>
                    <form v-else-if="channel.type === channelTypeTelegram">
                        <div class="form-group">
                            <label for="botToken">Bot token</label>
                            <div class="input-group">
                                <input v-model="channel.infos.bot_token" type="password" class="form-control" id="botToken">
                                <div class="input-group-append">
                                    <button @mousedown="showBotToken('botToken')" @mouseup="hideBotToken('botToken')" class="btn btn-outline-primary" type="button">
                                        <img class="light" src="../../../../assets/icons/icons8-eye-30.png" alt="eye">
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>
                    <form v-else-if="channel.type === channelTypeDiscord">
                        <div class="form-group">
                            <label for="discordBotToken">Bot token</label>
                            <div class="input-group">
                                <input v-model="channel.infos.bot_token" type="password" class="form-control" id="discordBotToken">
                                <div class="input-group-append">
                                    <button @mousedown="showBotToken('discordBotToken')" @mouseup="hideBotToken('discordBotToken')" class="btn btn-outline-primary" type="button">
                                        <img class="light" src="../../../../assets/icons/icons8-eye-30.png" alt="eye">
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>
                    <form v-else-if="channel.type === channelTypeRedis">
                        <div class="form-group">
                            <label for="redisDatabase">Database</label>
                            <input v-model="channel.infos.db" type="text" class="form-control" id="redisDatabase">
                        </div>
                        <div class="form-group">
                            <label for="redisHost">Host</label>
                            <input v-model="channel.infos.host" type="text" class="form-control" id="redisHost">
                        </div>
                        <div class="form-group">
                            <label for="redisPort">Port</label>
                            <input v-model="channel.infos.port" type="text" class="form-control" id="redisPort">
                        </div>
                        <div class="form-group">
                            <label for="redisQueueName">Queue name</label>
                            <input v-model="channel.infos.queue_name" type="text" class="form-control" id="redisQueueName">
                        </div>
                        <div class="form-group">
                            <label for="redisPassword">Password</label>
                            <input v-model="channel.infos.password" type="password" class="form-control" id="redisPassword">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button @click="updateChannel" type="button" class="btn btn-primary">Save</button>
                    <AuthCheck :loading="loading" :valid="valid" valid-msg="Channel updated" invalid-msg="Failed to update channel" loading-msg="Updating channel"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../../services/services.js";

    export default {
        name: "AdminChannelModal",
        components: {AuthCheck},
        props: {
            channelTypeEmail: String,
            channelTypeTelegram: String,
            channelTypeDiscord: String,
            channelTypeRedis: String,
        },
        data() {
            return {
                channel: null,
                modal: null,

                loading: false,
                valid: null,
            }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById('channelModalUpdate')
            );
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiAdminService(jwt);
        },
        methods: {
            updateChannel() {
                let self = this;
                this.loading = true;
                this.valid = null;
                this.service.channelUpdate(this.channel._key, this.channel.infos)
                    .then(function(b) {
                        self.valid = b;

                        if (b) {
                            self.loading = false;
                            self.modal.hide();
                            self.$emit('updated');
                        }
                    })
            },
            select(channel) {
                this.channel = channel;
                this.modal.show();
            },

            showBotToken(inputId) {
                let i = document.getElementById(inputId);
                i.type = 'text';
            },

            hideBotToken(inputId) {
                let i = document.getElementById(inputId);
                i.type = 'password';
            }
        }
    }
</script>

<style scoped>

</style>