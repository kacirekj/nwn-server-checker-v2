const template = `
    <div style="display: contents">
        <table>
            <tbody>
                <tr>
                    <td>IP</td>
                    <td>{{moduleInfo.ip}}:{{moduleInfo.port}}</td>
                </tr>
                <tr>
                    <td>Hráčů online</td>
                    <td>{{moduleInfo.players}}</td>
                </tr>
                <tr>
                    <td>Poslední aktualizace (CET)</td>
                    <td>{{ $moment(moduleInfo.updated + "Z").tz('Europe/Berlin').format('DD/MM/YYYY, HH:mm:ss') }}</td>
                </tr>
            </tbody>
        </table>
        <h3 v-if="displayRecentPeriod">Od začátku</h3>
            <figure>
                <img :src="'web/asset/' + moduleInfo.name + '-chart.png'" style="max-width: 100%; max-height: 100%;" alt="Chart not found.">
            </figure>
        <div v-if="displayRecentPeriod">
            <h3>Poslední 4 týdny</h3>
            <figure >
                <img :src="'web/asset/' + moduleInfo.name + '-chart-recent.png'" style="max-width: 100%; max-height: 100%;" alt="Chart not found.">
            </figure>
        </div>
        

    </div>
`
export default {
    template,
    props: ['moduleInfo', 'displayRecentPeriod'],
    emits: [],
    data() {
        return {
        }
    },
    computed: {
    },
    methods: {
    },
    mounted() {
    }
}
