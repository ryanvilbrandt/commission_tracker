% if not commissions:
    <p><em>None</em></p>
% else:
    % for commission in commissions:
    <details commission_id="{{ commission['id'] }}"{{ " open" if commission.get('open') else "" }}>
        <summary>{{ commission["name"] }}</summary>
        <p>{{ commission["description"] }}</p>
    </details>
    % end
% end