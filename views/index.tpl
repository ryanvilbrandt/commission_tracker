% rebase("base.tpl", title=title)
<div class="collapsible">
  <div class="header">
    <span class="open-arrow">▼</span>
    <span class="name">{{username}}</span>
  </div>
  <div class="body" hidden>
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
    <td>{{user["id"]}}</td>
    <td>{{user["username"]}}</td>
    <td>{{user["full_name"]}}</td>
    <td>{{user["role"].title()}}</td>
    <td>
      <button class="change_user_username" title="Change Username" user_id="{{user['id']}}"{{disabled}}>🇦</button>
      <button class="change_user_password" title="Change Password" user_id="{{user['id']}}"{{disabled}}>🔒</button>
      <button class="delete_user" title="Delete User" user_id="{{user['id']}}"{{disabled}}>❌</button>
    </td>
  </tr>
  % end
</table>
