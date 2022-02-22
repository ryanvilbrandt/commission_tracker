export function init() {
    let header = document.querySelector(".header");
    header.onclick = function() {
        let open_arrow = document.querySelector(".open-arrow");
        let body = document.querySelector(".body");
        open_arrow.innerText = body.hidden ? "▲" : "▼";
        body.hidden = !body.hidden;
    };
}
