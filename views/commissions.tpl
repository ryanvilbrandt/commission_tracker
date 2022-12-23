% queue_name = "new_commissions"
% hidden = commissions[queue_name]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
    <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
    <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
    New commissions ({{ len(commissions[queue_name]["commissions"]) }})
    <span class="queue_hidden_label" queue_name="{{ queue_name }}_inverted"{{ "" if hidden else " hidden" }}>(hidden)</span>
</h2>
<% include(
    "commissions_div.tpl",
    commissions=commissions[queue_name]["commissions"],
    queue_type=queue_name,
    queue_name=queue_name,
    queue_open=True,
    current_user=current_user,
    users=users,
    hidden=hidden
) %>

% queue_name = "available_commissions"
% hidden = commissions[queue_name]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
    <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
    <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
    Available commissions ({{ len(commissions[queue_name]["commissions"]) }})
    <span class="queue_hidden_label" queue_name="{{ queue_name }}_inverted"{{ "" if hidden else " hidden" }}>(hidden)</span>
</h2>
<% include(
    "commissions_div.tpl",
    commissions=commissions[queue_name]["commissions"],
    queue_type=queue_name,
    queue_name=queue_name,
    queue_open=True,
    current_user=current_user,
    users=users,
    hidden=hidden
) %>

% for user, d in commissions["other_commissions"].items():
    <h2 class="commission_header user_commissions{{ " queue_hidden" if d["hidden"] else "" }}{{ " queue_closed" if not d["user"]["queue_open"] else "" }}" id="{{ user }}_commissions">
        <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ user }}" queue_name="{{ user }}" title="Click to hide this commission queue"{{ " hidden" if d["hidden"] else "" }}>
        <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ user }}" queue_name="{{ user }}_inverted" title="Click to show this commission queue"{{ " hidden" if not d["hidden"] else "" }}>
        {{ d["user"]["full_name"] }}'s commissions ({{ len(d["commissions"]) }})
        <span class="queue_hidden_label" queue_name="{{ user }}_inverted"{{ "" if d["hidden"] else " hidden" }}>(hidden)</span>
    </h2>
    <% include(
        "commissions_div.tpl",
        commissions=d["commissions"],
        queue_type="other_commissions",
        queue_name=user,
        queue_open=d["user"]["queue_open"],
        current_user=current_user,
        users=users,
        hidden=d["hidden"]
    ) %>
% end

% queue_name = "finished_commissions"
% hidden = commissions[queue_name]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
    <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
    <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
    Finished commissions ({{ len(commissions[queue_name]["commissions"]) }})
    <span class="queue_hidden_label" queue_name="{{ queue_name }}_inverted"{{ "" if hidden else " hidden" }}>(hidden)</span>
</h2>
<% include(
    "commissions_div.tpl",
    commissions=commissions[queue_name]["commissions"],
    queue_type=queue_name,
    queue_name=queue_name,
    queue_open=True,
    current_user=current_user,
    users=users,
    hidden=hidden
) %>

% queue_name = "removed_commissions"
% hidden = commissions[queue_name]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
    <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
    <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
    Removed commissions ({{ len(commissions[queue_name]["commissions"]) }})
    <span class="queue_hidden_label" queue_name="{{ queue_name }}_inverted"{{ "" if hidden else " hidden" }}>(hidden)</span>
</h2>
<% include(
    "commissions_div.tpl",
    commissions=commissions[queue_name]["commissions"],
    queue_type=queue_name,
    queue_name=queue_name,
    queue_open=True,
    current_user=current_user,
    users=users,
    hidden=hidden
) %>
