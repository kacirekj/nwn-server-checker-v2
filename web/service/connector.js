const methods = {
    async getModuleInfos() {
        this.$logger.log()
        let response = await this.call({
            method: 'GET',
            url: '/api/module-infos'
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
