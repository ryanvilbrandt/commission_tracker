% if current_user["is_artist"]:
    % queue_name = "my_commissions"
    % hidden = commissions[queue_name]["hidden"]
    <h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
        % checked = " checked" if not hidden else ""
        <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="{{ queue_name }}" title="Show/Hide Commissions"{{ checked }}>
        Commissions assigned to me{{ " (Why do you have any???)" if not current_user["is_artist"] else "" }}:
    </h2>
    <% include(
        "commissions_div.tpl",
        commissions=commissions[queue_name]["commissions"],
        queue_type=queue_name,
        queue_name=queue_name,
        current_user_role=current_user["role"],
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
        New commissions (needs assignment):
    </h2>
    <% include(
        "commissions_div.tpl",
        commissions=commissions[queue_name]["commissions"],
        queue_type=queue_name,
        queue_name=queue_name,
        current_user_role=current_user["role"],
        users=users,
        hidden=hidden
    ) %>
% end

% queue_name = "available_commissions"
% hidden = commissions[queue_name]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="{{ queue_name }}">
    % checked = " checked" if not hidden else ""
    <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="{{ queue_name }}" title="Show/Hide Commissions"{{ checked }}>
    Available commissions:
</h2>
<% include(
    "commissions_div.tpl",
    commissions=commissions[queue_name]["commissions"],
    queue_type=queue_name,
    queue_name=queue_name,
    current_user_role=current_user["role"],
    users=users,
    hidden=hidden
) %>

% for user, d in commissions["other_commissions"].items():
    % if current_user["full_name"] != user:
    <h2 class="commission_header user_commissions{{ " queue_hidden" if d["hidden"] else "" }}" id="{{ user }}_commissions">
        % checked = " checked" if not d["hidden"] else ""
        <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="{{ user }}" title="Show/Hide Commissions"{{ checked }}>
        {{ d["full_name"] }}'s commissions:
    </h2>
    <div class="commission_stats">
        <span class="user_meta_header accepted" title="Assigned">✋: {{ d["meta"]["assigned"] }}</span>&nbsp;&nbsp;&nbsp;
        <span class="user_meta_header invoiced" title="Emailed/Invoiced">📮: {{ d["meta"]["invoiced"] }}</span>&nbsp;&nbsp;&nbsp;
        <span class="user_meta_header paid" title="Paid">💸: {{ d["meta"]["paid"] }}</span>&nbsp;&nbsp;&nbsp;
        <span class="user_meta_header not_accepted" title="Not Yet Accepted">❌: {{ d["meta"]["not_accepted"] }}</span>
    </div>
    <% include(
        "commissions_div.tpl",
        commissions=d["commissions"],
        queue_type="other_commissions",
        queue_name=user,
        current_user_role=current_user["role"],
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
    Finished commissions:
</h2>
<% include(
    "commissions_div.tpl",
    commissions=commissions[queue_name]["commissions"],
    queue_type=queue_name,
    queue_name=queue_name,
    current_user_role=current_user["role"],
    users=users,
    hidden=hidden
) %>
