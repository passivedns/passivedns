import PfaApiMock from "../mocks/pfa-api-mock.js";
import PfaApi from "./pfa-api.js";
import PfaApiPublic from "./pfa-api-public.js";
import PfaApiPublicMock from "../mocks/pfa-api-public-mock.js";
import * as jwt from "jsonwebtoken";
import user_token from "../mocks/data/user_token.json"
import admin_token from "../mocks/data/admin-token.json"
import PfaApiAdminMock from "../mocks/pfa-api-admin-mock.js";
import PfaApiAdmin from "./pfa-api-admin.js";

export default class Services {

    static isDemo() {
        return process.env.VUE_APP_DEMO === 'true'
    }

    static getPfaApiService(jwt) {
        if (this.isDemo()) {
            return new PfaApiMock()
        } else {
            return new PfaApi(jwt)
        }
    }

    static getPfaApiPublicService() {
        if (this.isDemo()) {
            return new PfaApiPublicMock()
        } else {
            return new PfaApiPublic()
        }
    }

    static getPfaApiAdminService(jwt) {
        if (this.isDemo()) {
            return new PfaApiAdminMock()
        } else {
            return new PfaApiAdmin(jwt)
        }
    }

    static decodeJwt(token) {
        if (this.isDemo()) {
            if (token === user_token.access_token) {
                return {role: "user", sub: "demo"}
            } else if (token === admin_token.access_token) {
                return {role: "admin", sub: "admin"}
            }
        } else {
            return jwt.decode(token)
        }
    }

    static newHttpError(msg) {
        let err = {};
        err.response = {}
        err.response.data = {}
        err.response.data.msg = msg
        return err
    }
}