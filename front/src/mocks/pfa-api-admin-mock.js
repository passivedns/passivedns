import user_request_list from "./data/user-request-list.json"
import user_invite_list from "./data/user-invite-list.json"
import user_list from "./data/user-list.json"
import channel_list from "./data/channels-list.json"

export default class PfaApiAdminMock {
    invite() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot invite people on demo")
        })
    }

    verify() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot verify people on demo")
        })
    }

    requestList() {
        return new Promise((resolve) => {
            resolve(user_request_list.user_request_list)
        })
    }

    requestDelete() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot remove on demo")
        })
    }

    inviteList() {
        return new Promise((resolve) => {
            resolve(user_invite_list.user_pending_list)
        })
    }

    userList() {
        return new Promise((resolve) => {
            resolve(user_list.user_list)
        })
    }

    userDelete() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot delete users on demo")
        })
    }

    channelsList() {
        return new Promise((resolve) => {
            resolve(channel_list.channel_list)
        })
    }

    channelCreate() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot create channels on demo")
        })
    }

    channelUpdate() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot update channels on demo")
        })
    }

    channelRemove() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot remove channels on demo")
        })
    }

    schedulerCreate() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot create scheduler on demo")
        })
    }

    schedulerUpdate() {
        return new Promise((resolve, reject) => {
            resolve(false)
            reject("cannot update scheduler on demo")
        })
    }

}