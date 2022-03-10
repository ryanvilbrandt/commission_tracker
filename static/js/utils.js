export function ajax_call(url, func, params=null) {
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
                if (this.status === 200) {
                    func(this);
                } else {
                    console.error("Ajax error: " + this.status + " / " + this.error);
                }
                break;
            default:
        }
    };
    xhttp.open(params === null ? "GET" : "POST", url, true);
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    if (params === null) {
        xhttp.send();
    } else {
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
    }
}