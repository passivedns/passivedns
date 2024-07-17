<template>
    <div class="container">
        <DomainNameCreate
        @success="refresh"></DomainNameCreate>
        <DomainNameImport
        @success="refresh"></DomainNameImport>
        <DomainNameList ref="dnList"></DomainNameList>
    </div>
</template>

<script>
    import DomainNameList from "@/components/main/home/DomainNameList.vue";
    import DomainNameCreate from "@/components/main/home/DomainNameCreate.vue";
    import DomainNameImport from "@/components/main/home/DomainNameImport.vue";
    import { ref } from 'vue';

    const dnList = ref();

    export default {
        name: "Home",
        components: {
            DomainNameCreate,
            DomainNameList,
            DomainNameImport,
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