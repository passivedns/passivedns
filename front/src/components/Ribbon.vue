<template>
    <div class="infos" v-if="infos !== null">
        <a :href="infos.jobUrl">{{infos.commitSha}}</a>
        {{infos.version}}
    </div>
</template>

<script>
    import PfaApiPublic from "@/services/pfa-api-public";

    export default {
        name: "Ribbon",
        data() {
            return {
                infos: null
            }
        },
        mounted() {
            let self = this;

            this.service = new PfaApiPublic();
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