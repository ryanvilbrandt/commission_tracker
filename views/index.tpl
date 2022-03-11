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
            <button class="change_user_username" title="Change Username" user_id="{{current_user['id']}}">🇺 Change Username</button>
            <button class="change_user_password" title="Change Password" user_id="{{current_user['id']}}">🔒 Change Password</button>
            % end
        </div>
    </div>

    <!-- <button id="refresh_button">🔄 Refresh commissions</button> -->

    <div id="commissions">
        % include("commissions.tpl", commissions=commissions)
    </div>

    % if current_user["role"] != "user":
    <br>
    <hr>
    <br>

    <button id="force_update_button">⬆️ Force update all users</button>

    <h2>Users:</h2>

    <table id="users-table" border="1">
      <tr>
        <th>ID</th>
        <th>Username</th>
        <th>Full Name</th>
        <th>Role</th>
        <th>Controls</th>
      </tr>
      % for user in users:
      <tr>
        <td class="user_id" user_id="{{user['id']}}">{{user["id"]}}</td>
        <td class="username" user_id="{{user['id']}}">{{user["username"]}}</td>
        <td class="full_name" user_id="{{user['id']}}">{{user["full_name"]}}</td>
        <td class="role" user_id="{{user['id']}}">{{user["role"].title()}}</td>
        <td>
          % if not user["disable_user_buttons"]:
          <button class="change_user_username" title="Change Username" user_id="{{user['id']}}">🇺</button>
          <button class="change_user_full_name" title="Change Full Name" user_id="{{user['id']}}">🇫</button>
          <button class="change_user_password" title="Change Password" user_id="{{user['id']}}">🔒</button>
          <button class="delete_user" title="Delete User" user_id="{{user['id']}}">❌</button>
          % end
        </td>
      </tr>
      % end
    </table>

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
      <input type="submit" value="Add New User">
    </form>
</div>
% end

<script type="module">
    import { init } from "/static/js/index.js";
    init();
</script>
