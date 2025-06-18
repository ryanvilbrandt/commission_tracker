    <table id="users-table" border="1">
      <tr>
        <th>ID</th>
        <th>Username</th>
        <th>Full Name</th>
        <th>Role</th>
        <th>Artist?</th>
        <th>Queue?</th>
        <th>Controls</th>
      </tr>
      % for user in users:
      <tr>
        <td>${user["id"]}</td>
        <td>${user["username"]}</td>
        <td>${user["full_name"]}</td>
        <td>${user["role"].title()}</td>
        <td><input class="admin_checkbox is_artist_checkbox" type="checkbox" user_id="${user['id']}" ${ "checked" if user["is_artist"] else "" }></td>
        <td><input class="admin_checkbox queue_open_checkbox" type="checkbox" user_id="${user['id']}" ${ "checked" if user["queue_open"] else "" }></td>
        <td>
          % if not user["disable_user_buttons"]:
          <button class="change_user_username" title="Change Username" user_id="${user['id']}">🇺</button>
          <button class="change_user_full_name" title="Change Full Name" user_id="${user['id']}">🇫</button>
          <button class="change_user_password" title="Change Password" user_id="${user['id']}">🔒</button>
          % if user["is_active"] == '1':
          <button class="delete_user" title="Delete User" user_id="${user['id']}">❌</button>
          % else:
          <button class="undelete_user" title="Undelete User" user_id="${user['id']}">➕</button>
          % endif
          % endif
        </td>
      </tr>
      % endfor
    </table>