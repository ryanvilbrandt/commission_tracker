% rebase("base.tpl", title=title)
<div class="collapsible">
  <div class="header" commission_id="1">
    <span class="open-arrow">▼</span>
    <span class="name">Test Commission</span>
  </div>
  <div class="body" commission_id="1" hidden>
    <p>I'm some text.</p>
    <p>I'm some more text.</p>
    <p>I'm even more text.</p>
  </div>
</div>

<br>

<table id="users-table" border="1">
  <tr>
    <th>ID</th>
    <th>Username</th>
    <th>Full Name</th>
    <th>Role</th>
    <th>Controls</th>
  </tr>
  % for user in users:
  %     disabled = " disabled" if user["disable_user_buttons"] else ""
  <tr>
    <td class="user_id" user_id="{{user['id']}}">{{user["id"]}}</td>
    <td class="username" user_id="{{user['id']}}">{{user["username"]}}</td>
    <td class="full_name" user_id="{{user['id']}}">{{user["full_name"]}}</td>
    <td class="role" user_id="{{user['id']}}">{{user["role"].title()}}</td>
    <td>
      <button class="change_user_username" title="Change Username" user_id="{{user['id']}}"{{disabled}}>🇺</button>
      <button class="change_user_full_name" title="Change Full Name" user_id="{{user['id']}}"{{disabled}}>🇫</button>
      <button class="change_user_password" title="Change Password" user_id="{{user['id']}}"{{disabled}}>🔒</button>
      <button class="delete_user" title="Delete User" user_id="{{user['id']}}"{{disabled}}>❌</button>
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

<script type="module">
    import { init } from "/static/js/index.js";
    init();
</script>
