import dn_list from "./data/dn-list.json"
import dn_list_export from "./data/dn-list-export.json"
import available_channels_list from "./data/available-channels-list.json"
import linked_channels_list from "./data/linked-channels-list.json"
import dn from "./data/dn.json"
import dn_history from "./data/dn-history.json"

export default class PfaApiMock {
    getAlertList() {
        return new Promise(() => {
            return dn_list
        })
    }

    exportAlertList() {
        return new Promise(() => {
            return dn_list_export
        })
    }

    getDnList() {
        return new Promise(() => {
            return dn_list
        })
    }

    exportDnList() {
        return new Promise(() => {
            return dn_list_export
        })
    }

    getChannelsAvailableList() {
        return new Promise(() => {
            return available_channels_list
        })
    }

    getChannelLinkedList() {
        return new Promise(() => {
            return linked_channels_list
        })
    }

    setupChannel() {
        return new Promise(() => {
            console.log("setupChannel called")
            return true
        })

    }

    verifyChannel() {
        return new Promise(() => {
            console.log("verifyChannel called")
            return true
        })
    }

    testChannel() {
        return new Promise(() => {
            console.log("testChannel called")
            return true
        })
    }

    removeChannel() {
        return new Promise(() => {
            console.log("removeChannel called")
            return true
        })
    }

    createDn() {
        return new Promise(() => {
            console.log("createDn called")
            return true
        })
    }

    getDn() {
        return new Promise(() => {
            return dn
        })
    }

    getDnHistory() {
        return new Promise(() => {
            return dn_history
        })
    }
}