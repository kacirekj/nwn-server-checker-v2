const template = `
    <div style="display: contents">

        <header>
            <nav class="noprint sticky">
                <ul>
                    <li><router-link to="/"><img style="height: 2.5em;" src="web/asset/favicon.png"></router-link></li>
                    <li><router-link class="nav-button" :class="{'nav-button-focus': $route.path == '/'}" to="/"><i class="fa-solid fa-house"></i> Statistika</router-link></li>
                    <li><router-link class="nav-button" :class="{'nav-button-focus': $route.path == '/discussion'}" to="/discussion"><i class="fa-solid fa-comment"></i> Diskuze <sup v-if="findRecentDiscussionItemsCount > 0" class="notification">{{findRecentDiscussionItemsCount}}</sup></router-link></li>
                    <li><router-link class="nav-button" :class="{'nav-button-focus': $route.path == '/admin'}" to="/admin"><i class="fa-solid fa-gear"></i> Admin</router-link></li>
                    <li class="float-right"><a class="nav-button" href="https://iscandar.ch"><small><i class="fa-solid fa-earth-europe"/> Iscandar.ch</small></a></li>
                    <li class="float-right"><a class="nav-button" href="https://raw.githack.com/kacirekj/demona-kalkulacka/master/dnd_kalkulacka_zraneni.html"></i><small><i class="fa-solid fa-earth-europe"/> Kalkulačka D&D</small></a></li>
                    <li class="float-right"><a class="nav-button" href="https://new.neverwinter.cz"><small><i class="fa-solid fa-earth-europe"/>  Neverwinter.cz</small></a></li>
                </ul>
            </nav>
        </header>
 
            <router-view>
                </router-view>
        <footer>
            <p>Author: <a :href="'mailto:' + 'kacirek.j' + '@' + 'gmail.com'">Jiří Kačírek</a> 2024, Total visits: {{webVisit.visitCount}}, Unique visits: {{webVisit.unique24hVisitCount}}</p>
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
            recentDiscussionItems: [],
            recentDiscussionOpenTimestamp: null,
        }
    },
    computed: {
        findRecentDiscussionItemsCount() {
            console.log("findRecentDiscussionItemsCount")
            const count = this.recentDiscussionItems
                .filter(item => this.recentDiscussionOpenTimestamp.getTime() < new Date(item.created).getTime())
                .length;
            if(count > 0) {
                document.title = "NWN - Statistika (" + count + ")";
            } else {
                document.title = "NWN - Statistika";
            }
            return count;
        }
    },
    methods: {
        updateSessionStorage() {
            const recentDiscussionOpenTimestamp = localStorage.getItem("recentDiscussionOpenTimestamp");
            this.recentDiscussionOpenTimestamp =  recentDiscussionOpenTimestamp ? new Date(recentDiscussionOpenTimestamp) : new Date("2000-01-01T00:00:00Z");
        },
    },
    watch: {
        theme() {
            document.documentElement.setAttribute('data-theme', this.theme)
            localStorage.setItem("theme", this.theme)
        },
    },
    async mounted() {
        this.updateSessionStorage();
        this.recentDiscussionItems = await this.$connector.getDiscussionItems();

        setInterval(() => this.updateSessionStorage(), 1000);
        setInterval(async () => {
            this.recentDiscussionItems = await this.$connector.getDiscussionItems();
        }, 5000);
        this.webVisit = await this.$connector.incrementWebVisit();
    },
    created() {
        const theme = localStorage.getItem("theme")
        this.theme = theme ? theme : this.defaultTheme
    }
}
