const methods = {
    async getDiscussionItems() {
        this.$logger.log()
        let response = await this.call({
            method: 'GET',
            url: '/api/discussion-items'
        })
        return response.data
    },
    async createDiscussionItem(discussionItem, captchaHash, captchaGues) {
        this.$logger.log()
        let response = await this.call({
            method: 'POST',
            url: '/api/discussion-items',
            data: discussionItem,
            params: {
                captchaHash: captchaHash,
                captchaGues: captchaGues,
            }
        })
        return response.data
    },
    async deleteDiscussionItems(ids, password) {
        this.$logger.log(ids)
        let response = await this.call({
            method: 'DELETE',
            url: '/api/discussion-items',
            params: {
                ids: ids,
                password: password
            }
        })
        return response
    },
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
                password: password
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
            throw e
        }
    }
}
export default new Vue({methods: methods})
