import {ajax_call} from "./utils.js";
import {ws_init, ws_load, ws_close} from "./mywebsocket.js";

let refresh_button = null;
let opened_details = [];
let current_user_role = null;
let current_user_is_artist = null;

export function init(v_current_user_role, v_current_user_is_artist) {
    current_user_role = v_current_user_role;
    current_user_is_artist = v_current_user_is_artist === "1";
    // refresh_button = document.querySelector("#refresh_button");
    // refresh_button.onclick = function() {
    //     refresh_button.disabled = true;
    //     // document.querySelector("#commissions_container").innerHTML = "";
    //     let arg = opened_details.length === 0 ? "_" : opened_details.join(",");
    //     ajax_call(`/fetch_commissions/${arg}`, fetch_commissions_callback)
    // }

    apply_commission_hooks();
    // Handle bug where page can be reloaded with checkboxes unchecked
    document.querySelectorAll(".show_hide_commissions_checkbox").forEach(function (e) {
        e.target = e;
        show_hide_commissions(e);
    });
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
    document.querySelectorAll(".action_button").forEach(button => set_action_button(button));
    document.querySelectorAll(".assign_to_user_button").forEach(e => e.onclick = click_assign);
    // document.querySelectorAll(".undo_invoiced_button").forEach(e => e.onclick = click_undo_invoiced);
    // document.querySelectorAll(".undo_paid_button").forEach(e => e.onclick = click_undo_paid);
    document.querySelectorAll(".commission-upload").forEach(e => init_commission_upload(e));
}

function apply_user_hooks() {
    document.querySelectorAll(".is_artist_checkbox").forEach(e => e.onclick = change_is_artist);
    document.querySelectorAll(".queue_open_checkbox").forEach(e => e.onclick = change_queue_open);
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
    if (msg.data === "refresh" || msg.data === "users" || msg.data === "queue_open") {
        if (current_user_role !== "user") {
            ajax_call(`/fetch_users`, fetch_users_callback);
        }
    }
    if (msg.data === "refresh" || msg.data === "queue_open") {
        if (current_user_is_artist) {
            ajax_call(`/fetch_queue_open`, fetch_queue_open_callback);
        }
    }
    if (msg.data === "refresh" || msg.data === "commissions") {
        let arg1 = opened_details.length === 0 ? "_" : opened_details.join(",");
        let hidden_queues = [];
        document.querySelectorAll(".show_hide_commissions_checkbox").forEach(function (e) {
            if (!e.checked) {
                hidden_queues.push(e.attributes["queue_owner"].value);
            }
        })
        let arg2 = hidden_queues.length === 0 ? "_" : hidden_queues.join(",");
        ajax_call(`/fetch_commissions/${arg1}/${arg2}`, fetch_commissions_callback);
    }
}

function fetch_users_callback(xhttp) {
    document.querySelector("#users").innerHTML = xhttp.responseText;
    apply_user_hooks();
}

function fetch_queue_open_callback(xhttp) {
    let checked = xhttp.responseText === "true";
    document.querySelector("#current_user_queue_open_checkbox").checked = checked;
    apply_user_hooks();
}

function open_details(e) {
    let details = e.target;
    if (!details.attributes["commission_id"]) return;
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
    if (hidden) {
        checkbox.parentElement.classList.add("queue_hidden");
    } else {
        checkbox.parentElement.classList.remove("queue_hidden");
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
    const params = {
        "user_id": user_id,
        "new_value": new_value
    }
    ajax_call(`/change_${property}`, callback, params);
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
    const params = {
        "user_id": user_id
    }
    ajax_call(`/delete_user`, callback, params);
}

function change_is_artist(event) {
    let user_id = event.target.attributes.user_id.value;
    let is_artist = event.target.checked;
    const params = {
        "user_id": user_id,
        "is_artist": is_artist
    }
    ajax_call(`/change_is_artist`, callback, params);
}

function change_queue_open(event) {
    let user_id = event.target.attributes.user_id.value;
    let queue_open = event.target.checked;
    const params = {
        "user_id": user_id,
        "queue_open": queue_open
    }
    ajax_call(`/change_queue_open`, callback, params);
}

function set_action_button(button) {
    if (button.classList.contains("claim")) {
        button.onclick = claim;
    } else if (button.classList.contains("accept")) {
        button.onclick = accept;
    } else if (button.classList.contains("reject")) {
        button.onclick = reject;
    } else if (button.classList.contains("invoiced")) {
        button.onclick = invoiced;
    } else if (button.classList.contains("paid")) {
        button.onclick = paid;
    } else if (button.classList.contains("finished_button")) {
        button.onclick = finished;
    } else {
        console.error(`Unknown button class: ${button.classList}`);
    }
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
    const commission_id = event.target.getAttribute("commission_id");
    const uploaded_files = document.querySelector(`.commission-upload[commission_id="${commission_id}"]`).files;
    console.log(uploaded_files);
    // if (uploaded_files.length === 0) {
    //     let confirmation = window.confirm(
    //         "Are you sure you want mark this commission as finished without uploading a file?"
    //     );
    //     if (!confirmation) return;
    // }
    let form_data = new FormData();
    form_data.append("image_file", uploaded_files[0]);
    form_data.append("commission_id", event.target.attributes["commission_id"].value);
    console.log(form_data);
    ajax_call(`/finish_commission`, callback, null, form_data);
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
        if (xhttp.response) {
            window.alert(xhttp.response);
        }
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

function init_commission_upload(element) {
    element.addEventListener("change", on_commission_upload, false);
    // Check if the file_list is already filled on load (can happen on refresh) and undisable button immediately
    const file_list = element.files;
    if (file_list.length > 0) {
        on_commission_upload(null, element);
    }
}

function on_commission_upload(event, v_element=null) {
    let element;
    if (v_element !== null) {
        element = v_element;
    } else {
        element = event.target;
    }
    const file = element.files[0];
    const commission_id = element.getAttribute("commission_id");
    const finished_button = document.querySelector(`.finished_button[commission_id="${commission_id}"]`);
    finished_button.disabled = false;
    finished_button.classList.remove("disabled_button");
    finished_button.title = "Mark as Finished";

    const reader = new FileReader();
    const upload_preview = document.querySelector(`.upload_preview[commission_id="${commission_id}"]`);
    reader.onload = (function(aImg) {
        return function(e) {
            aImg.src = e.target.result;
            aImg.hidden = false;
        };
    })(upload_preview);
    reader.readAsDataURL(file);
}