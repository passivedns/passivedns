<template>
    <div class="col">
        <div class="container mb-3">
            <h3>{{details.dn._key}}</h3>
            <span @click="manageTags" class="badge badge-primary m-1 badge-button">+</span>
            <span class="badge badge-primary m-1"
                  v-for="t in details.dn_tags" :key="t">{{t}}</span>
            <TagManageModal @refresh="refresh" ref="tagManageModal" type="DomainName"
                            :object="details.dn._key" id="TagManageDN"/>
        </div>
        <div class="container">
            <div class="row m-2">Registered at <span class="font-weight-bold ml-2">{{details.dn.registrar}}</span></div>
            <div class="row m-2" v-for="(r, index) in recordsList" :key="`${r.type}-${index}`">
                <div class="col"><h5><span class="badge badge-secondary">{{r.type}}</span></h5></div>
                <div class="col">
                    <div v-if="r.type === 'A'">
                        <div class="row text-muted">Address</div>
                    </div>
                    <div v-else-if="r.type === 'AAAA'">
                        <div class="row text-muted">Address</div>
                    </div>
                    <div v-else-if="r.type === 'NS'">
                        <div class="row text-muted">Target</div>
                    </div>
                    <div v-else-if="r.type === 'SOA'">
                        <div class="row text-muted">Expire</div>
                        <div class="row text-muted">Minimum</div>
                        <div class="row text-muted">Mname</div>
                        <div class="row text-muted">Refresh</div>
                        <div class="row text-muted">Retry</div>
                        <div class="row text-muted">Rname</div>
                        <div class="row text-muted">Serial</div>
                    </div>
                    <div v-else-if="r.type === 'MX'">
                        <div class="row text-muted">Exchange</div>
                        <div class="row text-muted">Preference</div>
                    </div>
                    <div v-else-if="r.type === 'TXT'">
                        <div class="row text-muted">Strings</div>
                    </div>
                </div>
                <div class="col">
                    <div v-if="r.type === 'A'">
                        <div class="row">{{r.address}}</div>
                    </div>
                    <div v-else-if="r.type === 'AAAA'">
                        <div class="row">{{r.address}}</div>
                    </div>
                    <div v-else-if="r.type === 'NS'">
                        <div class="row">{{r.target}}</div>
                    </div>
                    <div v-else-if="r.type === 'SOA'">
                        <div class="row">{{r.expire}}</div>
                        <div class="row">{{r.minimum}}</div>
                        <div class="row">{{r.mname}}</div>
                        <div class="row">{{r.refresh}}</div>
                        <div class="row">{{r.retry}}</div>
                        <div class="row">{{r.rname}}</div>
                        <div class="row">{{r.serial}}</div>
                    </div>
                    <div v-else-if="r.type === 'MX'">
                        <div class="row">{{r.exchange}}</div>
                        <div class="row">{{r.preference}}</div>
                    </div>
                    <div v-else-if="r.type === 'TXT'">
                        <div class="row">{{r.strings}}</div>
                    </div>
                </div>
            </div>
            <div class="container">
                <span class="badge badge-secondary m-2"
                      v-for="(r, index) in unparsedRecordsList"
                      :key="`${r.type}-${index}`">
                    {{r.type}}
                </span>
            </div>
        </div>
    </div>
</template>

<script>
    import TagManageModal from "@/components/main/home/TagManageModal.vue";
    export default {
        name: "DomainNameDetailPageDn",
        components: {TagManageModal},
        props: {
            details: Object
        },
        computed: {
            recordsList() {
                let supportedRecords = [
                    'A', 'AAAA', 'NS', 'SOA', 'MX', 'TXT'
                ];

                let records = [];
                this.details.dn.records.forEach(function(r) {
                    if (supportedRecords.indexOf(r.type) !== -1) {
                        records.push(r)
                    }
                });

                return records
            },
            unparsedRecordsList() {
                let supportedRecords = [
                    'A', 'AAAA', 'NS', 'SOA', 'MX', 'TXT'
                ];

                let records = [];
                this.details.dn.records.forEach(function(r) {
                    if (supportedRecords.indexOf(r.type) === -1) {
                        records.push(r)
                    }
                });

                return records
            },
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