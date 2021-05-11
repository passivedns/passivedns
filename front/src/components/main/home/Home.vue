<template>
    <div class="container">
        <DomainNameCreate></DomainNameCreate>
        <DomainNameList></DomainNameList>
    </div>
</template>

<script>
    import DomainNameList from "@/components/main/home/DomainNameList";
    import DomainNameCreate from "@/components/main/home/DomainNameCreate";

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