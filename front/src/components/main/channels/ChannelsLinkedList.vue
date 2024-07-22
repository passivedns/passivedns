<template>
    <div class="mb-4">
        <h3>Connected channels</h3>
        <div class="row" v-if="channelsList.length > 0">
            <div class="col-" v-for="c in channelsList" :key="c.channel._key">
                <div class="card m-1" style="width: 20rem;">
                    <div class="card-header">
                        <img v-if="c.channel.type === channelTypeEmail" class="mr-2 light"
                             src="../../../assets/icons/icons8-mail-48.png" alt="mail">
                        <span style="font-size: 24px" class="card-title">{{c.channel._key}}</span>
                    </div>
                    <div class="card-body">
                        <div class="card-subtitle mb-2">
                            <span v-if="c.user_channel.verified" class="badge badge-success">
                                <img src="../../../assets/icons/icons8-verified-account-24.png" width="12px" alt="checkmark">
                                verified
                            </span>
                            <span v-else class="badge badge-danger">
                                <img src="../../../assets/icons/icons8-cross-mark-16.png" width="12px" alt="crossmark">
                                not verified
                            </span>

                        </div>
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
        name: "ChannelsLinkedList",
        props: {
            channelsList: Array,
            channelTypeEmail: String,

            channelDefault: String
        },
        methods: {
            verify(user_channel) {
                this.$emit('verify', user_channel)
            },

            remove(user_channel) {
                this.$emit('remove', user_channel)
            },

            test(user_channel) {
                this.$emit('test', user_channel)
            }
        }
    }
</script>

<style scoped>

</style>