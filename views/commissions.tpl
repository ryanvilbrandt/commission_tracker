<table>
    <tr><th colspan="2">Commissions assigned to me:</th></tr>
    % include("commissions_div.tpl", commissions=commissions["my_commissions"], queue_name="my_commissions", current_user_role=current_user["role"])

    <tr><th colspan="2">Available commissions:</th></tr>
    % include("commissions_div.tpl", commissions=commissions["available_commissions"], queue_name="available_commissions", current_user_role=current_user["role"])

    <tr><th colspan="2">Commissions assigned to others:</th></tr>
    % include("commissions_div.tpl", commissions=commissions["other_commissions"], queue_name="other_commissions", current_user_role=current_user["role"])

    <tr><th colspan="2">Finished commissions:</th></tr>
    % include("commissions_div.tpl", commissions=commissions["finished_commissions"], queue_name="finished_commissions", current_user_role=current_user["role"])
</table>