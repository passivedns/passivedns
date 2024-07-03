<template>
    <div class="container">
        <DomainNameCreate
        @success="refresh"></DomainNameCreate>
        <DomainNameList ref="dnList"></DomainNameList>
    </div>
</template>

<script>
    import DomainNameList from "@/components/main/home/DomainNameList.vue";
    import DomainNameCreate from "@/components/main/home/DomainNameCreate.vue";
    import { ref } from 'vue';

    const dnList = ref();

    export default {
        name: "Home",
        components: {
            DomainNameCreate,
            DomainNameList,
        },

        methods: {
            refresh() {
                this.$refs.dnList.refreshDnList()
            }
        }
    }
</script>

<style scoped>

</style>