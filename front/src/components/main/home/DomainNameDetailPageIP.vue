<template>
    <div class="row mb-5">
        <div class="container mb-3">
            <h3>{{details.ip._key}}</h3>
            <span @click="manageTags" class="badge badge-primary m-1 badge-button">+</span>
            <span @click="manageTags" class="badge badge-primary m-1"
                  v-for="t in details.ip_tags" :key="t">{{t}}</span>
            <TagManageModal @refresh="refresh" ref="tagManageModal" type="IPAddress"
                            :object="details.ip._key" id="TagMaageIP"/>
        </div>
        <div class="container">
            <div class="row">
                <div class="col-3">Hosted by</div>
                <div class="col"><span class="font-weight-bold">{{details.ip.location.organization}}</span></div>
            </div>
            <div class="row">
                <div class="col-3">Own by</div>
                <div class="col"><span class="font-weight-bold">{{details.ip.location.ISP}}</span></div>
            </div>
            <div class="row">
                <div class="col-3">Located at</div>
                <div class="col">
                    <a :href="googleMapLink" target="_blank">
                        {{details.ip.location.city}},
                        {{details.ip.location.zip_code}},
                        {{details.ip.location.region_name}},
                        {{details.ip.location.country}}
                    </a>
                </div>
            </div>
            <div class="row">
                <div class="col-3">AS server</div>
                <div class="col"><span class="font-weight-bold">{{details.ip.location.AS}}</span></div>
            </div>
            <div class="row">
                <div class="col-3">Resolver</div>
                <div class="col"><span class="font-weight-bold">{{details.resolver}}</span></div>
            </div>
        </div>
    </div>
</template>

<script>
    import TagManageModal from "@/components/main/home/TagManageModal.vue";
    export default {
        name: "DomainNameDetailPageIP",
        components: {TagManageModal},
        props: {
            details: Object
        },
        computed: {
            googleMapLink() {
                let lat = this.details.ip.location.latitude;
                let lon = this.details.ip.location.longitude;
                return `https://google.com/maps/place/${lat} ${lon}`

            }
        },
        methods: {
            manageTags() {
                this.$refs.tagManageModal.show()
            },
            refresh() {
                this.$emit('refresh')
            }
        }
    }
</script>

<style scoped>
    .badge-button {
        cursor: pointer;
    }
</style>