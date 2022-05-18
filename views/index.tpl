% rebase("base.tpl", title=title)
<div id="content">
    <div id="header">
        <h1>Stream Commission Tracker</h1>
        <div id="user-information">
            <h2>
                {{ current_user["full_name"] }}
                % if current_user["role"] != "user":
                ({{ current_user["role"].title() }})
                % end
            </h2>
            % if current_user["role"] != "god":
            <button class="change_user_button change_user_full_name" title="Change Full Name" user_id="{{current_user['id']}}">🇫 Change Full Name</button>
            <button class="change_user_button change_user_password" title="Change Password" user_id="{{current_user['id']}}">🔒 Change Password</button>
            % end
            % if current_user["is_artist"]:
            <input class="queue_open_checkbox" id="current_user_queue_open_checkbox" type="checkbox" user_id="{{current_user['id']}}"{{ " checked" if current_user["queue_open"] else "" }}> Queue Open?
            % end
        </div>
    </div>

    <!-- <button id="refresh_button">🔄 Refresh commissions</button> -->

    <br>
    <details>
        <summary>How To Use The Commission Tracker</summary>
        <p>This is a quick summary of how to user the Commission Tracker.<br>
            If this is your first time logging in here, please click the <code>🔒 Change Password</code> button above to change your password.<br>
            You can also change your displayed name by clicking the <code>🇫 Change Full Name</code> button.</p>
        % if current_user["role"] != "user":
        {{ !host_quick_guide }}
        % else:
        {{ !user_quick_guide }}
        % end
    </details>

    <div id="commissions">
        % include("commissions.tpl", commissions=commissions, current_user=current_user, users=users)
    </div>

    % if current_user["role"] != "user":
    <br>
    <hr>
    <br>

    <button id="force_update_button">⬆️ Force update all users</button>

    <h2>Users:</h2>

    <div id="users">
        % include("users.tpl", users=users)
    </div>

    <div id="add_new_user_section">
        <h3>Add new user</h3>

        <form action="/add_new_user" method="POST">
            <label for="add_new_user_username">Username:</label><br>
            <input type="text" id="add_new_user_username" name="username" required><br>
            <label for="add_new_user_full_name">Full name:</label><br>
            <input type="text" id="add_new_user_full_name" name="full_name"><br>
            <label for="add_new_user_password">Password:</label><br>
            <input type="text" id="add_new_user_password" name="password" required><br>
            <p>
                Role<br>
                <input type="radio" id="add_new_user_admin" name="role" value="admin" required>
                <label for="add_new_user_admin">Admin</label><br>
                <input type="radio" id="add_new_user_user" name="role" value="user" required>
                <label for="add_new_user_user">User</label><br>
            </p>
            <label for="add_new_user_is_artist">Is an artist?</label>
            <input type="checkbox" id="add_new_user_is_artist" name="is_artist" checked><br>
            <label for="add_new_user_queue_open">Queue open?</label>
            <input type="checkbox" id="add_new_user_queue_open" name="queue_open" checked><br>
            <br>
            <input type="submit" value="Add New User">
        </form>
    </div>
</div>
% end

<div id="websocket_error_overlay" hidden></div>

<div id="top_error_overlay"></div>

<script type="module">
    import { init } from "/static/js/index.js";
    init("{{ current_user["role"] }}", "{{ current_user["is_artist"] }}");
</script>
