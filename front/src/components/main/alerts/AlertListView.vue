<template>
    <div>
        <div v-if="displayedDnList.length > 0">

            <div class="row m-2">
                <div class="col-"><img class="light" src="../../../assets/icons/icons8-expand-arrow-26-muted.png" alt="expand"></div>
                <div class="col font-weight-bold">Domain name</div>
                <div class="col font-weight-bold">DN tags</div>
                <div class="col font-weight-bold">Last IP address</div>
                <div class="col font-weight-bold">Last IP tags</div>
                <div class="col font-weight-bold">Current IP address</div>
                <div class="col font-weight-bold">Current IP tags</div>
            </div>

            <div v-for="dn in displayedDnList" :key="dn.domain_name" class="border-top">
                <div class="row align-items-center m-2">
                    <div class="col-">
                        <span v-if="selectedDn === dn.domain_name" class="expand" @click="collapseDn">
                            <img class="light" src="../../../assets/icons/icons8-collapse-arrow-26.png" alt="collapse">
                        </span>
                        <span v-else @click="expandDn(dn.domain_name)" class="expand">
                            <img class="light" src="../../../assets/icons/icons8-expand-arrow-26.png" alt="expand">
                        </span>
                    </div>

                    <div class="col">
                        <router-link :to="`/dn/${dn.domain_name}`">
                            {{formatDn(dn.domain_name)}}
                        </router-link>
                    </div>

                    <div class="col">
                        <span class="badge badge-primary mr-1" v-for="t in dn.domain_name_tags" :key="t">{{t}}</span>
                    </div>

                    <div class="col text-muted" v-if="dn.last_ip_address === null">No resolution found</div>
                    <div class="col" v-else>{{dn.last_ip_address}}</div>

                    <div class="col">
                        <span class="badge badge-primary mr-1" v-for="t in dn.last_ip_tags" :key="t">{{t}}</span>
                    </div>

                    <div class="col text-muted" v-if="dn.current_ip_address === null">No resolution found</div>
                    <div class="col" v-else>{{dn.current_ip_address}}</div>

                    <div class="col">
                        <span class="badge badge-primary mr-1" v-for="t in dn.current_ip_tags" :key="t">{{t}}</span>
                    </div>
                </div>

                <DomainNameDetail :selected-dn-data="selectedDnData" v-if="selectedDn === dn.domain_name"/>
            </div>

            <div class="d-flex justify-content-center" style="margin-top: 30px">
                <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with page indexes">
                    <div class="btn-group" role="group" aria-label="First group">
                        <button class="btn btn-primary btn-index" @click="pageIndexFirst">&lt;&lt;</button>
                        <button class="btn btn-primary btn-index" @click="pageIndexPrevious">&lt;</button>
                        <button class="btn btn-primary btn-index" v-for="i in pageIndexes" :key="i" @click="pageIndex = i">{{i + 1}}</button>
                        <button class="btn btn-primary btn-index" @click="pageIndexNext">&gt;</button>
                        <button class="btn btn-primary btn-index" @click="pageIndexLast">&gt;&gt;</button>
                    </div>
                </div>
            </div>

        </div>
        <div v-else class="text-muted">
            No record found
        </div>
    </div>
</template>

<script>
    import DomainNameDetail from "@/components/main/home/DomainNameDetail.vue";
    import DateUtil from "@/services/date-util.js";
    import StringUtil from "@/services/string-util.js";
    import Services from "../../../services/services.js";

    export default {
        name: "AlertListView",
        components: {DomainNameDetail},
        props: {
            dnList: Array,
        },
        computed: {
            displayedDnList() {
                if (this.dnList !== null) {
                    let firstIndex = this.pageIndex * this.dnPerPage;
                    let endIndex = firstIndex + this.dnPerPage;
                    return this.dnList.slice(firstIndex, endIndex)
                } else {
                    return null
                }
            },
            pageIndexes() {
                let pageCount = Math.floor(this.dnList.length / this.dnPerPage);
                if (this.dnList.length % this.dnPerPage > 0) {
                    pageCount += 1;
                }
                let indexes = [];
                for (let i = 0; i < pageCount; i++) {
                    indexes.push(i)
                }

                return indexes
            }
        },
        data() {
            return {
                pageIndex: 0,
                dnPerPage: 10,
                selectedDn: "",
                selectedDnData: null,
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);
        },
        methods: {
            pageIndexLast() {
                this.pageIndex = this.pageIndexes.length - 1;
            },

            pageIndexFirst() {
                this.pageIndex = 0;
            },

            pageIndexNext() {
                if (this.pageIndex < this.pageIndexes.length - 1) {
                    this.pageIndex += 1;
                }
            },

            pageIndexPrevious() {
                if (this.pageIndex > 0) {
                    this.pageIndex -= 1;
                }
            },
            expandDn(domainName) {
                let self = this;
                this.selectedDn = domainName;
                this.selectedDnData = null;

                this.service.getDn(domainName)
                    .then(function (d) {
                        self.selectedDnData = d;
                    })
            },

            collapseDn() {
                this.selectedDn = "";
                this.selectedDnData = null;
            },

            formatDate(d) {
                return DateUtil.formatDiffNow(d)
            },
            formatDn(dn) {
                return StringUtil.formatDn(dn)
            }
        }
    }
</script>

<style scoped>
    .expand {
        cursor: pointer
    }

    .btn-index {
        padding: 2px 10px;
    }
</style>