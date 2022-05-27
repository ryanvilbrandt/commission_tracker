% if current_user["is_artist"]:
    % queue_name = "my_commissions"
    % hidden = commissions[queue_name]["hidden"]
    % queue_open = current_user["queue_open"]
    <h2 class="commission_header{{ " queue_hidden" if hidden else "" }}{{ " queue_closed" if not queue_open else "" }}" id="{{ queue_name }}">
        <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
        <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
        Commissions assigned to me{{ " (Why do you have any???)" if not current_user["is_artist"] else "" }}
        <span class="queue_hidden_label" queue_name="{{ queue_name }}_inverted"{{ "" if hidden else " hidden" }}>(hidden)</span>
    </h2>
    <% include(
        "commissions_div.tpl",
        commissions=commissions[queue_name]["commissions"],
        queue_type=queue_name,
        queue_name=queue_name,
        queue_open=queue_open,
        current_user=current_user,
        users=users,
        hidden=hidden
    ) %>
% end

% if not current_user["is_artist"]:
    % queue_name = "new_commissions"
    % hidden = commissions[queue_name]["hidden"]
    <h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
        <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
        <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
        New commissions (needs assignment)
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
% end

% queue_name = "available_commissions"
% hidden = commissions[queue_name]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
    <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
    <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
    Available commissions
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
    % if current_user["username"] != user:
    <h2 class="commission_header user_commissions{{ " queue_hidden" if d["hidden"] else "" }}{{ " queue_closed" if not d["user"]["queue_open"] else "" }}" id="{{ user }}_commissions">
        <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ user }}" queue_name="{{ user }}" title="Click to hide this commission queue"{{ " hidden" if d["hidden"] else "" }}>
        <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ user }}" queue_name="{{ user }}_inverted" title="Click to show this commission queue"{{ " hidden" if not d["hidden"] else "" }}>
        {{ d["user"]["full_name"] }}'s commissions
        <span class="queue_hidden_label" queue_name="{{ user }}_inverted"{{ "" if d["hidden"] else " hidden" }}>(hidden)</span>
    </h2>
    <div class="commission_stats">
        % if not current_user["is_artist"]:
        <span class="user_meta_header accepted" title="Assigned">✋: {{ d["meta"]["assigned"] }}</span>
        % end
    </div>
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
% end

% queue_name = "finished_commissions"
% hidden = commissions[queue_name]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
    <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
    <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
    Finished commissions
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

% if not current_user["is_artist"]:
    % queue_name = "removed_commissions"
    % hidden = commissions[queue_name]["hidden"]
    <h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
        <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}" title="Click to hide this commission queue"{{ " hidden" if hidden else "" }}>
        <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="{{ queue_name }}" queue_name="{{ queue_name }}_inverted" title="Click to show this commission queue"{{ " hidden" if not hidden else "" }}>
        Removed commissions
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
% end
