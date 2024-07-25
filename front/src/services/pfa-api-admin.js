import axios from "axios";

export default class PfaApiAdmin {
    constructor(jwt) {
        this.service = axios.create({
            headers: {
                Authorization: `Bearer ${jwt}`
            }
        });

        this.routes = {
            "userList": "/apiv2/admin/users/list",
            "users": "/apiv2/admin/users",
            "channels": "/apiv2/admin/channels",
            "scheduler": "/apiv2/admin/scheduler"
        };
    }

    userList() {
        return this.service.get(this.routes.userList)
            .then(function(d) {
                return d.data.user_list
            })
            .catch(function(err) {
                console.log(err.response.msg)
            })
    }

    userDelete(username) {
        return this.service.delete(`${this.routes.users}/${username}`)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.user
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    userCreate(username, password) {
        return this.service.post(`${this.routes.users}/${username}`, {
            password: password,
        })
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.user
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    channelsList() {
        return this.service.get(this.routes.channels)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.channel_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    channelCreate(name, infos, type) {
        return this.service.post(`${this.routes.channels}/${name}`, {
            type: type,
            infos: infos
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

    channelUpdate(name, infos, type) {
        return this.service.put(`${this.routes.channels}/${name}`, {
            type: type,
            infos: infos
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

    channelRemove(name) {
        return this.service.delete(`${this.routes.channels}/${name}`)
            .then(function(d) {
                console.log(d.data.msg);
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    schedulerCreate(name, password) {
        return this.service.post(`${this.routes.scheduler}/${name}`, {
            password: password
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false
            })
    }

    schedulerUpdate(name, password) {
        return this.service.put(`${this.routes.scheduler}/${name}`, {
            password: password
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false
            })

    }

}