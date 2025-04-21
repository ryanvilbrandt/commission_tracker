<%def name="render(queue_name, queue_type, title, queue_open, hidden, commissions)">

<%
hidden_text = " hidden" if hidden else ""
not_hidden_text = "" if hidden else " hidden"
empty_queue_text = "None" if queue_open else "Queue closed"
%>
<!--<div id="debug">-->
<!--    <div>${queue_name}</div>-->
<!--    <div>${queue_type}</div>-->
<!--    <div>${title}</div>-->
<!--    <div>${queue_open}</div>-->
<!--    <div>${hidden}</div>-->
<!--    <div>${current_user}</div>-->
<!--</div>-->
<h2 class="commission_header${" queue_hidden" if hidden else ""}${" queue_closed" if not queue_open else ""}" id="${queue_name}">
    <img class="show_hide_icon" src="/static/img/eye-solid.svg" queue_owner="${queue_name}" queue_name="${queue_name}" title="Click to hide this commission queue"${hidden_text}>
    <img class="show_hide_icon hide" src="/static/img/eye-slash-solid.svg" queue_owner="${queue_name}" queue_name="${queue_name}_inverted" title="Click to show this commission queue"${not_hidden_text}>
    ${title} (${len(commissions)})
    <span class="queue_hidden_label" queue_name="${queue_name}_inverted"${not_hidden_text}>(hidden)</span>
</h2>

% if not commissions:
<div class="commission_container" queue_name="${queue_name}"${hidden_text}><em>${empty_queue_text}</em></div>
% else:
% for commission in commissions:
<div class="commission_buttons" queue_name="${queue_name}"${hidden_text}>
    % if queue_type != "new_commissions" and current_user["is_artist"]:
        % if queue_type == "my_commissions":
            <button class="reject action_button" title="Reject commission" commission_id="${commission['id']}">❌</button>
        % elif not commission["is_exclusive"]:
            <button class="claim action_button" title="Claim commission" commission_id="${commission['id']}">✋</button>
        % endif
    % elif queue_type == "finished_commissions" and not current_user["is_artist"]:
        % if not commission["emailed"]:
        <button class="emailed action_button" title="Commission has been emailed to the commissioner" commission_id="${commission['id']}">📧</button>
        % endif
    % elif queue_type == "removed_commissions" and not current_user["is_artist"]:
        % if not commission["refunded"]:
        <button class="refunded action_button" title="Commission has been refunded through Ko-fi" commission_id="${commission['id']}">💸</button>
        % endif
    % endif
