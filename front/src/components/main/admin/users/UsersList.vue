<template>
    <div>
        <h3>User list</h3>
        <div class="row">
            <div class="form-group col-md-2">
                <button @click="createScheduler" class="btn btn-primary">Add scheduler...</button>
            </div>
            <div class="form-group col-md-2">
                <button @click="createUser" class="btn btn-primary">Add user...</button>
            </div>
        </div>
        <div class="mt-2">
            <table v-if="userList.length > 0" class="table">
                <thead>
                <tr>
                    <th scope="col">Username</th>
                    <th scope="col" style="width: 15%">Role</th>
                    <th scope="col" style="width: 10%">Edit</th>
                    <th scope="col" style="width: 10%">Remove</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="u in userList" :key="u._key">
                    <td>{{u._key}}</td>
                    <td class="align-middle">
                        <span v-if="u.role === 'admin'" class="badge badge-danger">
                            <img src="../../../../assets/icons/icons8-microsoft-admin-32.png" alt="admin">
                            {{u.role}}
                        </span>
                        <span v-else-if="u.role === 'user'" class="badge badge-primary">
                            <img src="../../../../assets/icons/icons8-male-user-24.png" style="width: 18px" alt="user">
                            {{u.role}}
                        </span>
                        <span v-else-if="u.role === 'scheduler'" class="badge badge-secondary">
                            <img src="../../../../assets/icons/icons8-clock-64.png" style="width: 18px" alt="clock">
                            {{u.role}}
                        </span>
                    </td>
                    <td>
                        <button @click="schedulerUpdate(u._key)" class="btn btn-primary" :disabled="u.role !== 'scheduler'">
                            <img src="../../../../assets/icons/icons8-edit-16.png" alt="edit">
                        </button>
                    </td>
                    <td>
                        <button @click="removeConfirm(u._key)" class="btn btn-danger" :disabled="u.role === 'admin'">
                            <img src="../../../../assets/icons/icons8-remove-24.png" alt="remove">
                        </button>
                    </td>
                </tr>
                </tbody>
            </table>
            <div v-else>
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            </div>
        </div>

        <ModalConfirm @confirm="remove" ref="modalConfirm"
                      msg="Confirm the user deletion (no way back) ?"
                      modal-id="userRemoveConfirm"/>

        <SchedulerCreateModal ref="schedulerCreateModal" @schedulerCreated="schedulerCreated"/>

        <UserCreateModal ref="userCreateModal" @userCreated="userCreated"/>

        <SchedulerUpdateModal ref="schedulerUpdateModal"/>
    </div>
</template>

<script>
    import ModalConfirm from "@/components/main/ModalConfirm.vue";
    import SchedulerCreateModal from "@/components/main/admin/users/SchedulerCreateModal.vue";
    import SchedulerUpdateModal from "@/components/main/admin/users/SchedulerUpdateModal.vue";
    import UserCreateModal from "@/components/main/admin/users/UserCreateModal.vue";
    export default {
        name: "UsersList",
        components: {SchedulerUpdateModal, SchedulerCreateModal, ModalConfirm, UserCreateModal},
        props: {
            userList: Array
        },
        methods: {
            removeConfirm(username) {
                this.$refs.modalConfirm.show(username)
            },
            remove(username) {
                console.log(username);
                this.$emit('remove', username)
            },
            createScheduler() {
                this.$refs.schedulerCreateModal.show()
            },
            schedulerCreated() {
                this.$emit('schedulerCreated')
            },
            createUser() {
                this.$refs.userCreateModal.show()
            },
            userCreated() {
                this.$emit('userCreated')
            },
            schedulerUpdate(schedulerName) {
                this.$refs.schedulerUpdateModal.show(schedulerName)
            }
        }
    }
</script>

<style scoped>

</style>