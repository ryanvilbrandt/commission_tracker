    <table id="users-table" border="1">
      <tr>
        <th>ID</th>
        <th>Username</th>
        <th>Full Name</th>
        <th>Role</th>
        <th>Artist?</th>
        <th>Controls</th>
        <th># of commissions assigned</th>
      </tr>
      % for user in users:
      <tr>
        <td>{{user["id"]}}</td>
        <td>{{user["username"]}}</td>
        <td>{{user["full_name"]}}</td>
        <td>{{user["role"].title()}}</td>
        <td><input class="is_artist_checkbox" type="checkbox" user_id="{{user['id']}}" {{ "checked" if user["is_artist"] else "" }}></td>
        <td>
          % if not user["disable_user_buttons"]:
          <button class="change_user_username" title="Change Username" user_id="{{user['id']}}">🇺</button>
          <button class="change_user_full_name" title="Change Full Name" user_id="{{user['id']}}">🇫</button>
          <button class="change_user_password" title="Change Password" user_id="{{user['id']}}">🔒</button>
          <button class="delete_user" title="Delete User" user_id="{{user['id']}}">❌</button>
          % end
        </td>
        <td>{{user["commission_count"]}}</td>
      </tr>
      % end
    </table>