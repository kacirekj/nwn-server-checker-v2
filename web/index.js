/**
 *  Import
 */

// Components

// Services

import connector from "./service/connector.js";
import constant from "./service/constant.js";
import filter from "./service/filter.js";
import logger from './service/logger.js'
import model from './service/model.js'
import util from './service/util.js'

// Views

import appView from './view/appView.js'
import adminView from './view/adminView.js'
import discussionView from "./view/discussionView.js";
import homeView from './view/homeView.js'

/**
 *  Bind
 */

// Components

// Services

Vue.prototype.$connector = connector
Vue.prototype.$constant = constant
Vue.prototype.$filter = filter
Vue.prototype.$logger = logger
Vue.prototype.$model = model
Vue.prototype.$util = util

// Views

Vue.component('appView', appView)
const routes = [
    {path: '/', component: homeView},
    {path: '/admin', component: adminView},
    {path: '/discussion', component: discussionView}
]

// Global mixin

Vue.mixin({
    filters: filter,
})


// Create app

const App = {
    el: '#vueApp',
    router: new VueRouter({mode: 'history', routes: routes}),
}

window.addEventListener('load', () => {
    new Vue(App);
})
