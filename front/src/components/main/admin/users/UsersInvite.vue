<template>
    <div>
        <div>
            <h3>User invitation</h3>
            <div>
                <div class="input-group mb-3">
                    <input v-model="invitedEmailInput" type="text" class="form-control" placeholder="Email" aria-label="Username" aria-describedby="button-login">
                    <div class="input-group-append">
                        <button @click="invite" class="btn btn-outline-primary" type="button" id="button-login">Invite</button>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div>
                <table v-if="inviteList.length > 0" class="table">
                    <thead>
                    <tr>
                        <th scope="col">Email</th>
                        <th scope="col" style="width: 25%">Invited at</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="i in inviteList" :key="i.email">
                        <td>{{i.email}}</td>
                        <td>{{formatDate(i.invited_at)}}</td>
                    </tr>
                    </tbody>
                </table>
                <div v-else class="mx-auto text-muted" style="width: 200px;">
                    No data
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import DateUtil from "@/services/date-util";
    export default {
        name: "UsersInvite",
        props: {
            inviteList: Array
        },
        data() {
            return {
                invitedEmailInput: "",
            }
        },
        methods: {
            formatDate(d) {
                return DateUtil.formatDiffNow(d)
            },

            invite() {
                this.$emit('invite', this.invitedEmailInput)
            }
        }
    }
</script>

<style scoped>

</style>