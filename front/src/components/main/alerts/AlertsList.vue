<template>
    <div>
        <div class="form-row">
            <div class="form-group col-md-6">
<!--                <label for="alertSearchInput"><small>Filter</small></label>-->
                <input v-model="filter" class="form-control" placeholder="Search"
                       id="alertSearchInput" @keyup="applyQuery">
            </div>
            <div class="form-group col-md-2">
<!--                <label for="alertSearchType"><small>Filter by</small></label>-->
                <select v-model="filterType" class="custom-select" id="alertSearchType">
                    <option :value="filterTypeDn" selected>domain name</option>
                    <option :value="filterTypeDnTags">domain name tags</option>
                    <option :value="filterTypeIpTags">IP tags</option>
                </select>
            </div>
            <div class="form-group col-md-2">
<!--                <label for="alertSortBy"><small>Sort by</small></label>-->
                <select v-model="sortByType" class="custom-select" id="alertSortBy">
                    <option :value="sortByTypeDn" selected>domain name</option>
                    <option :value="sortByLastIp">last IP</option>
                    <option :value="sortByCurrentIp">current IP</option>
                </select>
            </div>
            <div class="form-group col-md-1">
<!--                <label for="alertLimit"><small>Limit</small></label>-->
                <select v-model="limit" class="custom-select" id="alertLimit">
                    <option :value="10" selected>10</option>
                    <option :value="25">25</option>
                    <option :value="100">100</option>
                </select>
            </div>
            <div class="form-group col-md-1">
<!--                <label for="alertSearch"><small>Go</small></label>-->
                <router-link :to="`/alerts?filter=${this.filter}&filterType=${this.filterType}&sortBy=${this.sortByType}&limit=${this.limit}`"
                             type="button" id="alertSearch" class="btn btn-primary">
                    Search
                </router-link>
            </div>
        </div>
        <div v-if="dnList !== null">
            <DomainNameListStats :json-blob-url="jsonBlobUrl" :csv-blob-url="csvBlobUrl" :stats="stats"/>
            <AlertListView :dn-list="dnList"/>
        </div>
        <span v-else class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    </div>
</template>

<script>
    import PfaApi from "@/services/pfa-api";
    import AlertListView from "@/components/main/alerts/AlertListView";
    import DomainNameListStats from "@/components/main/home/DomainNameListStats";
    export default {
        name: "AlertsList",
        components: {DomainNameListStats, AlertListView},
        data() {
            return {
                dnList: null,
                stats: null,
                jsonBlobUrl: "",
                csvBlobUrl: "",

                sortByCurrentIp: "currentIpAddress",
                sortByLastIp: "lastIpAddress",
                sortByTypeDn: "domainName",
                sortByType: "domainName",

                filterTypeDnTags: "dnTags",
                filterTypeIpTags: "ipTags",
                filterTypeDn: "domainName",
                filterType: "domainName",
                filter: "",

                limit: "10"
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

            this.refreshList();
        },
        watch: {
            $route() {
                this.refreshList();
            }
        },
        methods: {
            refreshList() {
                let self = this;
                this.service.getAlertList(this.filter, this.filterType, this.sortByType, this.limit)
                    .then(function(d) {
                        self.dnList = d.dn_list;
                        self.stats = d.stats;
                    });

                if (self.jsonBlobUrl !== '') {
                    window.URL.revokeObjectURL(self.jsonBlobUrl);
                    self.jsonBlobUrl = '';
                }
                this.service.exportAlertList(this.filter, this.filterType, this.sortByType, this.limit, 'json')
                    .then(function (jsonData) {
                        let blob = new Blob([JSON.stringify(jsonData)]);
                        self.jsonBlobUrl = window.URL.createObjectURL(blob);
                    });

                if (self.csvBlobUrl !== '') {
                    window.URL.revokeObjectURL(self.csvBlobUrl);
                    self.csvBlobUrl = '';
                }
                this.service.exportAlertList(this.filter, this.filterType, this.sortByType, this.limit, 'csv')
                    .then(function (csvData) {
                        let blob = new Blob([csvData]);
                        self.csvBlobUrl = window.URL.createObjectURL(blob);
                    })
            },

            applyQuery(e) {
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
            }
        }
    }
</script>

<style scoped>

</style>