% if current_user["is_artist"]:
    <h2 id="my_commissions">Commissions assigned to me:</h2>
    % include("commissions_div.tpl", commissions=commissions["my_commissions"], queue_name="my_commissions", current_user_role=current_user["role"], users=users)
% end

<h2 id="other_commissions">Available commissions:</h2>
% include("commissions_div.tpl", commissions=commissions["available_commissions"], queue_name="available_commissions", current_user_role=current_user["role"], users=users)

% for user, d in commissions["other_commissions"].items():
    % if current_user["full_name"] != user:
    <div id="{{ user }}_commissions" class="user_commissions">
        <h2>{{ d["full_name"] }}'s commissions:</h2>
    </div>
    <div class="commission_stats">
        <span class="user_meta_header accepted" title="Assigned">✋: {{ d["meta"]["assigned"] }}</span>&nbsp;&nbsp;&nbsp;
        <span class="user_meta_header invoiced" title="Emailed/Invoiced">📮: {{ d["meta"]["invoiced"] }}</span>&nbsp;&nbsp;&nbsp;
        <span class="user_meta_header paid" title="Paid">💸: {{ d["meta"]["paid"] }}</span>&nbsp;&nbsp;&nbsp;
        <span class="user_meta_header not_accepted" title="Not Yet Accepted">❌: {{ d["meta"]["not_accepted"] }}</span>
    </div>
    % include("commissions_div.tpl", commissions=d["commissions"], queue_name="other_commissions", current_user_role=current_user["role"], users=users)
    % end
% end

<h2 id="finished_commissions">Finished commissions:</h2>
% include("commissions_div.tpl", commissions=commissions["finished_commissions"], queue_name="finished_commissions", current_user_role=current_user["role"], users=users)
