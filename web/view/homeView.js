//import connector from "../service/connector";

const template = `
    <div style="display: contents">
        <header class="subheader">
            <h1>Neverwinter Nights</h1>
        </header>
        <main>
            <h2>
                Statistika návštěvnosti modulů
            </h2>
            <input type="text" v-model="search" placeholder="Search by name">
            <p>
            </p>
            <div v-for="m in findModuleInfos">
                <h3>
                    {{m.name}}
                    <span>
                        <router-link class="float-right" :to="{path: '/module', query: {id: m.id}}">
                            <i class="fa-solid fa-magnifying-glass"></i>
                        </router-link>
                    </span>
                </h3>
                <moduleInfo v-bind:moduleInfo="m"></moduleInfo>
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
        },
    },
    methods: {},
    async mounted() {
        this.moduleInfos = await this.$connector.getModuleInfos();
        console.log(window.location.search)
        this.search = this.$routeutil.getParam(window.location, "search", "");
        this.$routeutil.setParam(window.location, "test", this.search);
    },
}
