<template>
    <div class="mb-4">
        <h3>Available APIs</h3>
        <div class="row" v-if="externApisList.length > 0">
            <div class="col-" v-for="a in externApisList" :key="a._key">
                <div class="card m-1" style="width: 20rem;">
                    <div class="card-header">
                        <img class="mr-2 light"
                             src="../../../assets/icons/icons8-cloud-50.png" alt="API">
                        <span style="font-size: 24px" class="card-title">{{a._key}}</span>
                    </div>
                    <div class="card-body row justify-content-between">
                        <span class="card-link col-5">
                            <button @click="setup(a)" class="btn btn-primary">
                                <img src="../../../assets/icons/icons8-settings-24.png" alt="setup">
                                Setup
                            </button>
                        </span>
                        <span class="card-link col-5">
                            <button @click="update(a)" class="btn btn-primary">
                                <img src="../../../assets/icons/icons8-edit-16.png" alt="edit">
                                Edit
                            </button>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ExternApisAvailableList",
        props: {
            externApisList: Array,
        },
        methods: {
            setup(externApi) {
                this.$emit('setup', externApi)
            },

            update(externApi) {
                this.$emit('update', externApi)
            }
        }
    }
</script>

<style scoped>

</style>