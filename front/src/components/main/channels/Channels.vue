<template>
    <div class="container" >
<!--      fixme: add loader when loading the data-->
        <ChannelsAvailableList
                @setup="setup"
                :channels-list="channelsAvailableList"
        />

    </div>
</template>

<script>

    import ChannelsAvailableList from "@/components/main/channels/ChannelsAvailableList.vue";
    import Services from "../../../services/services.js";
    export default {
        name: "Channels",
        components: {ChannelsAvailableList},
        data() {
            return {
                channelsAvailableList: [],
                channelDefault: "_default"
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);
            this.refreshLists();
        },
        methods: {
            refreshLists() {
                this.getChannelsAvailableList();
            },
            getChannelsAvailableList() {
                let self = this;
                this.service.getChannelsAvailableList()
                    .then(function(d) {
                        self.channelsAvailableList = d;
                    })
            },
            test(user_channel) {
                this.service.testChannel(user_channel.channel._key)
            }
        }
    }
</script>

<style scoped>

</style>