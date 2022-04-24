% if current_user["is_artist"] and not commissions["my_commissions"]:
    <h2 class="commission_header" id="my_commissions">
        % checked = " checked" if not commissions["my_commissions"]["hidden"] else ""
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
        hidden=commissions["my_commissions"]["hidden"]
    ) %>
% end

<h2 class="commission_header" id="available_commissions">
    % checked = " checked" if not commissions["available_commissions"]["hidden"] else ""
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
    hidden=commissions["available_commissions"]["hidden"]
) %>

% for user, d in commissions["other_commissions"].items():
    % if current_user["full_name"] != user:
    <h2 class="commission_header" id="{{ user }}_commissions" class="user_commissions">
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
    % include("commissions_div.tpl", commissions=d["commissions"], queue_type="other_commissions", queue_name=user, current_user_role=current_user["role"], users=users, hidden=d["hidden"])
    % end
% end

<h2 class="commission_header" id="finished_commissions">
    % checked = " checked" if not commissions["finished_commissions"]["hidden"] else ""
    <input type="checkbox" class="show_hide_commissions_checkbox" queue_owner="finished_commissions" title="Show/Hide Commissions"{{ checked }}>
    Finished commissions:
</h2>
% include("commissions_div.tpl", commissions=commissions["finished_commissions"]["commissions"], queue_type="finished_commissions", queue_name="finished_commissions", current_user_role=current_user["role"], users=users, hidden=commissions["finished_commissions"]["hidden"])
