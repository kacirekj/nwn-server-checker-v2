const methods = {
    isoDateToReadable: function (isoDateStr) {
        const date = new Date(isoDateStr);
        return date.toLocaleString();
    },
    stringToNewLineArray: function (str) {
        if(!str) {
            return []
        }
        return str.split('\n');
    },
}
export default new Vue({methods})
