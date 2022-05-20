% hidden_text = " hidden" if hidden else ""
% empty_queue_text = "None" if queue_open else "Queue closed"
% if not commissions:
<div class="commission_container" queue_name="{{ queue_name }}"{{ hidden_text }}><em>{{ empty_queue_text }}</em></div>
% else:
% for commission in commissions:
<div class="commission_buttons" queue_name="{{ queue_name }}"{{ hidden_text }}>
    % if queue_type != "new_commissions":
        % if queue_type != "my_commissions" and current_user["is_artist"]:
            <button class="claim action_button" title="Claim commission" commission_id="{{ commission['id'] }}">✋</button>
        % end
        % if not queue_type == "finished_commissions":
            % if queue_type == "my_commissions":
                % if not commission["accepted"]:
                    <button class="accept action_button" title="Accept commission" commission_id="{{ commission['id'] }}">✅</button>
                % end
                <button class="reject action_button" title="Reject commission" commission_id="{{ commission['id'] }}">❌</button>
            % end
            % if queue_type == "other_commissions" and not commission["accepted"] and current_user["role"] != "user":
                <button class="accept action_button" title="Accept commission" commission_id="{{ commission['id'] }}">✅</button>
            % end
        % end
        % if queue_type == "my_commissions" or current_user["role"] != "user":
            % if not commission["invoiced"]:
                <button class="invoiced action_button" title="Mark as Emailed" commission_id="{{ commission['id'] }}">📮</button>
            % elif not commission["paid"]:
                <button class="paid action_button" title="Mark as Paid" commission_id="{{ commission['id'] }}">💸</button>
            % end
            % if not commission["finished"] and (queue_type == "my_commissions" or queue_type == "other_commissions"):
                <button class="finished_button action_button disabled_button" title="You must upload a file to this commission before marking it as Finished." commission_id="{{ commission['id'] }}" disabled>🎉</button>
            % end
        % end
    % end
</div>
% open = " open" if commission.get('open') else ""
% span_all = "_span_all" if queue_type == "new_commissions" else ""
<details class="commission_description{{ span_all }}" commission_id="{{ commission['id'] }}" queue_name="{{ queue_name }}"{{ open }}{{ hidden_text }}>
    % star = " ⭐" if commission["is_exclusive"] else ""
    <summary class="{{ commission['status'] }} commission_title_container">
        <span class="commission_title">#{{ commission['id'] }}: {{ commission["name"] }}{{ star }}</span>
        % if current_user["role"] != "user":
        <span class="created_updated">
            <span class="created_text" epoch="{{ commission['created_epoch'] }}"></span>&nbsp;&nbsp;&nbsp;
            <span class="updated_text" epoch="{{ commission['updated_epoch'] }}"></span>
        </span>
        % end
    </summary>
    <p><a href="{{ commission["url"] }}" target="_blank">Link to commission details</a></p>
    % if queue_type == "other_commissions" or queue_type == "my_commissions":
    <p hidden><input type="file" class="commission-upload" commission_id="{{ commission['id'] }}"></p>
    <div class="commission_upload_drag" commission_id="{{ commission['id'] }}">
        <img class="upload_preview" commission_id="{{ commission['id'] }}" hidden>
        <div>
            Upload the finished commission by
            <span class="commission_upload_click" commission_id="{{ commission['id'] }}">clicking</span>
            or dragging the file here.
        </div>
    </div>
    % elif queue_type == "finished_commissions":
    <p><a href="/get_finished_commission_image/{{ commission["uploaded_filename"] }}" target="_blank">Uploaded File</a></p>
    % end
    % if current_user["role"] != "user":
    <hr>
    <p>
        <b>Status:</b> {{ commission["status_text"] }}<br>
        <b>Assigned to:</b> {{ commission["full_name"] }}<br>
        <b>Email:</b> {{ commission['email'] }}
        % if commission["message"]:
        <br><b>Message:</b> {{ commission["message"] }}
        % end
    </p>
    <p>
        <label for="assign_users_dropdown_{{ commission['id'] }}">Assign to an artist:</label>
        <select name="assign_users" id="assign_users_dropdown_{{ commission['id'] }}">
        % if queue_type == "new_commissions":
            <option value="-1">Any Artist</option>
        % else:
            <option value="-1">Unassigned</option>
        % end
        % for user in users:
            % if user["is_artist"] and user["queue_open"]:
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