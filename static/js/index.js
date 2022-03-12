import {ajax_call} from "./utils.js";
import {ws_init, ws_load, ws_close} from "./mywebsocket.js";

let refresh_button = null;
let opened_details = [];

export function init() {
    // refresh_button = document.querySelector("#refresh_button");
    // refresh_button.onclick = function() {
    //     refresh_button.disabled = true;
    //     // document.querySelector("#commissions_container").innerHTML = "";
    //     let arg = opened_details.length === 0 ? "_" : opened_details.join(",");
    //     ajax_call(`/fetch_commissions/${arg}`, fetch_commissions_callback)
    // }

    apply_commission_hooks();

    document.querySelectorAll("#force_update_button").forEach(e => e.onclick = force_update)
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

function apply_commission_hooks() {
    document.querySelectorAll("details").forEach(e => e.ontoggle = open_details);
    document.querySelectorAll(".claim_button").forEach(e => e.onclick = claim);
    document.querySelectorAll(".accept_button").forEach(e => e.onclick = accept);
    document.querySelectorAll(".reject_button").forEach(e => e.onclick = reject);
    document.querySelectorAll(".invoiced_button").forEach(e => e.onclick = invoiced);
    document.querySelectorAll(".paid_button").forEach(e => e.onclick = paid);
    document.querySelectorAll(".finished_button").forEach(e => e.onclick = finished);
    document.querySelectorAll(".assign_to_user_button").forEach(e => e.onclick = click_assign);
}

function fetch_commissions_callback(xhttp) {
    document.querySelector("#commissions").innerHTML = xhttp.responseText;
    apply_commission_hooks();
    // refresh_button.disabled = false;
}

function handle_websocket(msg) {
    // refresh_button.disabled = true;
    console.debug(msg);
    if (msg.data === "ping") {
        return;
    }
    let arg = opened_details.length === 0 ? "_" : opened_details.join(",");
    ajax_call(`/fetch_commissions/${arg}`, fetch_commissions_callback);
}

function open_details(e) {
    let details = e.target;
    let commission_id = details.attributes["commission_id"].value;
    if (details.open) {
        if (!opened_details.includes(commission_id)) {
            opened_details.push(commission_id);
        }
    } else {
        if (opened_details.includes(commission_id)) {
            let index = opened_details.indexOf(commission_id);
            opened_details.splice(index, 1);
        }
    }
}

function force_update() {
    ajax_call(`/send_to_websockets`, callback);
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

function claim(event) {
    ajax_call(`/commission_action/claim/${event.target.attributes["commission_id"].value}`, callback);
}

function accept(event) {
    ajax_call(`/commission_action/accept/${event.target.attributes["commission_id"].value}`, callback);
}

function reject(event) {
    ajax_call(`/commission_action/reject/${event.target.attributes["commission_id"].value}`, callback);
}

function invoiced(event) {
    ajax_call(`/commission_action/invoiced/${event.target.attributes["commission_id"].value}`, callback);
}

function paid(event) {
    ajax_call(`/commission_action/paid/${event.target.attributes["commission_id"].value}`, callback);
}

function finished(event) {
    ajax_call(`/commission_action/finished/${event.target.attributes["commission_id"].value}`, callback);
}

function click_assign(event) {
    let commission_id = event.target.attributes["commission_id"].value;
    let user_id = document.querySelector(`#assign_users_dropdown_${commission_id}`).value;
    ajax_call(`/assign_commission/${commission_id}/${user_id}`, callback);
}

function callback(xhttp) {
    console.log(xhttp);
}