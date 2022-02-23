export function init() {
    let header = document.querySelector(".header");
    header.onclick = function() {
        let open_arrow = document.querySelector(".open-arrow");
        let body = document.querySelector(".body");
        open_arrow.innerText = body.hidden ? "▲" : "▼";
        body.hidden = !body.hidden;
    };
    console.log(document.querySelectorAll(".change_user_username"));
    document.querySelectorAll(".change_user_username").forEach(e => e.onclick = click_change_username);
    document.querySelectorAll(".delete_user").forEach(e => e.onclick = click_delete_user);
}

function click_change_username(event) {
    let new_username = window.prompt("What do you want to change that user's username to?");
    if (new_username === null) return;
    if (new_username === "") {
        window.alert("You must supply a username.");
        return;
    }
    let user_id = event.target.attributes.user_id.value;
    window.location.href = `/change_username/${user_id}/${new_username}`;
}

function click_delete_user(event) {
    let confirmation = window.confirm("Are you sure you want to delete that user?");
    if (!confirmation) return;
    let user_id = event.target.attributes.user_id.value;
    window.location.href = `/delete_user/${user_id}`;
}
