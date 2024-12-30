const methods = {
    async getModuleInfos() {
        this.$logger.log()
        let response = await this.call({
            method: 'GET',
            url: '/api/module-infos'
        })
        return response.data
    },
    async upsertModuleInfos(moduleInfos, password) {
        this.$logger.log()
        let response = await this.call({
            method: 'POST',
            url: '/api/module-infos',
            data: moduleInfos,
            params: {
                password: password
            }
        })
        return response.data
    },
    async deleteModuleInfos(ids, password) {
        this.$logger.log(ids)
        let response = await this.call({
            method: 'DELETE',
            url: '/api/module-infos',
            params: {
                ids: ids,
                params: {
                    password: password
                }
            }
        })
        return response.data
    },
    async getProperties() {
        this.$logger.log()
        let response = await this.call({
            method: 'GET',
            url: '/api/properties'
        })
        return response.data
    },
    async upsertProperties(properties, password) {
        this.$logger.log()
        let response = await this.call({
            method: 'POST',
            url: '/api/properties',
            data: properties,
            params: {
                password: password
            }
        })
        return response.data
    },
    async call(params) {
        try {
            return await axios({
                ...params,
                headers: {}
            })
        } catch (e) {
            let msg = e.response.data.error + ": " + e.response.data.message;
            window.alert(msg);
            console.log(e)
            return null;
        }
    }
}
export default new Vue({methods: methods})
