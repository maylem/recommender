let app = {};

app.model = (function() {
    'use strict';

    let $event_pump = $('body');

    return {
        'get_similar_users': function(user_handle) {
            let ajax_options = {
                type: 'GET',
                url: 'api/user_recommender/' + user_handle,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'user_handle': user_handle
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_get_similar_users_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

app.view = (function() {
    'use strict';

    let $user_handle = $('#user_handle');

    return {
        build_table: function(user_recommender) {
            let rows = ''

            $('.user_recommender table > tbody').empty(); // remove existing table elements

            if (user_recommender) {
                for (let i=0; i < user_recommender.length; i++) {
                    rows += `<tr><td class="user_handle">${user_recommender[i].user_handle}</td>
                    <td class="similarity">${user_recommender[i].similarity}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

app.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $user_handle = $('#user_handle');

    function validate(user_handle) {
        // restrict input to integer values only
        return !isNaN(user_handle) && !isNaN(Number(user_handle)) && Number(user_handle) % 1 == 0;
    }

    $('#get_similar_users').click(function(e) {
        let user_handle = $user_handle.val();

        e.preventDefault();

        if (validate(user_handle)) {
            model.get_similar_users(user_handle)
        } else {
            alert('Please enter an integer user handle');
        }

        e.preventDefault();
    });

    $event_pump.on('model_get_similar_users_success', function(e, data) {
        view.build_table(data);
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(app.model, app.view));


