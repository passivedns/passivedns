import PfaApiMock from "../mocks/pfa-api-mock";
import PfaApi from "./pfa-api";
import PfaApiPublic from "./pfa-api-public";
import PfaApiPublicMock from "../mocks/pfa-api-public-mock";

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
}