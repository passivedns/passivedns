import axios from "axios";
import config from "./config.json"

export default class PfaApiPublic {
    constructor() {
        this.service = axios.create({
            baseURL: config.host,
        });

        this.routes = {
            "infos": "/infos",
            "login": "/login",
            "request": "/request",
            "registerCheck": "/register/check",
            "register": "/register"
        };
    }

    getInfos() {
        return this.service.get(this.routes.infos)
            .then(function(response) {
                return response.data
            })
    }

    login(identity, password) {
        return this.service.post(this.routes.login, {
            identity: identity,
            password: password
        })
            .then(function(response) {
                return response.data.access_token
            })

    }

    checkJwt(jwt) {
        return this.service.get(this.routes.login, {
            headers: {
                "Authorization": `Bearer ${jwt}`
            }
        })
            .then(function() {
                return true

            })
            .catch(function() {
                return false
            })
    }

    requestAccess(email) {
        return this.service.post(this.routes.request, {
            "email": email
        })
            .then(function(d) {
                console.log(d.data.msg)
            })
    }

    register(token, username, password) {
        return this.service.post(this.routes.register, {
            username: username,
            password: password
        }, {
            params: {
                token: token
            }
        })
            .then(function(response) {
                console.log(response.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    checkRegisterToken(token) {
        return this.service.post(this.routes.registerCheck, {}, {
            params: {
                token: token
            }
        })
            .then(function(r) {
                console.log(r.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

}