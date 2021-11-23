function unfollowUser(user_email, csrf_token) {

    $(document).ready(function () {

        $.ajax({
            url: '/unfollow/' + user_email,
            type: 'POST',
            headers: {'X-CSRFToken': csrf_token},

            success: function (data) {
                let statusModal = $('#status_message_modal');
                $('#status_message_modal_title').text('Success');
                $('#status_message_modal_body').text(data.toString());
                statusModal.modal('show')
                statusModal.on('hidden.bs.modal', function () {
                    location.reload();
                })
            },

            error: function (data) {
                $('#status_message_modal_title').text('Error');
                $('#status_message_modal_body').text(data.responseText);
                $('#status_message_modal').modal('show')
            }

        });

    });

}

function redirect(url) {

    $(document).ready(function () {
        window.location.replace(url);
    });

}

function createPost() {

}