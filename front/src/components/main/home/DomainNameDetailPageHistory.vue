<template>
    <div class="row">
        <div class="container">
            <h3>History</h3>
        </div>
        <div class="container">
            <table v-if="history.length > 0" class="table">
                <thead>
                <tr>
                    <th scope="col">IP</th>
                    <th scope="col">Country</th>
                    <th scope="col">Last seen</th>
                    <th scope="col">First seen</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="r in history" :key="r.ip._key">
                    <td>{{r.ip._key}}</td>
                    <td>{{r.ip.location.country}}</td>
                    <td>{{formatDate(r.last_updated_at)}}</td>
                    <td>{{formatDate(r.first_updated_at)}}</td>
                </tr>
                </tbody>
            </table>
            <div v-else class="text-muted">
                No history found for this domain name
            </div>
        </div>
    </div>
</template>

<script>
    import DateUtil from "@/services/date-util";

    export default {
        name: "DomainNameDetailPageHistory",
        props: {
            history: Array,
        },
        methods: {
            formatDate(d) {
                return DateUtil.formatDiffNow(d)
            }
        }
    }
</script>

<style scoped>

</style>
