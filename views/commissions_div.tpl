% if not commissions:
<tr><td colspan="3"><em>None</em></td></tr>
% else:
% for commission in commissions:
<tr>
<td style="vertical-align: top;">
    % if queue_name != "my_commissions":
        <button class="claimed action_button" title="Claim commission" commission_id="{{ commission['id'] }}">✋</button>
    % end
    % if not queue_name == "finished_commissions":
        % if queue_name == "my_commissions":
            % if not commission["accepted"]:
                <button class="accepted action_button" title="Accept commission" commission_id="{{ commission['id'] }}">✅</button>
            % end
            <button class="rejected action_button" title="Reject commission" commission_id="{{ commission['id'] }}">❌</button>
        % end
        % if queue_name == "other_commissions" and not commission["accepted"] and current_user_role != "user":
            <button class="accepted action_button" title="Accept commission" commission_id="{{ commission['id'] }}">✅</button>
        % end
    % end
    % if queue_name == "my_commissions" or current_user_role != "user":
        % if not commission["invoiced"]:
            <button class="invoiced action_button" title="Mark as Emailed" commission_id="{{ commission['id'] }}">📮</button>
        % elif not commission["paid"]:
            <button class="paid action_button" title="Mark as Paid" commission_id="{{ commission['id'] }}">💸</button>
        % end
        % if not commission["finished"]:
            <button class="finished action_button" title="Mark as Finished" commission_id="{{ commission['id'] }}">🎉</button>
        % end
    % end
</td>
<td colspan="2">
    <details commission_id="{{ commission['id'] }}"{{ " open" if commission.get('open') else "" }}>
        % star = " ⭐" if not commission["allow_any_artist"] else ""
        <summary class="{{ commission['status'] }}">#{{ commission['id'] }}: {{ commission["name"] }}{{ star }} ({{ commission["status_text"] }})</summary>
        <p><b>Number of characters:</b> {{ commission["num_characters"] }}</p>
        <p><b>Description</b><br>{{ commission["description"] }}</p>
        <p><b>Reference images</b></p>
        <ul>
        % for image in commission["reference_images"]:
            <li><a href="{{ image }}">{{ image }}</a></li>
        % end
        </ul>
        <p><b>Expression</b><br>{{ commission["expression"] }}</p>
        % if commission["notes"]:
        <p><b>Additional notes</b><br>{{ commission["notes"] }}</p>
        % end
        <b>Assigned to:</b> {{ commission["full_name"] }}<br>
        <b>Artist choice:</b> {{ commission["artist_choice"] }}<br>
        % if commission["if_queue_is_full"]:
        <b>If queue is full:</b> {{ commission["if_queue_is_full"] }}<br>
        % end
        % if commission["twitch"]:
        <b>Twitch:</b> {{ commission["twitch"] }}<br>
        % end
        % if commission["twitter"]:
        <b>Twitter:</b> {{ commission["twitter"] }}<br>
        % end
        % if commission["discord"]:
        <b>Discord:</b> {{ commission["discord"] }}<br>
        % end
        <b>Email:</b> {{ commission['email'] }}
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
        <p>
            % disabled = " disabled" if not commission["invoiced"] else ""
            <button class="undo_invoiced_button" commission_id="{{ commission['id'] }}"{{ disabled }}>Undo "Mark as Emailed"</button>
            % disabled = " disabled" if not commission["paid"] else ""
            <button class="undo_paid_button" commission_id="{{ commission['id'] }}"{{ disabled }}>Undo "Mark as Paid"</button>
        </p>
        % end
    </details>
</td>
</tr>
% end
% end