<template>
    <div class="container" >
        <h1 id="channels">Channels</h1>

        <div class="form-group">
            <button @click="createChannel" class="btn btn-primary">Add channel...</button>
        </div>

        <AdminChannelsList
                ref="adminChannelsList"
                @select="select"
                @removeConfirm="removeConfirm"
                :channels-list="channelsList"
        />

        <AdminChannelModalUpdate
                ref="adminChannelModalUpdate"
                @updated="getChannelList"
        />

        <AdminChannelModalCreate
                ref="adminChannelModalCreate"
                @created="getChannelList"
        />

        <ModalConfirm ref="modalConfirm" @confirm="removeConfirmed"
                      modal-id="channelRemoveConfirm"
                      msg="Confirm the channel deletion (no way back) ?"/>
    </div>
</template>

<script>

    import AdminChannelsList from "@/components/main/admin/channels/AdminChannelsList.vue";
    import ModalConfirm from "@/components/main/ModalConfirm.vue";
    import AdminChannelModalUpdate from "@/components/main/admin/channels/AdminChannelModalUpdate.vue";
    import AdminChannelModalCreate from "@/components/main/admin/channels/AdminChannelModalCreate.vue";
    import Services from "../../../../services/services.js";

    export default {
        name: "AdminChannels",
        components: {AdminChannelModalCreate, ModalConfirm, AdminChannelsList, AdminChannelModalUpdate},
        data() {
            return {
                channelsList: [],
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiAdminService(jwt);
            this.getChannelList()
        },
        methods: {
            select(channel) {
                this.$refs.adminChannelModalUpdate.select(channel)
            },
            removeConfirm(channel) {
                this.$refs.modalConfirm.show(channel)
            },
            createChannel() {
                this.$refs.adminChannelModalCreate.show()
            },
            removeConfirmed(channel) {
                let self = this;
                this.service.channelRemove(channel._key)
                    .then(function() {
                        self.getChannelList();
                    })
            },
            getChannelList() {
                let self = this;
                this.service.channelsList()
                    .then(function(d) {
                        self.channelsList = d
                    })
            },
        }
    }
</script>

<style scoped>

</style>