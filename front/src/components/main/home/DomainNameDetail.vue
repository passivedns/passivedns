<template>
    <div>
        <div v-if="selectedDnData !== null" class="row m-3">
            <div class="col">
                <small class="row text-muted">DN infos</small>
                <div class="row">Registered in
                    <span class="ml-2 font-weight-bold font-monospace">{{selectedDnData.dn.registrar}}</span>
                </div>
                <div class="row">
                    <span v-for="(r, index) in selectedDnData.dn.records" :key="`${r.type}-${index}`" class="badge badge-secondary m-1">
                        {{r.type}}
                    </span>
                </div>
            </div>
            <div v-if="selectedDnData.ip !== null" class="col">
                <small class="row text-muted">IP infos</small>
                <div class="row">Hosted in
                    <a :href="googleMapLink" target="_blank" class="ml-2">
                        {{selectedDnData.ip.location.city}}, {{selectedDnData.ip.location.zip_code}}, {{selectedDnData.ip.location.country}}
                    </a>
                </div>
                <div class="row">
                    ISP
                    <span class="ml-2 mr-2 font-weight-bold font-monospace">{{selectedDnData.ip.location.ISP}}</span>
                    hosted by
                    <span class="ml-2 font-weight-bold font-monospace">{{selectedDnData.ip.location.organization}}</span>
                </div>
                <div class="row text-muted">
                    {{selectedDnData.ip.location.AS}}
                </div>
            </div>
        </div>
        <span v-else class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    </div>
</template>

<script>
    export default {
        name: "DomainNameDetail",
        props: {
            selectedDnData: Object,
        },
        computed: {
            googleMapLink() {
                let lat = this.selectedDnData.ip.location.latitude;
                let lon = this.selectedDnData.ip.location.longitude;
                return `https://google.com/maps/place/${lat} ${lon}`

            }
        }
    }
</script>

<style scoped>

</style>