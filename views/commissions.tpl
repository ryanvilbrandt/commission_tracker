% if current_user["is_artist"]:
    % queue_name = "my_commissions"
    % hidden = commissions[queue_name]["hidden"]
    % queue_open = current_user["queue_open"]
    <h2 class="commission_header{{ " queue_hidden" if hidden else "" }}{{ " queue_closed" if not queue_open else "" }}" id="{{ queue_name }}">
        % checked = " checked" if not hidden else ""
        <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="{{ queue_name }}" title="Show/Hide Commissions"{{ checked }}>
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
        % checked = " checked" if not hidden else ""
        <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="{{ queue_name }}" title="Show/Hide Commissions"{{ checked }}>
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
    % checked = " checked" if not hidden else ""
    <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="{{ queue_name }}" title="Show/Hide Commissions"{{ checked }}>
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
        % checked = " checked" if not d["hidden"] else ""
        <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="{{ user }}" title="Show/Hide Commissions"{{ checked }}>
        {{ d["user"]["full_name"] }}'s commissions
        <span class="queue_hidden_label" queue_name="{{ user }}_inverted"{{ "" if d["hidden"] else " hidden" }}>(hidden)</span>
    </h2>
    <div class="commission_stats">
        % if current_user["role"] != "user":
        <span class="user_meta_header accepted" title="Assigned">✋: {{ d["meta"]["assigned"] }}</span>&nbsp;&nbsp;&nbsp;
        <!-- <span class="user_meta_header invoiced" title="Emailed/Invoiced">📮: {{ d["meta"]["invoiced"] }}</span>&nbsp;&nbsp;&nbsp; -->
        <!-- <span class="user_meta_header paid" title="Paid">💸: {{ d["meta"]["paid"] }}</span>&nbsp;&nbsp;&nbsp; -->
        <span class="user_meta_header not_accepted" title="Not Yet Accepted">❌: {{ d["meta"]["not_accepted"] }}</span>
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
    % checked = " checked" if not hidden else ""
    <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="{{ queue_name }}" title="Show/Hide Commissions"{{ checked }}>
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
