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
        <figure>
            <img :src="'web/asset/' + moduleInfo.name + '-chart.png'" style="max-width: 100%; max-height: 100%;" alt="Chart not found.">
        </figure>
    </div>
`
export default {
    template,
    props: ['moduleInfo'],
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
