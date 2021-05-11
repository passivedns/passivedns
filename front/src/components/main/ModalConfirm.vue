<template>
    <div class="modal fade" :id="modalId" tabindex="-1" role="dialog"
         aria-labelledby="channelModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p>{{msg}}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" @click="confirm">Confirm</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ModalConfirm",
        props: {
            msg: String,
            modalId: String
        },
        data() {
            return {
                data: null,
            }
        },
        mounted() {
            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById(this.modalId)
            );
        },
        methods: {
            show(data) {
                this.data = data;
                this.modal.show();
            },

            confirm() {
                this.modal.hide();
                this.$emit('confirm', this.data);
            }
        }
    }
</script>

<style scoped>

</style>