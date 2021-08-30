import dn_list from "./data/dn-list.json"
import dn_list_export from "./data/dn-list-export.json"
import available_channels_list from "./data/available-channels-list.json"
import linked_channels_list from "./data/linked-channels-list.json"
import dn from "./data/dn.json"
import dn_history from "./data/dn-history.json"
import tag_list from "./data/tag-list.json"
import tag_linked_list from "./data/tag-linked-list.json"


let timeout = 1000

export default class PfaApiMock {
    getAlertList() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(dn_list)
            }, timeout)
        })
    }

    exportAlertList() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(dn_list_export)
            }, timeout)
        })
    }

    getDnList() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(dn_list)
            }, timeout)
        })
    }

    exportDnList() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(dn_list_export)
            }, timeout)
        })
    }

    getChannelsAvailableList() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(available_channels_list.channel_list)
            }, timeout)
        })
    }

    getChannelLinkedList() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(linked_channels_list.channel_list)
            }, timeout)
        })
    }

    setupChannel() {
        return new Promise((resolve) => {
            console.log("setupChannel called")
            resolve(false)
        })

    }

    verifyChannel() {
        return new Promise((resolve) => {
            console.log("verifyChannel called")
            resolve(false)
        })
    }

    testChannel() {
        return new Promise((resolve) => {
            setTimeout(() => {
                console.log("testChannel called")
                resolve(true)
            }, timeout)
        })
    }

    removeChannel() {
        return new Promise((resolve) => {
            console.log("removeChannel called")
            resolve(false)
        })
    }

    createDn() {
        return new Promise((resolve) => {
            console.log("createDn called")
            resolve(false)
        })
    }

    getDn() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(dn)
            }, timeout)
        })
    }

    getDnHistory() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(dn_history.history)
            }, timeout)
        })
    }

    createTag() {
        return new Promise((resolve) => {
            console.log("createTag called")
            resolve(false)
        })
    }

    getTagList() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(tag_list.tag_list)
            }, timeout)
        })
    }

    getLinkedTagsList() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(tag_linked_list.tag_link_list)
            }, timeout)
        })
    }

    createLinkedTag() {
        return new Promise((resolve, reject) => {
            console.log("createLinkedTag called")
            reject("cant link tags on demo")
        })
    }

    deleteLinkedTag() {
        return new Promise((resolve, reject) => {
            console.log("deleteLinkedTag called")
            reject("cant remove tags on demo")
        })
    }

    changePassword() {
        return new Promise((resolve) => {
            console.log("changePassword called")
            resolve({b: false, msg: "cant change password on demo"})
        })
    }

    follow() {
        return new Promise((resolve) => {
            console.log("follow called")
            resolve(false)
        })
    }

    unfollow() {
        return new Promise((resolve) => {
            console.log("unfollow called")
            resolve(false)
        })
    }

    deleteDn() {
        return new Promise((resolve) => {
            console.log("deleteDn called")
            resolve(false)
        })
    }




}