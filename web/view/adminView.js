const template = `
    <div style="display: contents">
        <header class="subheader">
            <h1>Admin</h1>
        </header>
        <main>
            <p>
                Please <b>let me know</b> about the changes you want to make: <b>kacirek.j@gmail.com</b>
            </p>
            <p>
                <input type="text" v-model="password" placeholder="Enter password to allow changes in config">
            </p>
            <div class="row">
                <div class="col">
                    <h2>Properties config</h2>
                </div>
                <div class="col-4">
                    <h2 class="float-right">
                        <a class="fa-regular fa-floppy-disk" v-on:click="saveProperties()"/>
                    </h2>
                </div>
            </div>
            <table>
            <tbody>
                <tr v-for="property in findProperties">
                    <td>
                        {{property.key}}
                    </td>
                    <td>
                        <input v-model="property.value">          
                    </td>
                </tr>    
            </tbody>
            </table>
                
            <div class="row">
                <div class="col">
                    <h2>Modules config</h2>
                </div>
                <div class="col-4">
                    <h2 class="float-right">
                        <a class="fa-regular fa-plus" v-on:click="addModuleInfo()"/>
                        &nbsp;
                        <a class="fa-regular fa-floppy-disk" v-on:click="saveModuleInfos()"/>
                    </h2>
                </div>
            </div>
            <p>
                <input type="text" v-model="search" placeholder="Search by name">
            </p>
            <div v-for="moduleInfo in findModuleInfos">
                <div class="row">
                    <div class="col">
                        <h3>{{moduleInfo.name}}</h3>
                    </div>
                    <div class="col-4">
                        <h3 class="float-right">
                            <a class="fa-regular fa-trash-can" v-on:click="$set(moduleInfo, '_deleted', true)"/>
                        </h3>
                    </div>
                </div>
                <table>
                    <tbody>
                        <tr v-for="key in Object.keys(moduleInfo)">
                            <td>
                                {{key}}
                            </td>
                            <td>
                                <input v-model="moduleInfo[key]" v-on:input="$set(moduleInfo, '._changed', true)">          
                            </td>
                        </tr>    
                    </tbody>
                </table>
             </div>
        </main>
    </div>
`
export default {
    template,
    data() {
        return {
            password: "",
            search: "",
            moduleInfos: [],
            properties: []
        }
    },
    computed: {
        findModuleInfos() {
            console.log("sort")
            return this.moduleInfos
                .filter(mi => mi.name.includes(this.search))
                .filter(mi => mi._deleted !== true)
                .sort((a, b) => {
                    console.log(a.id, b.id)
                    if (a.id === null || b.id !== null) {
                        return 1;
                    } else {
                        return a.name.localeCompare(b.name);
                    }
                })
        },
        findProperties() {
            return this.properties
                .sort((a, b) => a.key.localeCompare(b.key))
        }
    },
    methods: {
        async saveModuleInfos() {
            const upserts = this.moduleInfos.filter(mi => mi._changed);
            const deletes = this.moduleInfos.filter(mi => mi._deleted);

            const result = window.confirm(
                "Items changed: " + upserts.map(u => u.name).join(", ") + "\n" +
                "Items deleted: " + deletes.map(u => u.name).join(", ")
            );
            if (result) {
                await this.$connector.upsertModuleInfos(upserts);
                await this.$connector.deleteModuleInfos(deletes.map(d => d.id));
                this.moduleInfos = await this.$connector.getModuleInfos();
            }
        },
        async addModuleInfo() {
            const tmp = {
                name: '',
                ip: '',
                port: ''
            }
            this.moduleInfos = [tmp, ...this.moduleInfos]
        },
        async saveProperties() {
            this.properties = await this.$connector.upsertProperties(this.properties)
        },
        async deleteModuleInfo(id) {
            this.moduleInfos = await this.$connector.upsertModuleInfos(this.moduleInfos)
        }
    },
    async mounted() {
        this.moduleInfos = await this.$connector.getModuleInfos();
        this.properties = await this.$connector.getProperties();
    },
}
