//import connector from "../service/connector";

const template = `
    <div style="display: contents">
        <header class="subheader">
            <h1>Neverwinter Nights - Statistika návštěvnosti</h1>
        </header>
        <main>
            <h2>Persistentní moduly</h2>
            <p>
                <input type="text" v-model="search" placeholder="Search by name">
            </p>
            <div v-for="m in findModuleInfos">
                <h3>{{m.name}}</h3>
                
                <table>
                    <tbody>
                        <tr>
                            <td>IP</td>
                            <td>{{m.ip}}:{{m.port}}</td>
                        </tr>
                        <tr>
                            <td>Hráčů online</td>
                            <td>{{m.players}}</td>
                        </tr>
                        <tr>
                            <td>Poslední aktualizace (UTC)</td>
                            <td>{{$util.isoDateToReadable(m.updated)}}</td>
                        </tr>
                    </tbody>
                </table>
                <figure>
                    <img :src="'web/asset/' + m.name + '-chart.png'" style="max-width: 100%; max-height: 100%;" alt="Chart not found.">
                </figure>
             </div>
        </main>
    </div>
`
export default {
    template,
    data() {
        return {
            search: "",
            moduleInfos: []
        }
    },
    computed: {
        findModuleInfos() {
            return this.moduleInfos
                .filter(mi => mi.name.includes(this.search))
                .sort((a, b) => a.name.localeCompare(b.name))
        }
    },
    methods: {},
    async mounted() {
        this.moduleInfos = await this.$connector.getModuleInfos();
    },
}
