<%namespace name="comm_div" file="commissions_div.tpl" />

% if current_user["is_artist"]:
    <% queue_name = "my_commissions" %>
    ${comm_div.render(
        queue_name,
        queue_name,
        "Commissions assigned to me",
        current_user["queue_open"],
        commissions[queue_name]["hidden"],
        commissions[queue_name]["commissions"],
    )}
% endif

% if not current_user["is_artist"]:
    <% queue_name = "new_commissions" %>
    ${comm_div.render(
        queue_name,
        queue_name,
        "New commissions (needs assignment)",
        True,
        commissions[queue_name]["hidden"],
        commissions[queue_name]["commissions"],
    )}
% endif

<% queue_name = "available_commissions" %>
${comm_div.render(
    queue_name,
    queue_name,
    "Available commissions",
    True,
    commissions[queue_name]["hidden"],
    commissions[queue_name]["commissions"],
)}

% for user, d in commissions["other_commissions"].items():
    % if current_user["username"] != user:
    ${comm_div.render(
        user,
        "other_commissions",
        f"{d['user']['full_name']}'s commissions",
        d["user"]["queue_open"],
        d["hidden"],
        commissions[queue_name]["commissions"],
    )}
    % endif
% endfor

<% queue_name = "finished_commissions" %>
${comm_div.render(
    queue_name,
    queue_name,
    "Finished commissions",
    True,
    commissions[queue_name]["hidden"],
    commissions[queue_name]["commissions"],
)}

% if not current_user["is_artist"]:
    <% queue_name = "removed_commissions" %>
    ${comm_div.render(
        queue_name,
        queue_name,
        "Removed commissions",
        True,
        commissions[queue_name]["hidden"],
        commissions[queue_name]["commissions"],
    )}
% endif
