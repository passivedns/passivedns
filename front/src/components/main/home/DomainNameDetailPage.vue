<template>
    <div class="container">
        <div class="row" v-if="details !== null">
            <DomainNameDetailPageDn @refresh="getDn" :details="details"/>
            <div class="col">
                <DomainNameDetailPageIP @refresh="getDn" v-if="details.ip !== null" :details="details"/>
                <div class="row text-muted" v-else>
                    <div class="col"><h3>No resolution found</h3></div>
                </div>

                <DomainNameDetailPageHistory v-if="history !== null" :history="history"/>
            </div>
        </div>
        <span v-else class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    </div>
</template>

<script>
import DomainNameDetailPageDn from "@/components/main/home/DomainNameDetailPageDn.vue";
    import DomainNameDetailPageIP from "@/components/main/home/DomainNameDetailPageIP.vue";
    import DomainNameDetailPageHistory from "@/components/main/home/DomainNameDetailPageHistory.vue";
    import Services from "../../../services/services.js";

    export default {
        name: "DomainNameDetailPage",
        components: {DomainNameDetailPageHistory, DomainNameDetailPageIP, DomainNameDetailPageDn},
        data() {
            return {
                dn: "",
                details: null,
                history: null,
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);

            this.dn = this.$route.params.dn;
            this.getDn();
            this.getIpHistory();
        },
        methods: {
            getDn() {
                let self = this;
                this.service.getDn(this.dn)
                    .then(function(details) {
                        self.details = details;
                    })
            },
            getIpHistory() {
                let self = this;
                this.service.getDnHistory(this.dn)
                    .then(function(history) {
                        self.history = history;
                    })
            }
        }
    }
</script>

<style scoped>

</style>