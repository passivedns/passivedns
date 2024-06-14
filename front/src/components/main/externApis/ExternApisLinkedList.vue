<template>
    <div class="mb-4">
        <h3>Connected APIs</h3>
        <div class="row" v-if="externApisList.length > 0">
            <div class="col-" v-for="a in externApisList" :key="a._key">
                <div class="card m-1" style="width: 20rem;">
                    <div class="card-header">
                        <img class="mr-2 light"
                             src="../../../assets/icons/icons8-cloud-50.png" alt="API">
                        <span style="font-size: 24px" class="card-title">{{a._key}}</span>
                    </div>
                    <div class="card-body">
                        <p class="card-text">
                            {{c.user_channel.contact}}
                        </p>
                        <span v-if="c.user_channel.verified === true" class="card-link">
                            <button @click="test(c)" class="btn btn-primary">
                                Test
                            </button>
                        </span>
                        <span v-else class="card-link">
                            <button @click="verify(c)" class="btn btn-primary">
                                Verify
                            </button>
                        </span>
                        <span class="card-link">
                            <button v-if="c.channel._key !== channelDefault" @click="remove(c)" class="btn btn-danger">
                                <img src="../../../assets/icons/icons8-remove-24.png" alt="remove">
                                Remove
                            </button>
                        </span>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="text-muted">
            No data
        </div>
    </div>
</template>

<script>
    export default {
        name: "ExternApisLinkedList",
        props: {
            externApisList: Array,
        },
        methods: {
            remove(user_channel) {
                this.$emit('remove', user_channel)
            },
        }
    }
</script>

<style scoped>

</style>