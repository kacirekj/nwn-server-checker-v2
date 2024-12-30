const DEBUG = true
const VALUE = true

const methods = {
    log(value0, value1) {
        if (!DEBUG) {
            return
        }
        const caller = (new Error()).stack.split("\n")[2].trim().split(" ")[1]

        if (VALUE) {
            console.log(caller, value0, value1)
        } else {
            console.log(caller)
        }
    }
}
export default new Vue({methods})
