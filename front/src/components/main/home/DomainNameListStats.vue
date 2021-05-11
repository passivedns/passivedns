<template>
    <div class="row">
        <div class="col- text-muted">
            <span>{{stats.count}} records</span>
            <span class="ml-2">{{stats.transaction_time}} seconds</span>
        </div>
        <div class="col text-muted text-right">
                        <span v-if="jsonBlobUrl === ''" class="spinner-border spinner-border-sm mr-2"
                              role="status" aria-hidden="true"></span>
            <a v-else :href="jsonBlobUrl" :download="jsonFile" class="mr-2">json</a>

            <span v-if="csvBlobUrl === ''" class="spinner-border spinner-border-sm mr-2"
                  role="status" aria-hidden="true"></span>
            <a v-else :href="csvBlobUrl" :download="csvFile">csv</a>
        </div>
    </div>
</template>

<script>
    export default {
        name: "DomainNameListStats",
        props: {
            stats: Object,
            jsonBlobUrl: String,
            csvBlobUrl: String,
        },
        computed: {
            jsonFile() {
                return `domain_name_list_${+new Date()}.json`
            },
            csvFile() {
                return `domain_name_list_${+new Date()}.csv`
            },
        }
    }
</script>

<style scoped>

</style>