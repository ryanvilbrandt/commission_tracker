export function ajax_call(url, func, params=null, form_data=null) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        switch (this.readyState) {
            case 0:
                break;
            case 1:
                console.debug("Ajax opened " + url);
                break;
            case 2:
                console.debug("Ajax status/headers received " + this.status + " / " + this.getAllResponseHeaders());
                break;
            case 3:
                console.debug("Ajax loading response text");
                break;
            case 4:
                func(this);
                // if (this.status === 200) {
                //     func(this);
                // } else {
                //     console.error("Ajax error: " + this.status + " / " + this.error);
                // }
                break;
            default:
        }
    };
    const call_type = params === null && form_data === null ? "GET" : "POST";
    xhttp.open(call_type, url, true);
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    if (params !== null) {
        let post_params;
        if (typeof params === "string") {
            post_params = params;
        } else {
            post_params = Object.keys(params).map(
                k => encodeURIComponent(k) + "=" + encodeURIComponent(params[k])
            ).join("&");
        }
        xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhttp.send(post_params);
    } else if (form_data !== null) {
        xhttp.send(form_data);
    } else {
        xhttp.send();
    }
}