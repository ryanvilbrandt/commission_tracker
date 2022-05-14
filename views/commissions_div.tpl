% hidden_text = " hidden" if hidden else ""
<div class="commission_container queue_hidden" queue_name="{{ queue_name }}_inverted"{{ " hidden" if not hidden else "" }}><em>Hidden</em></div>
% if not commissions:
<div class="commission_container" queue_name="{{ queue_name }}"{{ hidden_text }}><em>None</em></div>
% else:
% for commission in commissions:
<div class="commission_buttons" queue_name="{{ queue_name }}"{{ hidden_text }}>
    % if queue_type != "new_commissions":
        % if queue_type != "my_commissions" and current_user_role == "user":
            <button class="claim action_button" title="Claim commission" commission_id="{{ commission['id'] }}">✋</button>
        % end
        % if not queue_type == "finished_commissions":
            % if queue_type == "my_commissions":
                % if not commission["accepted"]:
                    <button class="accept action_button" title="Accept commission" commission_id="{{ commission['id'] }}">✅</button>
                % end
                <button class="reject action_button" title="Reject commission" commission_id="{{ commission['id'] }}">❌</button>
            % end
            % if queue_type == "other_commissions" and not commission["accepted"] and current_user_role != "user":
                <button class="accept action_button" title="Accept commission" commission_id="{{ commission['id'] }}">✅</button>
            % end
        % end
        % if queue_type == "my_commissions" or current_user_role != "user":
            % if not commission["invoiced"]:
                <button class="invoiced action_button" title="Mark as Emailed" commission_id="{{ commission['id'] }}">📮</button>
            % elif not commission["paid"]:
                <button class="paid action_button" title="Mark as Paid" commission_id="{{ commission['id'] }}">💸</button>
            % end
            % if not commission["finished"]:
                <button class="finished action_button" title="Mark as Finished" commission_id="{{ commission['id'] }}">🎉</button>
            % end
        % end
    % end
</div>
% open = " open" if commission.get('open') else ""
<details class="commission_description" commission_id="{{ commission['id'] }}" queue_name="{{ queue_name }}"{{ open }}{{ hidden_text }}>
    % star = " ⭐" if commission["is_exclusive"] else ""
    <summary class="{{ commission['status'] }}">#{{ commission['id'] }}: {{ commission["name"] }}{{ star }}</summary>
    <p>
        <b>Email:</b> {{ commission['email'] }}<br>
        <b>Status:</b> {{ commission["status_text"] }}<br>
        <b>Assigned to:</b> {{ commission["full_name"] }}
    </p>
    <p><b>Link to commission details:</b> <a href="{{ commission["url"] }}" target="_blank">{{ commission["url"] }}</a></p>
    % if commission["message"]:
    <p><b>Message:</b> {{ commission["message"] }}</p>
    % end
    % if current_user_role != "user":
    <hr>
    <p>
        <label for="assign_users_dropdown_{{ commission['id'] }}">Assign to a user:</label>
        <select name="assign_users" id="assign_users_dropdown_{{ commission['id'] }}">
            <option value="-1">Unassigned</option>
        % for user in users:
            % if user["role"] == "user":
            <option value="{{ user["id"] }}">{{ user["full_name"] }}</option>
            % end
        % end
        </select>
        <button class="assign_to_user_button" commission_id="{{ commission['id'] }}">Assign</button>
    </p>
    % end
</details>
% end
% end