import axios from "axios";

export default class PfaApi {
    constructor(jwt) {
        this.service = axios.create({
            headers: {
                Authorization: `Bearer ${jwt}`
            }
        });

        this.routes = {
            "dnList": "/apiv2/dn",
            "dnListExport": "/apiv2/dn/export",
            "dn": "/apiv2/dn",
            "alert": "/apiv2/alert",
            "alertExport": "apiv2/alert/export",
            "resolution": "/apiv2/resolution",
            "channels": "/apiv2/channels",
            "userChannels": "/apiv2/user/channels",
            "tag": "/apiv2/tag",
            "tagLinked": "/apiv2/tag_dn_ip",
            "tagLinkedList": "/apiv2/tag_dn_ip/list/from",
            "password": "/apiv2/password",
            "logout": "/apiv2/logout",
            "apikey": "/apiv2/apikey",
            "apiIntegrations": "/apiv2/apiintegration",
            "userApis": "/apiv2/user/apiintegration"
        };
    }

    logout() {
        return this.service.get(this.routes.logout, {})
        .then(function(d) {
            console.log(d.data.msg);
            return d.data
        })
    }

    getAlertList(filter, filterBy, sortBy, limit) {
        return this.service.get(this.routes.alert, {
            params: {
                days: "1",
                filter: filter,
                filter_by: filterBy,
                sort_by: sortBy,
                limit: limit
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return d.data;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    exportAlertList(filter, filterBy, sortBy, limit, exportType) {
        return this.service.get(this.routes.alertExport, {
            params: {
                days: "1",
                filter: filter,
                filter_by: filterBy,
                sort_by: sortBy,
                limit: limit,
                export: exportType
            }
        })
            .then(function(d) {
                return d.data
            })
    }

    getDnList(owned, followed, filter, filterBy, sortBy, limit) {
        let params = {
            owned: owned,
            followed: followed,
            filter: filter,
            filter_by: filterBy,
            sort_by: sortBy,
            limit: limit
        };

        return this.service.get(this.routes.dnList, {
            params: params
        })
            .then(function(d) {
                console.log(d.data.msg);
                return d.data;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    exportDnList(owned, followed, filter, filterBy, sortBy, limit, exportType) {
        return this.service.get(this.routes.dnListExport, {
            params: {
                owned: owned,
                followed: followed,
                filter: filter,
                filter_by: filterBy,
                sort_by: sortBy,
                limit: limit,
                export: exportType
            }
        })
            .then(function(d) {
                return d.data
            })
    }

    getChannelsAvailableList() {
        return this.service.get(this.routes.channels)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.channel_list
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    getChannelLinkedList() {
        return this.service.get(this.routes.userChannels)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.channel_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    setupChannel(channelName, contact) {
        return this.service.post(`${this.routes.userChannels}/${channelName}`, {}, {
            params: {
                contact: contact
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    verifyChannel(channelName, token) {
        return this.service.put(`${this.routes.userChannels}/${channelName}`, {}, {
            params: {
                token: token
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    testChannel(channelName) {
        return this.service.get(`${this.routes.userChannels}/${channelName}/test`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    removeChannel(channelName) {
        return this.service.delete(`${this.routes.userChannels}/${channelName}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    createDn(domainName) {
        return this.service.post(`${this.routes.dn}/${domainName}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false
            })
    }

    getDn(domainName) {
        return this.service.get(`${this.routes.dn}/${domainName}`)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    getDnHistory(domainName) {
        return this.service.get(`${this.routes.resolution}/${domainName}/history`)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.history;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }


    createTag(tag) {
        return this.service.post(`${this.routes.tag}/${tag}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    getTagList() {
        return this.service.get(this.routes.tag)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.tag_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    getLinkedTagsList(object, type) {
        return this.service.get(this.routes.tagLinkedList, {
            params: {
                object: object,
                type: type
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.tag_link_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    createLinkedTag(object, type, tag) {
        return this.service.post(this.routes.tagLinked, {}, {
            params: {
                object: object,
                type: type,
                tag: tag
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    deleteLinkedTag(object, type, tag) {
        return this.service.delete(`${this.routes.tagLinked}/${tag}/${object}/${type}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    changePassword(currentPassword, newPassword) {
        return this.service.put(this.routes.password, {
            "current_password": currentPassword,
            "new_password": newPassword
        })
            .then(function(d) {
                console.log(d.data.msg);
                return {b: true, msg: d.data.msg};
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return {b: false, msg: err.response.data.msg};
            })
    }

    follow(dn) {
        return this.service.post(`${this.routes.dn}/${dn}/follow`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    unfollow(dn) {
        return this.service.delete(`${this.routes.dn}/${dn}/follow`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    deleteDn(dn) {
        return this.service.delete(`${this.routes.dn}/${dn}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    getExternApisAvailableList() {
        return this.service.get(this.routes.apiIntegrations)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.api_list
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    getExternApiLinkedList() {
        return this.service.get(this.routes.userApis)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.api_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    setupExternApi(externApi, user_key) {
        return this.service.post(`${this.routes.apikey}/${externApi}`, {}, {
            params: {
                api_key: user_key
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    removeExternApi(externApi) {
        return this.service.delete(`${this.routes.apikey}/${externApi}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    requestExternApiDn(externApi, dn) {
        return this.service.post(`${this.routes.apiIntegrations}/dn/${externApi}`, {}, {
            params: {
                domain_name: dn
            }
        })
            .then(function(d) {
                console.log(d.data.msg)
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    requestExternApiIp(externApi, ip) {
        return this.service.post(`${this.routes.apiIntegrations}/ip/${externApi}`, {}, {
            params: {
                ip_address: ip
            }
        })
            .then(function(d) {
                console.log(d.data.msg)
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }
}