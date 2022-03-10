<h2>Commissions assigned to me:</h2>
% include("commissions_div.tpl", commissions=commissions["my_commissions"], claimable=False)

<h2>Available commissions:</h2>
% include("commissions_div.tpl", commissions=commissions["available_commissions"], claimable=True)

<h2>Commissions assigned to others:</h2>
% include("commissions_div.tpl", commissions=commissions["other_commissions"], claimable=True)

<h2>Finished commissions:</h2>
% include("commissions_div.tpl", commissions=commissions["finished_commissions"], claimable=False)