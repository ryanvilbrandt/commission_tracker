% if not commissions:
    <p><em>None</em></p>
% else:
    % for commission in commissions:
    <details class="details-animated" commission_id="{{ commission['id'] }}">
        <summary>{{ commission["name"] }}</summary>
        <p>{{ commission["description"] }}</p>
    </details>
    % end
% end