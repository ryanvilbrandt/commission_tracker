export function init() {
    document.querySelectorAll(".change_user_username").forEach(e => e.onclick = click_change_username);
    document.querySelectorAll(".change_user_full_name").forEach(e => e.onclick = click_change_full_name);
    document.querySelectorAll(".change_user_password").forEach(e => e.onclick = click_change_password);
    document.querySelectorAll(".delete_user").forEach(e => e.onclick = click_delete_user);
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
