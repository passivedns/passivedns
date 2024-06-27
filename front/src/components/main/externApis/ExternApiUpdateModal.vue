<template>
    <div class="modal fade" id="externApiUpdateModal" tabindex="-1" role="dialog"
         aria-labelledby="externApiModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content" v-if="externApi !== null">
                <div class="modal-header">
                    <h4 class="modal-title" id="externApiModalLabel">{{externApi._key}}</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group">
                            <label for="baseUrl">Base URL</label>
                            <input v-model="externApi.base_url" type="text" class="form-control" id="baseUrl">
                        </div>
                        <div class="form-group">
                            <label for="apiHeader">Header</label>
                            <input v-model="externApi.header" type="text" class="form-control" id="apiHeader">
                        </div>
                        <div class="form-group">
                            IP
                            <label for="ipMethod">IP Method</label>
                            <select id="ipMethod" v-model="externApi.ip_method" class="form-control">
                                <option value="GET">GET</option>
                                <option value="POST">POST</option>
                            </select>
                            <label for="ipUri">IP URI</label>
                            <input v-model="externApi.ip_uri" type="text" class="form-control" id="ipUri">
                        </div>
                        <div class="form-group">
                            <label for="dnMethod">Domain Method</label>
                            <select id="dnMethod" v-model="externApi.domain_method" class="form-control">
                                <option value="GET">GET</option>
                                <option value="POST">POST</option>
                            </select>
                            <label for="dnUri">Domain URI</label>
                            <input v-model="externApi.domain_uri" type="text" class="form-control" id="dnUri">
                        </div>
                        
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button @click="updateApi" type="button" class="btn btn-primary">Save</button>
                    <AuthCheck :loading="loading" :valid="valid" valid-msg="API updated" invalid-msg="Failed to update API" loading-msg="Updating API"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../services/services.js";

    export default {
        name: "ExternApiUpdateModal",
        components: {AuthCheck},
        data() {
            return {
                externApi: null,
                modal: null,

                loading: false,
                valid: null,
            }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById('externApiUpdateModal')
            );
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);
        },
        methods: {
            show(externApi) {
                this.externApi = externApi;
                this.modal.show();
            },
            updateApi() {
                let self = this;
                this.loading = true;
                this.valid = null;
                this.service.externApiUpdate(this.externApi)
                    .then(function(b) {
                        self.valid = b;

                        if (b) {
                            self.loading = false;
                            self.modal.hide();
                            self.$emit('updated');
                        }
                    })
            },
        }
    }
</script>

<style scoped>

</style>