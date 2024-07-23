<template>
    <div>
        <div v-if="channelsList.length > 0">
            <table class="table">
                <thead>
                <tr>
                    <th scope="col" style="width: 10%"></th>
                    <th scope="col">Name</th>
                    <th scope="col" style="width: 5%">Edit</th>
                    <th scope="col" style="width: 5%">Remove</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="ch in channelsList" :key="ch._key">
                    <td>
                        <img class="light" src="../../../../assets/icons/redis-48.png" alt="redis">
                    </td>

                    <td class="align-middle">
                        <h4>{{ch._key}}</h4>
                    </td>

                    <td class="align-middle">
                        <button class="btn btn-primary" @click="select(ch)">
                            <img src="../../../../assets/icons/icons8-edit-16.png" alt="edit">
                        </button>
                    </td>

                    <td class="align-middle">
                        <button class="btn btn-danger" @click="removeConfirm(ch)" :disabled="ch._key === '_default'">
                            <img src="../../../../assets/icons/icons8-remove-24.png" alt="delete">
                        </button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            <span class="spinner-border spinner-border-sm" role="status"
                  aria-hidden="true"></span>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AdminChannelsList",
        props: {
            channelsList: Array,
        },
        data() {
            return {
                channelSelected: null
            }
        },
        methods: {
            select(channel) {
                this.$emit('select', channel);
            },
            removeConfirm(channel) {
                this.$emit('removeConfirm', channel)
            },

        },
    }
</script>

<style scoped>

</style>