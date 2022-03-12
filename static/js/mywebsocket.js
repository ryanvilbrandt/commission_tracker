let ws = null;
let ws_loaded = false;
let websocket_errors = 0;
let websocket_uri = null;
let handle_websocket = null;
let max_websocket_errors = 3;


export function ws_init(v_websocket_uri, v_handle_websocket) {
    websocket_uri = v_websocket_uri;
    handle_websocket = v_handle_websocket;
}

export function ws_load() {
    let loc = window.location;
    let ws_uri = (loc.protocol === "https:") ? "wss:" : "ws:";
    ws_uri += `//${loc.host}${websocket_uri}`;
    console.debug(ws_uri);
    ws = new WebSocket(ws_uri);
    set_hooks();
    ws_loaded = true;
    console.log(`Loaded websocket`);
}

function set_hooks() {
    ws.onopen = () => {
        // Set onclose hook only after the websocket has successfully been opened
        ws.onclose = () => on_websocket_close();
    }
    ws.onmessage = (msg) => {
        let error_msg = document.getElementById("websocket_error_overlay");
        if (error_msg !== null)
            error_msg.hidden = true;
        websocket_errors = 0;
        handle_websocket(msg);
    };
    ws.onerror = function (error) {
        console.debug("Triggering from onerror");
        on_websocket_error(error);
    }
}

function on_websocket_error(error) {
    if (!ws_loaded) return;
    websocket_errors += 1;
    console.error(`WebSocket error (${websocket_errors} / ${max_websocket_errors}):`);
    console.error(error);
    quiet_close();
    if (websocket_errors >= max_websocket_errors) {
        console.error("Hit max websocket connection attempts. Giving up.");
        let error_msg = document.getElementById("websocket_error_overlay");
        if (error_msg !== null) {
            error_msg.innerText = `Failed to connect to WebSocket after ${websocket_errors} attempts.\n` +
                `Please reload page to try again.`;
            error_msg.hidden = false;
        }
        return;
    }
    console.log("Reconnecting in 5 seconds...");
    setTimeout(ws_load, 5000);
}

function on_websocket_close() {
    console.log("Triggering from onclose");
    on_websocket_error("Websocket closed");
    ws_loaded = false;
}

function quiet_close() {
    // If the websocket errored out but is still open, close it first before continuing
    if (ws !== null && ws.readyState < ws.CLOSING) {
        ws.onclose = null;
        ws.close();
    }
    ws_loaded = false;
}

export function ws_close() {
    quiet_close();
}