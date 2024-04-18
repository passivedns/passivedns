<template>
    <div class="modal fade" :id="id" tabindex="-1" role="dialog"
         aria-labelledby="tagModalManageLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title" id="tagModalManageLabel">{{object}}</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div><small>Linked tags</small></div>
                    <div class="mb-3" >
                        <div v-if="tagLinkedList.length > 0">
                            <span class="badge badge-primary badge-button m-1"
                                  v-for="t in tagLinkedList"
                                  :key="t" @click="removeTagLinked(t)">
                                {{t}}
                            </span>
                        </div>
                        <div class="text-muted" v-else>
                            No tag linked
                        </div>
                    </div>
                    <div><small>Available tags</small></div>
                    <div class="form-group">
                        <div class="input-group mb-1 mt-1">
                            <input v-model="tagInput" type="text" class="form-control" placeholder="New tag" aria-label="New tag" aria-describedby="tagCreateButton">
                            <div class="input-group-append">
                                <button @click="addTag" class="btn btn-outline-primary"
                                        type="button" id="tagCreateButton">New tag</button>
                            </div>
                        </div>
                    </div>
                    <div v-if="availableTagList.length > 0">
                        <span @click="addTagLinked(t)" class="badge badge-primary badge-button m-1"
                              v-for="t in availableTagList"
                              :key="t">
                            {{t}}
                        </span>
                    </div>
                    <div v-else class="text-muted">
                        No tag available
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                </div>

            </div>
        </div>

    </div>
</template>

<script>
import Services from "../../../services/services.js";

    export default {
        name: "TagManageModal",
        props: {
            id: String,
            object: String,
            type: String,
        },
        computed: {
            availableTagList() {
                let self = this;
                let out = [];
                this.tagList.forEach(function(t) {
                    if (self.tagLinkedList.indexOf(t) === -1) {
                        out.push(t)
                    }
                });

                return out;
            }
        },
        data() {
            return {
                tagList: [],
                tagLinkedList: [],

                tagInput: "",
            }
        },
        mounted() {
            let jwt = localStorage.getItem('jwt');
            this.service = Services.getPfaApiService(jwt);

            // eslint-disable-next-line no-undef
            this.modal = new bootstrap.Modal(
                document.getElementById(this.id)
            )
        },
        methods: {
            show() {
                this.modal.show();
                this.refreshTagList();
            },
            refreshTagList() {
                let self = this;
                this.service.getLinkedTagsList(this.object, this.type)
                    .then(function(l) {
                        self.tagLinkedList = l;
                    });

                this.service.getTagList()
                    .then(function(l) {
                        self.tagList = l;
                    })
            },
            removeTagLinked(t) {
                let self = this;
                this.service.deleteLinkedTag(this.object, this.type, t)
                    // fixme: add catch error
                    .then(function() {
                        self.refreshTagList();
                        self.$emit('refresh')
                    })
            },
            addTagLinked(t) {
                let self = this;
                this.service.createLinkedTag(this.object, this.type, t)
                    // fixme: add catch error
                    .then(function() {
                        self.refreshTagList();
                        self.$emit('refresh');
                    })
            },
            addTag() {
                let self = this;
                this.service.createTag(this.tagInput)
                    // fixme: add catch error
                    .then(function(b) {
                        if (b) {
                            self.addTagLinked(self.tagInput)
                        }
                    })
            }
        }
    }
</script>

<style scoped>
    .badge-button {
        cursor: pointer;
    }
</style>