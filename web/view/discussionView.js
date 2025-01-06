//import connector from "../service/connector";

const template = `
    <div style="display: contents">
        <header class="subheader">
            <h1>Diskuze</h1>
        </header>
        <main>
            <h2>Příspěvky</h2>
                
            <div class="card">
                <div class="row">
                    <div class="col">
                        Autor:
                        <input type="text" v-model="newDiscussionItem.author" placeholder="Zadejte svou přezdívku">
                        Kontrolní obrázek:               
                        <input type="text" v-model="captchaGues" @input="captchaGues = captchaGues.toUpperCase()" placeholder="Vepište text z obrázku">               
                    </div>
                    <img class="float-right" :src="captchaSrc">                    
                    <div class="col-4">
                                                                <a class="float-right" v-on:click="createDiscussionItem()">Odeslat</a>
                    </div>
                </div>
                <hr>
                <p>
                    <textarea type="text" v-model="newDiscussionItemComputed.text" placeholder="Zadejte text zprávy"/>
                </p>

            </div>
            <div v-for="item in discussionItems" class="card">
<!--                <div class="row">-->
<!--                    <div class="col-1">-->
<!--                        <img style="height: 2.7em;" src="web/asset/Human_anonymous_3.png">-->
<!--                    </div>-->
                    <div class="col">
                        <div class="row">
                            <div class="col">
                                <b>
                                    {{item.author}}               
                                </b>
                            </div>
                            <div class="col-4">
                                <b class="float-right">
                                    <a class="fa-regular fa-trash-can" v-on:click="deleteDiscussionItem(item.id)"/>
                                </b>
                            </div>
                        </div>   
                                            <small>{{$util.isoDateToReadable(item.created)}}  </small>                                             
                    </div>     
<!--                </div>            -->
                <hr>
                <p v-for="line in $util.stringToNewLineArray(item.text)" >
                {{line}}
                </p>
            </div>
        </main>
    </div>
`
export default {
    template,
    data() {
        return {
            captchaSrc: "",
            captchaGues: "",
            captchaHash: "",
            newDiscussionItem: {author: "", created: new Date(), text: ""},
            discussionItems: []
        }
    },
    computed: {
        newDiscussionItemComputed() {
            this.newDiscussionItem.text = this.newDiscussionItem.text.substring(0, 1000)
            return this.newDiscussionItem;
        }
    },
    methods: {
        async createDiscussionItem() {
            if(this.newDiscussionItem.author.length <= 1 || this.newDiscussionItem.text.length <= 2) {
                window.alert("Zadejte přezdívku a tělo zprávy.")
                return;
            }
            try {
                const result = await this.$connector.createDiscussionItem(this.newDiscussionItem, this.captchaHash, this.captchaGues);
                this.discussionItems = [result, ...this.discussionItems];
                this.newDiscussionItem = {author: "", created: new Date(), text: ""};
                await this.loadCaptcha();
            } catch (e) {
                await this.loadCaptcha();
            }
        },
        async deleteDiscussionItem(id) {
            const password = window.prompt("Zadejte administrátorské heslo: ")
            if(!password) {
                return;
            }
            const result = await this.$connector.deleteDiscussionItems([id], password);
            if(result) {
                this.discussionItems = this.discussionItems.filter(di => di.id != id);
            }
        },
        async loadCaptcha() {
            this.$logger.log()
            const response = await fetch("api/captcha");
            const blob = await response.blob();
            this.captchaGues = "";
            this.captchaSrc = URL.createObjectURL(blob);
            this.captchaHash = response.headers.get("Content-disposition").split("filename=")[1].split(".")[0]
            console.log(this.captchaHash)
        },
        setCaptchaHash(event) {
            const fullPath = event.target.src;
            console.log(event.target)
            // this.imageName = fullPath.split(".").pop(); // Extract the filename
        },
    },
    async mounted() {
        this.discussionItems = await this.$connector.getDiscussionItems();
        await this.loadCaptcha();
        localStorage.setItem("recentDiscussionOpenTimestamp", new Date().toISOString())
    },
}
