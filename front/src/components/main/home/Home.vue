<template>
    <div class="container">
        <DomainNameCreate></DomainNameCreate>
        <DomainNameList></DomainNameList>
    </div>
</template>

<script>
    import DomainNameList from "@/components/main/home/DomainNameList.vue";
    import DomainNameCreate from "@/components/main/home/DomainNameCreate.vue";

    export default {
        name: "Home",
        components: {
            DomainNameCreate,
            DomainNameList,
        },

        methods: {

        }
    }
</script>

<style scoped>

</style>