<template>
    <div class="mb-4">
        <h3>Available channels</h3>
        <div class="row" v-if="channelsList.length > 0">
            <div class="col-" v-for="c in channelsList" :key="c._key">
                <div class="card m-1" style="width: 20rem;">
                    <div class="card-header">
                        <img v-if="c.type === channelTypeRedis" class="mr-2 light"
                             src="../../../assets/icons/redis-48.png" alt="redis">
                        <span style="font-size: 24px" class="card-title">{{c._key}}</span>
                    </div>
                    <div class="card-body">
                        <span class="card-link">
                            <button v-if="c.type !== channelTypeRedis" @click="setup(c)" class="btn btn-primary">
                                <img src="../../../assets/icons/icons8-settings-24.png" alt="setup">
                                Setup
                            </button>
                            <button v-else="c.type === channelTypeRedis" @click="test(c)" class="btn btn-primary">Test channel</button>
                            <AuthCheck :loading="loading" :valid="valid" valid-msg="Test sent"
                               loading-msg="Sending test" invalid-msg="Could not send"></AuthCheck>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AuthCheck from "@/components/connection/AuthCheck.vue";
import Services from "../../../services/services.js";
    export default {
        name: "ChannelsAvailableList",
        components: {
            AuthCheck
        },
        props: {
            channelsList: Array,
            channelTypeRedis: String,
        },
        data() {
            return {
                loading: false,
                valid: null,
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);
        },
        methods: {
            setup(channel) {
                this.$emit('setup', channel)
            },
            test(channel) {
                let self = this;
                this.loading = true;
                this.valid = null;
                this.service.testChannel(channel._key)
                    .then(function(b) {
                        self.valid = b;
                        if (b) {
                            self.loading = false;
                            self.close();
                        }
                    })
            }
        }
    }
</script>

<style scoped>

</style>