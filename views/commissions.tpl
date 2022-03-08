<h2>Commissions assigned to me:</h2>
% include("commissions_div.tpl", commissions=commissions["my_commissions"])

<h2>Available commissions:</h2>
% include("commissions_div.tpl", commissions=commissions["available_commissions"])

<h2>Commissions assigned to others:</h2>
% include("commissions_div.tpl", commissions=commissions["other_commissions"])