% hidden_text = " hidden" if hidden else ""
% empty_queue_text = "None" if queue_open else "Queue closed"
% if not commissions:
<div class="commission_container" queue_name="{{ queue_name }}"{{ hidden_text }}><em>{{ empty_queue_text }}</em></div>
% else:
% for commission in commissions:
<div class="commission_buttons" queue_name="{{ queue_name }}"{{ hidden_text }}>
    % if queue_type != "new_commissions" and current_user["is_artist"]:
        % if queue_type == "my_commissions":
            <button class="reject action_button" title="Reject commission" commission_id="{{ commission['id'] }}">❌</button>
        % else:
            <button class="claim action_button" title="Claim commission" commission_id="{{ commission['id'] }}">✋</button>
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
    <p>
        <b>Status:</b> {{ commission["status_text"] }}<br>
        <a href="{{ commission["url"] }}" target="_blank">Link to commission details</a>
    </p>
    % if queue_type == "other_commissions" or queue_type == "my_commissions":
    <p hidden><input type="file" class="commission_upload" commission_id="{{ commission['id'] }}"></p>
    <div class="commission_upload_drag" commission_id="{{ commission['id'] }}">
        <div class="upload_prompt" commission_id="{{ commission['id'] }}">
            Select the finished commission image to upload<br>by
            <span class="commission_upload_click clickable" commission_id="{{ commission['id'] }}">clicking this link</span>
            or dragging the file here.
        </div>
        <img class="upload_preview" commission_id="{{ commission['id'] }}" hidden>
        <div class="upload_confirmation" commission_id="{{ commission['id'] }}" hidden>
            Is the above image file the one you want to upload?<br>You can
            <span class="commission_finish clickable" commission_id="{{ commission['id'] }}">upload it</span>
            and mark this commission as finished, or
            <span class="commission_upload_click clickable" commission_id="{{ commission['id'] }}">select a new file.</span>
        </div>
    </div>
    % elif queue_type == "finished_commissions":
    <p><a href="/get_finished_commission_image/{{ commission["uploaded_filename"] }}" target="_blank">Uploaded File</a></p>
    % end
    % if current_user["role"] != "user":
    <hr>
    <p>
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