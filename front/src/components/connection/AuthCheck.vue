<template>
    <transition name="fade">
        <div class="auth-check" v-if="loading">
            <div v-if="valid === null">
                <button class="btn btn-primary" type="button" disabled>
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    {{loadingMsg}}...
                </button>
            </div>
            <div v-else-if="valid === true">
                <button class="btn btn-success" type="button" disabled>
                    <img src="../../assets/icons/icons8-checkmark-16.png" alt="valid">
                    {{validMsg}}
                </button>
            </div>
            <div v-else-if="valid === false">
                <button class="btn btn-danger" type="button" disabled>
                    <img src="../../assets/icons/icons8-cross-mark-16.png" alt="invalid">
                    {{invalidMsg}}
                </button>
            </div>
        </div>
    </transition>
</template>

<script>
    export default {
        name: "AuthCheck",
        props: {
            loading: Boolean,
            valid: Boolean,
            loadingMsg: String,
            invalidMsg: String,
            validMsg: String
        }
    }
</script>

<style scoped>
    .auth-check {
        margin: 15px;
    }

    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
        opacity: 0;
    }

</style>