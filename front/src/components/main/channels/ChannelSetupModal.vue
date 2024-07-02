<template>
    <div class="modal fade" id="channelModalSetup" tabindex="-1" role="dialog"
         aria-labelledby="channelModalSetupLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content" v-if="channel !== null">
                <div class="modal-header">
                    <h4 class="modal-title" id="channelModalSetupLabel">{{channel._key}}</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p class="card-text" v-if="channel.type === channelTypeEmail">
                        This channel allows you to be alerted by email.
                        Put right below the email with which you want to be alerted.
                    </p>
                    <p class="card-text" v-else-if="channel.type === channelTypeTelegram">
                        This channel allows you to be alerted via Telegram.
                        Put right below the chat ID where you want to be alerted.
                        It can be a group chat or an individual chat.
                    </p>
                    <p class="card-text" v-else-if="channel.type === channelTypeDiscord">
                        This channel allows you to be alerted via Discord.
                        Put right below your user ID (it should be a number of 18 digits).
                    </p>
                    <div>
                        <div class="form-group">
                            <label v-if="channel.type === channelTypeEmail" for="contactInput">Email</label>
                            <label v-else-if="channel.type === channelTypeTelegram" for="contactInput">Chat ID</label>
                            <input id="contactInput" v-model="contact" type="text" class="form-control" required>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button @click="setup" type="button" class="btn btn-primary">Setup</button>
                    <AuthCheck :loading="loading" :valid="valid" valid-msg="Channel setup"
                               loading-msg="Setting up the channel" invalid-msg="Failed to setup the channel"></AuthCheck>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../services/services.js";

    export default {
        name: "ChannelSetupModal",
        components: {AuthCheck},
        props: {
            channelTypeEmail: String,
            channelTypeTelegram: String,
            channelTypeDiscord: String,
        },
        data() {
            return {
                channel: null,
                modal: null,
                contact: "",

                loading: false,
                valid: null,
            }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById('channelModalSetup')
            );

            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt)
        },
        methods: {
            show(channel) {
                this.channel = channel;
                this.modal.show();
            },
            close() {
                this.modal.hide();
            },
            setup() {
                let self = this;
                this.loading = true;
                this.valid = null;
                this.service.setupChannel(this.channel._key, this.contact)
                    .then(function(b) {
                        self.valid = b;

                        if (b) {
                            self.loading = false;
                            self.close();
                            self.$emit('success')
                        }
                    })
            }
        }
    }
</script>

<style scoped>

</style>