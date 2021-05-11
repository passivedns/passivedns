<template>
    <div>
        <div v-if="displayedDnList.length > 0">

            <div class="row m-2">
                <div class="col-"><img class="light" src="../../../assets/icons/icons8-expand-arrow-26-muted.png" alt="expand"></div>
                <div class="col font-weight-bold">Domain name</div>
                <div class="col font-weight-bold">DN tags</div>
                <div class="col font-weight-bold">IP address</div>
                <div class="col font-weight-bold">IP tags</div>
                <div class="col font-weight-bold">Last ip change</div>
                <div class="col font-weight-bold">Status</div>
                <div class="col font-weight-bold">Edit</div>
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

                    <div class="col text-muted" v-if="dn.ip_address === null">No resolution</div>
                    <div class="col" v-else>{{dn.ip_address}}</div>

                    <div class="col">
                        <span class="badge badge-primary mr-1" v-for="t in dn.ip_address_tags" :key="t">{{t}}</span>
                    </div>

                    <div class="col text-muted" v-if="dn.last_ip_change === null">No resolution</div>
                    <div class="col" v-else>{{formatDate(dn.last_ip_change)}}</div>

                    <div class="col">
                        <span v-if="dn.owned" class="badge badge-success">owned</span>
                        <span v-else-if="dn.followed" class="badge badge-primary">followed</span>
                        <span v-else class="badge badge-secondary">not followed</span>
                    </div>

                    <div class="col">
                        <button @click="deleteDn(dn.domain_name)" v-if="dn.owned" class="btn btn-danger" style="padding: 2px">
                            <img src="../../../assets/icons/icons8-remove-24.png" alt="remove">
                        </button>
                        <button @click="followDn(dn.domain_name)" v-else-if="!dn.followed" class="btn btn-primary" style="padding: 2px">
                            <img src="../../../assets/icons/icons8-like-24.png" width="18px" alt="follow">
                        </button>
                        <button @click="unfollowDn(dn.domain_name)" v-else class="btn btn-danger" style="padding: 2px">
                            <img src="../../../assets/icons/icons8-unfollow-24.png" width="18px" alt="unfollow">
                        </button>
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
    import DomainNameDetail from "@/components/main/home/DomainNameDetail";
    import DateUtil from "@/services/date-util";
    import PfaApi from "@/services/pfa-api";
    import StringUtil from "@/services/string-util";

    export default {
        name: "DomainNameListView",
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
            this.service = new PfaApi(jwt);
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

            followDn(domainName) {
                let self = this;
                this.service.follow(domainName)
                    .then(function() {
                        self.$emit('refresh')
                    })
            },

            unfollowDn(domainName) {
                let self = this;
                this.service.unfollow(domainName)
                    .then(function() {
                        self.$emit('refresh')
                    })
            },

            deleteDn(domainName) {
                let self = this;
                this.service.deleteDn(domainName)
                    .then(function(b) {
                        if (b) {
                            self.$emit('refresh')
                        }
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