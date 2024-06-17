<template>
    <div class="container" >
        <ExternApisAvailableList
                @setup="setup"
                :extern-apis-list="externApisAvailableList"
        />

        <ExternApiSetupModal
                ref="externApiSetupModal"
                @success="refreshLists"
        />

        <ExternApisLinkedList
                @remove="remove"
                :extern-apis-list="externApisLinkedList"
        />

        <ModalConfirm ref="externApiRemoveConfirm" @confirm="removeConfirm"
                modal-id="externApiRemoveConfirm"
                msg="Confirm the API setup deletion ?"
        />

    </div>
</template>

<script>

import ExternApisLinkedList from "@/components/main/externApis/ExternApisLinkedList.vue";
    import ExternApisAvailableList from "@/components/main/externApis/ExternApisAvailableList.vue";
    import ExternApiSetupModal from "@/components/main/externApis/ExternApiSetupModal.vue";
    import ModalConfirm from "@/components/main/ModalConfirm.vue";
    import Services from "../../../services/services.js";
    export default {
        name: "ExternApis",
        components: {ModalConfirm, ExternApiSetupModal, ExternApisAvailableList, ExternApisLinkedList},
        data() {
            return {
                externApisLinkedList: [],
                externApisAvailableList: [],
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);
            this.refreshLists();
        },
        methods: {
            refreshLists() {
                this.getExternApisLinkedList();
                this.getExternApisAvailableList();
            },

            getExternApisLinkedList() {
                let self = this;
                this.service.getExternApiLinkedList()
                    .then(function(d) {
                        self.externApisLinkedList = d;
                    })
            },
            getExternApisAvailableList() {
                let self = this;
                this.service.getExternApisAvailableList()
                    .then(function(d) {
                        self.externApisAvailableList = d;
                    })
            },
            setup(externApi) {
                this.$refs.externApiSetupModal.show(externApi)
            },
            remove(externApi) {
                this.$refs.externApiRemoveConfirm.show(externApi);
            },

            removeConfirm(externApi) {
                let self = this;
                this.service.removeExternApi(externApi._key)
                    .then(function() {
                        self.refreshLists()
                    })
            }
        }
    }
</script>

<style scoped>

</style>