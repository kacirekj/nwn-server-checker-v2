const template = `
    <div style="display: contents">

        <header>
            <nav class="noprint sticky">
                <ul>
                    <li><router-link to="/"><img style="height: 2em;" src="web/asset/favicon.png"></router-link></li>
                    <li><router-link class="nav-button" :class="{'nav-button-focus': $route.path == '/'}" to="/">Domů</router-link></li>
                    <li><router-link class="nav-button" :class="{'nav-button-focus': $route.path == '/discussion'}" to="/discussion">Kniha návštěv</router-link></li>
                    <li><router-link class="nav-button" :class="{'nav-button-focus': $route.path == '/admin'}" to="/admin">Administrace</router-link></li>
                </ul>
            </nav>
        </header>
 
        <keep-alive>
            <router-view>
                </router-view>
        </keep-alive>
        <footer>
            <p>Copyright (c) Jiří Kačírek 2024, Total visits: {{webVisit.visitCount}}, Unique visits: {{webVisit.unique24hVisitCount}}</p>
        </footer>

    </div>

`
export default {
    template,
    data() {
        return {
            webVisit: {},
            defaultTheme: 'light',
            theme: null,
            activeButtonIdx: null,
            loginVisible: true,
            token: null,
        }
    },
    methods: {
    },
    watch: {
        theme() {
            document.documentElement.setAttribute('data-theme', this.theme)
            sessionStorage.setItem("theme", this.theme)
        },

    },
    async mounted() {
        this.webVisit = await this.$connector.incrementWebVisit();
    },
    created() {
        const theme = sessionStorage.getItem("theme")
        this.theme = theme ? theme : this.defaultTheme
    }
}
