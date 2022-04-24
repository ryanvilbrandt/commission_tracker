import {ajax_call} from "./utils.js";
import {ws_init, ws_load, ws_close} from "./mywebsocket.js";

let refresh_button = null;
let opened_details = [];
let current_user_role = null;

export function init(v_current_user_role) {
    current_user_role = v_current_user_role;
    // refresh_button = document.querySelector("#refresh_button");
    // refresh_button.onclick = function() {
    //     refresh_button.disabled = true;
    //     // document.querySelector("#commissions_container").innerHTML = "";
    //     let arg = opened_details.length === 0 ? "_" : opened_details.join(",");
    //     ajax_call(`/fetch_commissions/${arg}`, fetch_commissions_callback)
    // }

    apply_commission_hooks();
    document.querySelectorAll("#force_update_button").forEach(e => e.onclick = force_update);
    apply_user_hooks();

    ws_init("/commissions_websocket", handle_websocket);
    ws_load();

    window.addEventListener("beforeunload", event => {
        console.log("Closing websocket");
        ws_close();
    });
}

function apply_commission_hooks() {
    document.querySelectorAll("details").forEach(e => e.ontoggle = open_details);
    document.querySelectorAll(".show_hide_commissions_checkbox").forEach(e => e.onclick = show_hide_commissions);
    document.querySelectorAll(".claim_button").forEach(e => e.onclick = claim);
    document.querySelectorAll(".accept_button").forEach(e => e.onclick = accept);
    document.querySelectorAll(".reject_button").forEach(e => e.onclick = reject);
    document.querySelectorAll(".invoiced_button").forEach(e => e.onclick = invoiced);
    document.querySelectorAll(".paid_button").forEach(e => e.onclick = paid);
    document.querySelectorAll(".finished_button").forEach(e => e.onclick = finished);
    document.querySelectorAll(".assign_to_user_button").forEach(e => e.onclick = click_assign);
    document.querySelectorAll(".undo_invoiced_button").forEach(e => e.onclick = click_undo_invoiced);
    document.querySelectorAll(".undo_paid_button").forEach(e => e.onclick = click_undo_paid);
}

function apply_user_hooks() {
    document.querySelectorAll(".is_artist_checkbox").forEach(e => e.onclick = change_is_artist);
    document.querySelectorAll(".change_user_username").forEach(e => e.onclick = click_change_username);
    document.querySelectorAll(".change_user_full_name").forEach(e => e.onclick = click_change_full_name);
    document.querySelectorAll(".change_user_password").forEach(e => e.onclick = click_change_password);
    document.querySelectorAll(".delete_user").forEach(e => e.onclick = click_delete_user);
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
    let arg1 = opened_details.length === 0 ? "_" : opened_details.join(",");
    let hidden_queues = [];
    document.querySelectorAll(".show_hide_commissions_checkbox").forEach(function (e) {
        if (!e.checked) {
            hidden_queues.push(e.attributes["queue_owner"].value);
        }
    })
    let arg2 = hidden_queues.length === 0 ? "_" : hidden_queues.join(",");
    ajax_call(`/fetch_commissions/${arg1}/${arg2}`, fetch_commissions_callback);
    if (current_user_role !== "user") {
        ajax_call(`/fetch_users`, fetch_users_callback);
    }
}

function fetch_users_callback(xhttp) {
    document.querySelector("#users").innerHTML = xhttp.responseText;
    apply_user_hooks();
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

function show_hide_commissions(e) {
    let checkbox = e.target;
    let queue_name = checkbox.attributes["queue_owner"].value;
    let hidden = !checkbox.checked;
    document.querySelectorAll(`[queue_name="${queue_name}"]`).forEach(e => e.hidden = hidden);
    document.querySelectorAll(`[queue_name="${queue_name}_inverted"]`).forEach(e => e.hidden = !hidden);
}

function force_update() {
    ajax_call(`/send_to_websockets`, callback);
}

function change_is_artist(event) {
    let user_id = event.target.attributes.user_id.value;
    let is_artist = event.target.checked;
    window.location.href = `/change_is_artist/${user_id}/${is_artist}`;
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

function click_undo_invoiced(event) {
    ajax_call(`/commission_action/undo_invoiced/${event.target.attributes["commission_id"].value}`, callback);
}

function click_undo_paid(event) {
    ajax_call(`/commission_action/undo_paid/${event.target.attributes["commission_id"].value}`, callback);
}

function callback(xhttp) {
    console.log(xhttp.status);
    if (xhttp.status < 400) {
        console.log(xhttp);
    } else {
        console.error(xhttp);
        let msg = `(${xhttp.status}) ${xhttp.statusText} &lt;${xhttp.responseURL}&gt; `
        document.querySelector("#top_error_overlay").appendChild(build_top_error(msg));
        document.querySelectorAll(".top_error_close").forEach(e => e.onclick = close_error);
    }
}

function build_top_error(msg) {
    let error_bar = document.createElement("div");
    error_bar.className = "top_error_message";
    error_bar.innerHTML = `${msg} <span class="top_error_close">✖️</span>`;
    return error_bar;
}

function close_error(e) {
    let message = e.target.parentElement;
    let overlay = message.parentElement;
    overlay.removeChild(message);
}