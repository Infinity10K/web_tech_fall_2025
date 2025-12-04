function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const likeButtons = document.querySelectorAll('button[data-question-id]');

for (const button of likeButtons) {
    button.addEventListener('click', (e) => {
        const counter = document.querySelector(`span[data-like-counter="${button.dataset.questionId}"]`)

        counter.innerHTML = (Number(counter.innerHTML) + 1).toString()

        const request = new Request(
            `question/${button.dataset.questionId}/like`,
            {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin' // Do not send CSRF token to another domain.
            }
        );
        fetch(request).then(function(response) {
            response.json().then((data) => {
                    console.log(data)

                    counter.innerHTML = data.likeCount
                }
            )

        });
        }
    )
}
