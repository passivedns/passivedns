import axios from "axios";

export default class PfaApiPublic {
    constructor() {
        this.service = axios.create({
        });

        this.routes = {
            "infos": "/apiv2/infos",
            "login": "/apiv2/token",
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

}