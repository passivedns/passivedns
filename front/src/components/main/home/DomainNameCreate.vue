<template>
    <div>
        <div class="form-row">
            <div class="form-group col-md-11">
                <input v-model="dn" id="dnCreateInput" class="form-control" placeholder="New domain name">
            </div>
            <div class="form-group col-md-1">
                <button @click="createNewDn" id="dnCreate" type="button" class="btn btn-primary">Create</button>
            </div>
            <AuthCheck :valid="valid"
                       :loading="loading"
                       valid-msg="Domain name created"
                       invalid-msg="Failed to create domain name"
                       loading-msg="Creating domain name"/>
        </div>
    </div>
</template>

<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
    import Services from "../../../services/services.js";

    export default {
        name: "DomainNameCreate",
        components: {AuthCheck},
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);
        },
        data() {
            return {
                dn: "",

                loading: false,
                valid: null,
            }
        },
        methods: {
            createNewDn() {
                let self = this;
                if (this.dn === "") {
                    return
                }

                this.loading = true;
                this.service.createDn(this.dn)
                    .then(function(b) {
                        self.valid = b;
                        setTimeout(function() {
                            self.loading = false;
                        }, 1000)
                    })
            }
        }
    }
</script>

<style scoped>

</style>