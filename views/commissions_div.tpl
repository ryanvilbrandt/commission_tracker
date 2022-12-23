% hidden_text = " hidden" if hidden else ""
% empty_queue_text = "None" if queue_open else "Queue closed"
% if not commissions:
<div class="commission_container" queue_name="{{ queue_name }}"{{ hidden_text }}><em>{{ empty_queue_text }}</em></div>
% else:
% for commission in commissions:
<div class="commission_buttons" queue_name="{{ queue_name }}"{{ hidden_text }}>
    % if queue_type == "new_commissions":
        <button class="reject action_button" title="Reject commission" commission_id="{{ commission['id'] }}">❌</button>
    % elif queue_type == "available_commissions":
        <button class="claim action_button" title="Claim commission" commission_id="{{ commission['id'] }}">✋</button>
    % elif queue_type == "finished_commissions":
        % if not commission["emailed"]:
        <button class="emailed action_button" title="Commission has been emailed to the commissioner" commission_id="{{ commission['id'] }}">📧</button>
        % end
    % elif queue_type == "removed_commissions":
        % if not commission["refunded"]:
        <button class="refunded action_button" title="Commission has been refunded through Ko-fi" commission_id="{{ commission['id'] }}">💸</button>
        % end
    % end
</div>
% open = " open" if commission.get('open') else ""
<details class="commission_description" commission_id="{{ commission['id'] }}" queue_name="{{ queue_name }}"{{ open }}{{ hidden_text }}>
    % star = " ⭐" if commission["is_exclusive"] else ""
    % commission_type = " ({})".format(commission["num_characters"]) if queue_type != "new_commissions" else ""
    % finished_by = " -- Commission by {}".format(commission["full_name"]) if queue_type == "finished_commissions" else ""
    <summary class="{{ commission['status'] }} commission_title_container">
        <span class="commission_title">#{{ commission['id'] }}: {{ commission["name"] }}{{ star }}{{ commission_type }}{{ finished_by }}</span>
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
    % if queue_type == "new_commissions":
    <p>What type of commission is this?</p>
    <p>
        <!--
        <input type="radio" id="option_1" name="num_characters" class="num_characters" value="Fri Doodle" commission_id="{{ commission['id'] }}">
        <label for="option_1">(Fri) 5-Minute Doodle</label><br>
        <input type="radio" id="option_2" name="num_characters" class="num_characters" value="Fri Sketch" commission_id="{{ commission['id'] }}">
        <label for="option_2">(Fri) Refined Sketch</label><br>
        -->
        <input type="radio" id="option_3" name="num_characters" class="num_characters" value="Sun Zesty Doodle" commission_id="{{ commission['id'] }}">
        <label for="option_3">(Sun) ~Zesty~ 5-Minute Doodle</label><br>
        <input type="radio" id="option_4" name="num_characters" class="num_characters" value="Sun Zesty Sketch" commission_id="{{ commission['id'] }}">
        <label for="option_4">(Sun) ~Zesty~ Refined Sketch</label><br>
    </p>
    <p class="assign_new_commission_error_text" commission_id="{{ commission['id'] }}" hidden>
        You must specify what type of commission this is.
    </p>
    <p><button class="approve" title="Approve commission" commission_id="{{ commission['id'] }}" new_commission="{{ queue_type == "new_commissions" }}">✔️ Approve</button></p>
    % elif queue_type == "other_commissions" or queue_type == "my_commissions":
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
        % if commission["uploaded_filename"]:
        <p><a href="/get_finished_commission_image/{{ commission["uploaded_filename"] }}" target="_blank">Previously uploaded file</a></p>
        % end
    % elif queue_type == "finished_commissions":
    <p><a href="/get_finished_commission_image/{{ commission["uploaded_filename"] }}" target="_blank">Uploaded file</a></p>
    % end
    % if commission["notes"]:
        <hr>
        <p><b>Notes:</b></p>
        % for note in commission["notes"]:
        <p>
            <span class="note_text">{{! note["text"] }}</span><br>
            <span class="notes_attribution">{{ note["full_name"] }} ({{ note["created_ts"] }})</span>
        </p>
        % end
    % end
    <p>
        <button class="add_note_button">Add Note</button>
    </p>
    <p hidden>
        <label for="note_text">Note:</label><br>
        <textarea class="submit_note_text" name="note_text" rows="4" cols="50"></textarea><br>
        <button class="submit_note_button" commission_id="{{ commission['id'] }}" user_id="{{ current_user['id'] }}">Submit</button>
    </p>
    % if current_user["role"] != "user":
        <hr>
        <p>
            <b>Assigned to:</b> {{ commission["full_name"] }}<br>
            % if commission["message"]:
            <br><b>Message:</b> {{ commission["message"] }}
            % end
        </p>
        % if not commission["refunded"]:
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
                <button class="assign_to_user_button" commission_id="{{ commission['id'] }}" new_commission="{{ queue_type == "new_commissions" }}">Assign</button>
            </p>
            % if queue_type != "removed_commissions":
            <p><button class="remove_commission_button" commission_id="{{ commission['id'] }}">🛑 Remove Commission</button></p>
            % end
        % end
    % end
</details>
% end
% end