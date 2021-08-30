import infos from "./data/infos.json"
import user_token from "./data/user_token.json"
import admin_token from "./data/admin-token.json"
import Services from "../services/services";

export default class PfaApiPublicMock {
    getInfos() {
        return new Promise((resolve) => {
            resolve(infos)
        })
    }

    login(username, password) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (username === 'demo' && password === 'demo') {
                    resolve(user_token.access_token)
                } else if (username === 'admin' && password === 'admin') {
                    resolve(admin_token.access_token)
                } else {
                    reject("invalid demo credentials")
                }

            }, 1000)
        })
    }

    checkJwt(jwt) {
        return new Promise((resolve) => {
            setTimeout(() => {
                if (jwt === user_token.access_token || jwt === admin_token.access_token) {
                        resolve(true)
                } else {
                    resolve(false)
                }
            }, 1000)

        })
    }

    requestAccess() {
        return new Promise((resolve, reject) => {
            reject(Services.newHttpError("cannot register on demo"))
        })
    }

    register() {
        return new Promise((resolve) => {
            resolve(false)
        })
    }

    checkRegisterToken() {
        return new Promise((resolve, reject) => {
            reject("cannot register on demo")
        })
    }
}