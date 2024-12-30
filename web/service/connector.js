const methods = {
    async getModuleInfos() {
        this.$logger.log()
        let response = await this.call({
            method: 'GET',
            url: '/api/module-infos'
        })
        return response.data
    },
    async upsertModuleInfos(moduleInfos) {
        this.$logger.log()
        let response = await this.call({
            method: 'POST',
            url: '/api/module-infos',
            data: moduleInfos
        })
        return response.data
    },
    async deleteModuleInfos(ids) {
        this.$logger.log(ids)
        let response = await this.call({
            method: 'DELETE',
            url: '/api/module-infos',
            params: {
                ids: ids
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
    async upsertProperties(properties) {
        this.$logger.log()
        let response = await this.call({
            method: 'POST',
            url: '/api/properties',
            data: properties
        })
        return response.data
    },
    async call(params) {
        return axios({
            ...params,
            headers: {}
        })
    }
}
export default new Vue({methods: methods})
