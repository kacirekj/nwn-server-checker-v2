const methods = {
  getParam: function (location, parameterName, orElseGet) {
    const search = new URLSearchParams(location.search);
    const param = search.get(parameterName);
    return param ? param : orElseGet;
  },
  getParamStringArray: function (location, parameterName, orElseGet) {
    const param = this.getParam(location, parameterName);
    return param ? param.split(",") : orElseGet;
  },
  getParamNumberArray: function (location, parameterName, orElseGet) {
    const param = this.getParam(location, parameterName);
    return param ? param.split(",").map((p) => Number(p)) : orElseGet;
  },
  setParam: function (location, parameterName, value) {
    const search = new URLSearchParams(location.search);
    search.set(parameterName, value);
    return location.pathname + "?" + search.toString();
  },
  deleteParam: function (location, parameterName) {
    const search = new URLSearchParams(location.search);
    search.delete(parameterName);
    return location.pathname + "?" + search.toString();
  },
};

export default new Vue({methods})
