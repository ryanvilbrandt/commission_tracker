% if current_user["is_artist"] and not commissions["my_commissions"]:
    % hidden = commissions["available_commissions"]["hidden"]
    <h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="my_commissions">
        % checked = " checked" if not hidden else ""
        <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="my_commissions" title="Show/Hide Commissions"{{ checked }}>
        Commissions assigned to me{{ " (Why do you have any???)" if not current_user["is_artist"] else "" }}:
    </h2>
    <% include(
        "commissions_div.tpl",
        commissions=commissions["my_commissions"]["commissions"],
        queue_type="my_commissions",
        queue_name="my_commissions",
        current_user_role=current_user["role"],
        users=users,
        hidden=hidden
    ) %>
% end

% hidden = commissions["available_commissions"]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="available_commissions">
    % checked = " checked" if not hidden else ""
    <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="available_commissions" title="Show/Hide Commissions"{{ checked }}>
    Available commissions:
</h2>
<% include(
    "commissions_div.tpl",
    commissions=commissions["available_commissions"]["commissions"],
    queue_type="available_commissions",
    queue_name="available_commissions",
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

% hidden = commissions["finished_commissions"]["hidden"]
<h2 class="commission_header{{ " queue_hidden" if hidden else "" }}" id="finished_commissions">
    % checked = " checked" if not hidden else ""
    <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="finished_commissions" title="Show/Hide Commissions"{{ checked }}>
    Finished commissions:
</h2>
<% include(
    "commissions_div.tpl",
    commissions=commissions["finished_commissions"]["commissions"],
    queue_type="finished_commissions",
    queue_name="finished_commissions",
    current_user_role=current_user["role"],
    users=users,
    hidden=hidden
) %>
