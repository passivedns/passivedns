<template>
    <div class="container" >
        <ChannelsAvailableList
                @setup="setup"
                :channels-list="channelsAvailableList"
                :channel-type-email="channelTypeEmail"
                :channel-type-telegram="channelTypeTelegram"
                :channel-type-discord="channelTypeDiscord"
        />

        <ChannelSetupModal
                ref="channelSetupModal"
                @success="refreshLists"
                :channel-type-email="channelTypeEmail"
                :channel-type-telegram="channelTypeTelegram"
                :channel-type-discord="channelTypeDiscord"
        />

        <ChannelsLinkedList
                @verify="verify"
                @remove="remove"
                @test="test"
                :channels-list="channelsLinkedList"
                :channel-type-email="channelTypeEmail"
                :channel-type-telegram="channelTypeTelegram"
                :channel-type-discord="channelTypeDiscord"
                :channel-default="channelDefault"
        />

        <ChannelVerifyModal
                ref="channelVerifyModal"
                @success="refreshLists"
                :channel-type-email="channelTypeEmail"
                :channel-type-telegram="channelTypeTelegram"
                :channel-type-discord="channelTypeDiscord"
        />

        <ModalConfirm ref="channelRemoveConfirm" @confirm="removeConfirm"
                modal-id="channelRemoveConfirm"
                msg="Confirm the channel setup deletion ?"
        />

    </div>
</template>

<script>

import ChannelsLinkedList from "@/components/main/channels/ChannelsLinkedList";
    import ChannelsAvailableList from "@/components/main/channels/ChannelsAvailableList";
    import ChannelSetupModal from "@/components/main/channels/ChannelSetupModal";
    import ChannelVerifyModal from "@/components/main/channels/ChannelVerifyModal";
    import ModalConfirm from "@/components/main/ModalConfirm";
    import Services from "../../../services/services";
    export default {
        name: "Channels",
        components: {ModalConfirm, ChannelVerifyModal, ChannelSetupModal, ChannelsAvailableList, ChannelsLinkedList},
        data() {
            return {
                channelsLinkedList: [],
                channelsAvailableList: [],

                channelTypeEmail: "email",
                channelTypeTelegram: "telegram",
                channelTypeDiscord: "discord",
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
                this.getChannelLinkedList();
                this.getChannelsAvailableList();
            },

            getChannelLinkedList() {
                let self = this;
                this.service.getChannelLinkedList()
                    .then(function(d) {
                        self.channelsLinkedList = d;
                    })
            },
            getChannelsAvailableList() {
                let self = this;
                this.service.getChannelsAvailableList()
                    .then(function(d) {
                        self.channelsAvailableList = d;
                    })
            },
            setup(channel) {
                this.$refs.channelSetupModal.show(channel)
            },
            verify(user_channel) {
                this.$refs.channelVerifyModal.show(user_channel.channel)
            },
            remove(user_channel) {
                this.$refs.channelRemoveConfirm.show(user_channel);
            },

            removeConfirm(user_channel) {
                let self = this;
                this.service.removeChannel(user_channel.channel._key)
                    .then(function() {
                        self.refreshLists()
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