<template>
    <div>
        <div class="form-row">
                <div class="form-group col-md-3">
<!--                    <label for="dn-search-input" ><small>Filter</small></label>-->
                    <input v-model="filter" class="form-control" placeholder="Search" id="dn-search-input" v-on:keyup="validateSearch">
                </div>
                <div class="form-group col-md-">
<!--                    <label for="dn-search-type"><small>Filter by</small></label>-->
                    <select v-model="filterType" class="custom-select" id="dn-search-type">
                        <option :value="filterTypeDn" selected>Filter by domain name</option>
                        <option :value="filterTypeDnTags" selected>Filter by domain name tags</option>
                        <option :value="filterTypeIpTags" selected>Filter by IP tags</option>
                    </select>
                </div>
                <div class="form-group col-md-">
<!--                    <label for="dn-sort-type"><small>Sort by</small></label>-->
                    <select v-model="sortByType" class="custom-select" id="dn-sort-type">
                        <option :value="sortByTypeDn" selected>Sort by domain name</option>
                        <option :value="sortByTypeIp">Sort IP address</option>
                        <option :value="sortByTypeLast">Sort last IP change</option>
                    </select>
                </div>
                <div class="form-group col-md-">
                    <select v-model="ownershipFilter" class="custom-select" id="owned-followed">
                        <option :value="noOwnership" selected>No ownership filter</option>
                        <option :value="followedOnly">Followed only</option>
                        <option :value="ownedOnly">Owned only</option>
                        <option :value="ownedFollowedOnly">Followed/owned only</option>
                    </select>
                </div>
                <div class="form-group col-md-">
<!--                    <label for="dn-limit"><small>Limit</small></label>-->
                    <select v-model="limit" class="custom-select" id="dn-limit">
                        <option :value="10" selected>10 results</option>
                        <option :value="25">25 results</option>
                        <option :value="100">100 results</option>
                    </select>
                </div>

                <div class="form-group col-md-1">
<!--                    <label for="dn-search"><small>Go</small></label>-->
                    <router-link :to="`/?filter=${this.filter}&filterType=${this.filterType}&sortBy=${this.sortByType}&limit=${this.limit}&ownershipFilter=${this.ownershipFilter}`"
                                 type="button" id="dn-search" class="btn btn-primary">
                        Search
                    </router-link>
                </div>
        </div>
        <div v-if="dnList !== null">
            <DomainNameListStats :csv-blob-url="csvBlobUrl" :json-blob-url="jsonBlobUrl" :stats="stats"/>
            <DomainNameListView @refresh="refreshDnList" :dn-list="dnList"/>
        </div>
        <span v-else class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    </div>
    
</template>

<script>
    import PfaApi from "@/services/pfa-api";
    import DomainNameListView from "@/components/main/home/DomainNameListView";
    import DomainNameListStats from "@/components/main/home/DomainNameListStats";

    export default {
        name: "DomainNameList",
        components: {DomainNameListStats, DomainNameListView},
        data: function() {
            return {
                dnList: null,
                stats: null,
                jsonBlobUrl: "",
                csvBlobUrl: "",


                typeDn: "domainName",
                typeIp: "ipAddress",

                filter: "",
                filterTypeDn: "domainName",
                filterTypeDnTags: "dnTags",
                filterTypeIpTags: "ipTags",
                filterType: "domainName",

                sortByTypeLast: "lastIpChange",
                sortByTypeDn: "domainName",
                sortByTypeIp: "ipAddress",
                sortByType: "domainName",

                limit: "10",

                noOwnership: "noOwnership",
                followedOnly: "followedOnly",
                ownedOnly: "ownedOnly",
                ownedFollowedOnly: "ownedFollowedOnly",
                ownershipFilter: "ownedFollowedOnly"
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = new PfaApi(jwt);

            this.filter = this.$route.query.filter;
            if (this.filter == null) {
                this.filter = ""
            }
            this.filterType = this.$route.query.filterType;
            if (this.filterType == null) {
                this.filterType = this.filterTypeDn;
            }
            this.sortByType = this.$route.query.sortBy;
            if (this.sortByType == null) {
                this.sortByType = this.sortByTypeDn;
            }
            this.limit = this.$route.query.limit;
            if (this.limit == null) {
                this.limit = 10;
            }

            this.ownershipFilter = this.$route.query.ownershipFilter;
            if (this.ownershipFilter == null) {
                this.ownershipFilter = this.ownedFollowedOnly;
            }

            this.refreshDnList();
        },
        watch: {
            $route() {
                this.refreshDnList();
            }
        },
        methods: {
            refreshDnList() {
                let self = this;
                self.dnList = null;
                let owned = false;
                let followed = false;

                if (this.ownershipFilter === this.followedOnly) {
                    followed = true;
                } else if (this.ownershipFilter === this.ownedOnly) {
                    owned = true;
                } else if (this.ownershipFilter === this.ownedFollowedOnly) {
                    followed = true;
                    owned = true;
                }

                this.service.getDnList(owned, followed, this.filter, this.filterType, this.sortByType, this.limit, '')
                    .then(function (l) {
                        self.dnList = l.dn_list;
                        self.stats = l.stats;
                    });


                if (self.jsonBlobUrl !== '') {
                    window.URL.revokeObjectURL(self.jsonBlobUrl);
                    self.jsonBlobUrl = '';
                }
                this.service.exportDnList(this.filter, this.filterType, this.sortByType, this.limit, 'json')
                    .then(function (jsonData) {
                        let blob = new Blob([JSON.stringify(jsonData)]);
                        self.jsonBlobUrl = window.URL.createObjectURL(blob);
                    });

                if (self.csvBlobUrl !== '') {
                    window.URL.revokeObjectURL(self.csvBlobUrl);
                    self.csvBlobUrl = '';
                }
                this.service.exportDnList(this.filter, this.filterType, this.sortByType, this.limit, 'csv')
                    .then(function (csvData) {
                        let blob = new Blob([csvData]);
                        self.csvBlobUrl = window.URL.createObjectURL(blob);
                    })


            },

            validateSearch: function (e) {
                let self = this;
                if (e.keyCode === 13) {
                    this.$router.push({
                        path: '/',
                        query: {
                            filter: self.filter,
                            filterType: self.filterType,
                            sortBy: self.sortBy,
                            limit: self.limit,
                        }
                    })
                }
            },
        }
    }

</script>

<style scoped>
</style>