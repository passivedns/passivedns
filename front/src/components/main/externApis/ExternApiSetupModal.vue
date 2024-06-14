<template>
    <div class="modal fade" id="externApiModalSetup" tabindex="-1" role="dialog"
         aria-labelledby="externApiModalSetupLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content" v-if="externApi !== null">
                <div class="modal-header">
                    <h4 class="modal-title" id="externApiModalSetupLabel">{{externApi._key}}</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p class="card-text">
                        Put below your API key for {{ externApi._key }}.
                    </p>
                    <div>
                        <div class="form-group">
                            <label for="apiKeyInput">API Key</label>
                            <input id="apiKeyInput" v-model="api_key" type="text" class="form-control">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button @click="setup" type="button" class="btn btn-primary">Setup</button>
                    <AuthCheck :loading="loading" :valid="valid" valid-msg="API setup"
                               loading-msg="Setting up the API" invalid-msg="Failed to setup the API"></AuthCheck>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../services/services.js";

    export default {
        name: "ExternAPiSetupModal",
        components: {AuthCheck},
        props: {},
        data() {
            return {
                externApi: null,
                modal: null,
                api_key: "",

                loading: false,
                valid: null,
            }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById('externApiModalSetup')
            );

            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt)
        },
        methods: {
            show(externApi) {
                this.externApi = externApi;
                this.modal.show();
            },
            close() {
                this.modal.hide();
            },
            setup() {
                let self = this;
                this.loading = true;
                this.valid = null;
                this.service.setupExternApi(this.externApi._key, this.api_key)
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