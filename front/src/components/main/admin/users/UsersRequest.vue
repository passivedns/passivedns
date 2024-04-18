<template>
    <div>
        <h3>Access requests</h3>
        <div>
            <table v-if="requestList.length > 0" class="table">
                <thead>
                <tr>
                    <th scope="col">Email</th>
                    <th scope="col" style="width: 15%">Requested at</th>
                    <th scope="col" style="width: 10%">Verify</th>
                    <th scope="col" style="width: 5%">Remove</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="r in requestList" :key="r._key">
                    <td>{{r._key}}</td>
                    <td>{{formatDate(r.requested_at)}}</td>
                    <td>
                        <button @click="verify(r._key)" class="btn btn-primary">Invite</button>
                    </td>
                    <td>
                        <button @click="removeRequestConfirm(r._key)" class="btn btn-danger">
                            <img src="../../../../assets/icons/icons8-remove-24.png" alt="remove">
                        </button>
                    </td>
                </tr>
                </tbody>
            </table>
            <div v-else class="mx-auto text-muted" style="width: 200px;">
                No data
            </div>
        </div>

        <ModalConfirm @confirm="removeRequest" ref="requestRemoveConfirm"
                      msg="Confirm the user request deletion (no way back) ?"
                      modal-id="requestRemoveConfirm"/>
    </div>
</template>

<script>
    import DateUtil from "@/services/date-util.js";
    import ModalConfirm from "@/components/main/ModalConfirm.vue";
    export default {
        name: "UsersRequest",
        components: {
            ModalConfirm
        },
        props: {
            requestList: Array,
        },
        methods: {
            formatDate(d) {
                return DateUtil.formatDiffNow(d)
            },
            verify(email) {
                this.$emit('verify', email)
            },
            removeRequestConfirm(email) {
                this.$refs.requestRemoveConfirm.show(email)
            },
            removeRequest(email) {
                this.$emit('remove', email)
            }
        }
    }
</script>

<style scoped>

</style>