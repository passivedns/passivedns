<template>
    <div>
        <div class="form-row">
            <div class="form-group col-md-11">
                <input id="dnImportList" class="form-control" type="file" @change="handleFileUpload($event)"/>
            </div>
            <div class="form-group col-md-1">
                <button @click="importDn" id="dnImport" type="button" class="btn btn-primary">Import</button>
            </div>
            <AuthCheck :valid="valid"
                       :loading="loading"
                       valid-msg="Domain names imported"
                       invalid-msg="Failed to import domain names"
                       loading-msg="Importing domain names"/>
        </div>
    </div>
</template>

<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../services/services.js";

    export default {
        name: "DomainNameImport",
        components: {AuthCheck},
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);
        },
        data() {
            return {
                file: null,

                loading: false,
                valid: null,
            }
        },
        methods: {
            handleFileUpload($event) {
                this.file = $event.target.files[0];
            },
            async importDn() {
                let self = this;
                if (this.file === null) {
                    return
                }

                this.loading = true;

                let formData = new FormData();
                formData.append('file', this.file);

                this.service.importDnList(formData)
                    .then(function(b) {
                        self.valid = b;
                        setTimeout(function() {
                            self.loading = false;
                            self.$emit('success');
                        }, 1000)
                    })
                    .catch(function(err) {
                        self.valid = false;
                        self.loading = false;
                    });
            }
        }
    }
</script>

<style scoped>

</style>