<template>
    <div class="modal fade" id="channelModalVerify" tabindex="-1" role="dialog"
         aria-labelledby="channelModalVerifyLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content" v-if="channel !== null">
                <div class="modal-header">
                    <h4 class="modal-title" id="channelModalVerifyLabel">{{channel._key}}</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div>
                        <div class="form-group">
                            <label for="tokenInput">Validation token</label>
                            <input id="tokenInput" v-model="token" type="password" class="form-control">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button @click="verify" type="button" class="btn btn-primary">Verify</button>
                    <AuthCheck :loading="loading" :valid="valid" valid-msg="Token verified"
                               loading-msg="Verifying" invalid-msg="Invalid token"></AuthCheck>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import PfaApi from "@/services/pfa-api";
    import AuthCheck from "@/components/connection/AuthCheck";

    export default {
        name: "ChannelVerifyModal",
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
                channel: null,
                modal: null,
                token: "",
                loading: false,
                valid: null,
            }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById('channelModalVerify')
            );

            let jwt = localStorage.getItem('jwt');
            this.service = new PfaApi(jwt);
        },
        methods: {
            show(channel) {
                this.channel = channel;
                this.modal.show();
            },
            close() {
                this.modal.hide();
            },
            verify() {
                let self = this;
                this.loading = true;
                this.valid = null;
                this.service.verifyChannel(this.channel._key, this.token)
                    .then(function(b) {
                        self.valid = b;
                        if (b) {
                            self.loading = false;
                            self.close();
                            self.$emit('success');
                        }
                    })
            }
        }
    }
</script>

<style scoped>

</style>