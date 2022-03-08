import {ajax_call} from "./utils.js";
import {ws_init, ws_load, ws_close} from "./mywebsocket.js";

let refresh_button = null;
let opened_details = [];

export function init() {
    refresh_button = document.querySelector("#refresh_button");
    refresh_button.onclick = function() {
        refresh_button.disabled = true;
        // document.querySelector("#commissions_container").innerHTML = "";
        ajax_call(`/fetch_commissions/${opened_details.join(",")}`, fetch_commissions_callback)
    }

    document.querySelectorAll("details").forEach(e => e.ontoggle = open_details)

    document.querySelectorAll(".change_user_username").forEach(e => e.onclick = click_change_username);
    document.querySelectorAll(".change_user_full_name").forEach(e => e.onclick = click_change_full_name);
    document.querySelectorAll(".change_user_password").forEach(e => e.onclick = click_change_password);
    document.querySelectorAll(".delete_user").forEach(e => e.onclick = click_delete_user);

    ws_init("/commissions_websocket", handle_websocket);
    ws_load();

    window.addEventListener("beforeunload", event => {
        console.log("Closing websocket");
        ws_close();
    });
}

function fetch_commissions_callback(xhttp) {
    document.querySelector("#commissions_container").innerHTML = xhttp.responseText;
    document.querySelectorAll("details").forEach(e => e.ontoggle = open_details)
    refresh_button.disabled = false;
}

function handle_websocket(msg) {
    refresh_button.disabled = true;
    console.log(msg);
    ajax_call(`/fetch_commissions/${opened_details.join(",")}`, fetch_commissions_callback);
}

function open_details(e) {
    let details = e.target;
    let commission_id = details.attributes["commission_id"].value;
    console.log(details);
    if (details.open) {
        if (!opened_details.includes(commission_id)) {
            console.log("Push");
            opened_details.push(commission_id);
        }
    } else {
        if (opened_details.includes(commission_id)) {
            console.log("Pop");
            let index = opened_details.indexOf(commission_id);
            opened_details.splice(index, 1);
        }
    }
    console.log(opened_details);
}

function change_user_property(event, property) {
    let human_property = property.replace("_", " ");
    let new_value = window.prompt(`What do you want to change that user's ${human_property} to?`);
    if (new_value === null) return;
    if (new_value === "") {
        window.alert(`You must supply a valid ${human_property}.`);
        return;
    }
    let user_id = event.target.attributes.user_id.value;
    window.location.href = `/change_${property}/${user_id}/${new_value}`;
}

function click_change_username(event) {
    change_user_property(event, "username");
}

function click_change_full_name(event) {
    change_user_property(event, "full_name");
}

function click_change_password(event) {
    change_user_property(event, "password");
}

function click_delete_user(event) {
    let confirmation = window.confirm("Are you sure you want to delete that user?");
    if (!confirmation) return;
    let user_id = event.target.attributes.user_id.value;
    window.location.href = `/delete_user/${user_id}`;
}
