//import connector from "../service/connector";

const template = `
    <div style="display: contents">
        <header class="subheader">
            <h1>Detail modulu</h1>
        </header>
        <main>
            <h2>{{moduleInfo.name}}</h2>
            <moduleInfo v-bind:moduleInfo="moduleInfo"></moduleInfo>
        </main>
    </div>
`
export default {
    template,
    data() {
        return {
            moduleId: "",
            moduleInfo: {}
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
        this.moduleId = this.$routeutil.getParam(window.location, "id", "");
        const moduleInfos = await this.$connector.getModuleInfos([this.moduleId]);
        this.moduleInfo = moduleInfos[0];
    },
}
