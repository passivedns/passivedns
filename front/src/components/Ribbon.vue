<template>
    <div class="infos" v-if="infos !== null">
        <a :href="infos.jobUrl">{{infos.commitSha}}</a>
        {{infos.version}}
    </div>
</template>

<script>
    import Services from "../services/services";

    export default {
        name: "Ribbon",
        data() {
            return {
                infos: null
            }
        },
        mounted() {
            let self = this;

            this.service = Services.getPfaApiPublicService();
            this.service.getInfos()
                .then(function(infos) {
                    self.infos = {
                        commitSha: infos.commit_sha,
                        jobUrl: infos.job_url,
                        version: infos.version,
                    };
                })
        }
    }
</script>

<style scoped>

</style>