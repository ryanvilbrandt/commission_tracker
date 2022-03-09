% if not commissions:
<p><em>None</em></p>
% else:
<table>
    % for commission in commissions:
    <tr>
    <td style="vertical-align: top;">
        % if claimable:
        <button class="claim_button" title="Claim" commission_id="{{ commission['id'] }}">✋</button>
        % else:
        % if not commission["accepted"]:
        <button class="accept_button" title="Accept" commission_id="{{ commission['id'] }}">✅</button>
        % end
        <button class="reject_button" title="Reject" commission_id="{{ commission['id'] }}">❌</button>
        % end
        % if not commission["invoiced"]:
        <button class="invoiced_button" title="Invoiced" commission_id="{{ commission['id'] }}">📮</button>
        % elif not commission["paid"]:
        <button class="paid_button" title="Paid" commission_id="{{ commission['id'] }}">💸</button>
        % end
        % if not commission["finished"]:
        <button class="finished_button" title="Finished" commission_id="{{ commission['id'] }}">🎉</button>
        % end
    </td>
    <td>
        <details commission_id="{{ commission['id'] }}"{{ " open" if commission.get('open') else "" }}>
            <summary>{{ commission["name"] }} ({{ commission["assigned_string"] }})</summary>
            <ul>
                <li><b>Number of characters:</b> {{ commission["num_characters"] }}</li>
                <li><b>Artist choice:</b> {{ commission["artist_choice"] }}</li>
                % if commission["if_queue_is_full"]:
                <li><b>If queue is full:</b> {{ commission["if_queue_is_full"] }}</li>
                % end
                % if commission["twitch"]:
                <li><b>Twitch:</b> {{ commission["twitch"] }}</li>
                % end
                % if commission["twitter"]:
                <li><b>Twitter:</b> {{ commission["twitter"] }}</li>
                % end
                % if commission["discord"]:
                <li><b>Discord:</b> {{ commission["discord"] }}</li>
                % end
            </ul>
            <p><b>Description</b><br>{{ commission["description"] }}</p>
            <p><b>Reference images</b></p>
            <ul>
            % for image in commission["reference_images"]:
                <li><a href="{{ image }}">{{ image }}</a></li>
            % end
            </ul>
            <p><b>Expression</b><br>{{ commission["expression"] }}</p>
            % if commission["notes"]:
            <p><b>Additional notes</b><br>{{ commission["notes"] }}</p>
            % end
            <p><b>Invoice Notes:</b> {{ commission['email'] }} (#{{ commission['id'] }})</p>
        </details>
    </td>
    </tr>
    % end
</table>
% end