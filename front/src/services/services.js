import PfaApi from "./pfa-api.js";
import PfaApiPublic from "./pfa-api-public.js";
import * as jwt from "jsonwebtoken";
import PfaApiAdmin from "./pfa-api-admin.js";

export default class Services {

    static getPfaApiService(jwt) {
        return new PfaApi(jwt)
    }

    static getPfaApiPublicService() {
        return new PfaApiPublic()

    }

    static getPfaApiAdminService(jwt) {
        return new PfaApiAdmin(jwt)
    }

    static decodeJwt(token) {
        return jwt.decode(token)
    }

    static newHttpError(msg) {
        let err = {};
        err.response = {}
        err.response.data = {}
        err.response.data.msg = msg
        return err
    }
}