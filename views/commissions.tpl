<table>
    <tr><th colspan="2">Commissions assigned to me:</th></tr>
    % include("commissions_div.tpl", commissions=commissions["my_commissions"], claimable=False)

    <tr><th colspan="2">Available commissions:</th></tr>
    % include("commissions_div.tpl", commissions=commissions["available_commissions"], claimable=True)

    <tr><th colspan="2">Commissions assigned to others:</th></tr>
    % include("commissions_div.tpl", commissions=commissions["other_commissions"], claimable=True)

    <tr><th colspan="2">Finished commissions:</th></tr>
    % include("commissions_div.tpl", commissions=commissions["finished_commissions"], claimable=False)
</table>