</div>
<%
open = " open" if commission.get('open') else ""
span_all = "_span_all" if queue_type == "new_commissions" else ""
exclusive = " exclusive" if queue_open else ""
%>
<details class="commission_description${span_all}" commission_id="${commission['id']}" queue_name="${queue_name}"${open}${hidden_text}>
    <%
    star = ' <span id="exclusive-star" title="Indicates an exclusive commission, where the client has paid for a particular artist">⭐</span>' if commission["is_exclusive"] else ""
    finished_by = " -- Commission by {}".format(commission["full_name"]) if queue_type == "finished_commissions" else ""
    %>
    <summary class="${commission['status']} commission_title_container">
        <span class="commission_title"><b>#${commission['id']}:</b>&nbsp;&nbsp;&nbsp;&nbsp;${commission["name"]}${star}${finished_by}</span>
        % if current_user["role"] != "user":
        <span class="created_updated">
            <span class="created_text" epoch="${commission['created_epoch']}"></span>&nbsp;&nbsp;&nbsp;
            <span class="updated_text" epoch="${commission['updated_epoch']}"></span>
        </span>
        % endif
    </summary>
    <p>
        <b>Status:</b> ${commission["status_text"]}<br>
        <a href="${commission["url"]}" target="_blank">Link to commission details</a>
    </p>
    % if queue_type == "other_commissions" or queue_type == "my_commissions":
    <p hidden><input type="file" class="commission_upload" commission_id="${commission['id']}"></p>
    <div class="commission_upload_drag" commission_id="${commission['id']}">
        <div class="upload_prompt" commission_id="${commission['id']}">
            Upload the finished commission image by clicking the "Upload Commission" button or dragging the file here.
        </div>
        <div class="commission_upload_buttons" commission_id="${commission['id']}">
            <button class="commission_upload_button" commission_id="${commission['id']}">Upload Commission</button>
        </div>
        <img class="upload_preview" commission_id="${commission['id']}" hidden>
        <div class="upload_confirmation" commission_id="${commission['id']}" hidden>
            Is the above image file the one you want to upload?
        </div>
        <div class="commission_reupload_buttons" commission_id="${commission['id']}" hidden>
            <button class="commission_finish_button" commission_id="${commission['id']}">Confirm and Submit</button>
            <button class="commission_reupload_button" commission_id="${commission['id']}">Upload New File</button>
        </div>
    </div>
        % if commission["uploaded_filename"]:
        <p><a href="/get_finished_commission_image/${commission['uploaded_filename']}" target="_blank">Previously uploaded file</a></p>
        % endif
    % elif queue_type == "finished_commissions":
    <p><a href="/get_finished_commission_image/${commission['uploaded_filename']}" target="_blank">Uploaded file</a></p>
    % endif
    % if commission["notes"]:
        <hr>
        <p><b>Notes:</b></p>
        % for note in commission["notes"]:
        <p>
            <span class="note_text">${note["text"]}</span><br>
            <span class="notes_attribution">${note["full_name"]} (${note["created_ts"]})</span>
        </p>
        % endfor
    % endif
    <p>
        <button class="add_note_button">Add Note</button>
    </p>
    <p hidden>
        <label for="note_text">Note:</label><br>
        <textarea class="submit_note_text" name="note_text" rows="4" cols="50"></textarea><br>
        <button class="submit_note_button" commission_id="${commission['id']}" user_id="${current_user['id']}">Submit</button>
    </p>
    % if current_user["role"] != "user":
        <hr>
        <p>
            <b>Assigned to:</b> ${commission["full_name"]}<br>
            % if commission["message"]:
            <br><b>Message:</b> ${commission["message"]}
            % endif
        </p>
        % if queue_type == "new_commissions":
        <p hidden>How many characters is this commission asking for?</p>
        <p hidden>
            <input type="radio" id="new_comm_1_character" name="num_characters" class="num_characters" value="1 char" commission_id="${commission['id']}">
            <label for="new_comm_1_character">1 character</label><br>
            <input type="radio" id="new_comm_2_characters" name="num_characters" class="num_characters" value="2 char" commission_id="${commission['id']}">
            <label for="new_comm_2_characters">2 characters</label><br>
        </p>
        <p class="assign_new_commission_error_text" commission_id="${commission['id']}" hidden>You must specify if this commission requests either 1 or 2 characters.</p>
        % endif
        % if not commission["refunded"]:
            <p>
                <label for="assign_users_dropdown_${commission['id']}">Assign to an artist:</label>
                <select name="assign_users" id="assign_users_dropdown_${commission['id']}">
                % if queue_type == "new_commissions":
                    <option value="-1">Any Artist</option>
                % else:
                    <option value="-1">Unassigned</option>
                % endif
                % for user in users:
                    % if user["is_artist"] and user["queue_open"]:
                    <option value="${user["id"]}">${user["full_name"]}</option>
                    % endif
                % endfor
                </select>
                <button class="assign_to_user_button" commission_id="${commission['id']}" new_commission="${queue_type == "new_commissions"}">Assign</button>
            </p>
            % if queue_type != "removed_commissions":
            <p><button class="remove_commission_button" commission_id="${commission['id']}">🛑 Remove Commission</button></p>
            % endif
        % endif
    % endif
</details>
% endfor
% endif

</%def>