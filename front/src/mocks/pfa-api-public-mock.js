import infos from "./data/infos.json"
import token from "./data/token.json"

export default class PfaApiPublicMock {
    getInfos() {
        return new Promise(() => {
            return infos
        })
    }

    login(username, password) {
        return new Promise(() => {
            if (username !== 'demo' || password !== 'demo') {
                throw "invalid demo credentials"
            }
            return token
        })
    }

    checkJwt(jwt) {

        // fixme: use this for all mocks
        return new Promise((resolve) => {
            setTimeout(() => {
                if (jwt === 'token') {
                        resolve(true)
                } else {
                    resolve(false)
                }
            }, 1000)

        })
    }

    requestAccess() {
        return new Promise(() => {
            return true
        })
    }

    register() {
        return new Promise(() => {
            throw "cannot register on demo"
        })
    }

    checkRegisterToken() {
        return new Promise(() => {
            throw "cannot register on demo"
        })
    }
}