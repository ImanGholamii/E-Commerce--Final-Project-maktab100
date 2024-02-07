// Function to get CSRF token from cookies
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

// Check if csrftoken is not already defined before declaring it
if (!window.csrftoken) {
    window.csrftoken = getCookie('csrftoken');
}

// Function to update user order
function updateUserOrder(productId, action) {
    console.log('Product ID:', productId);
    console.log('Action:', action);
    console.log('User is Logged in, sending data...')

    var url = '/update_item/';
    // Send data to url, define what kind of data shall send to the backend
    console.log('csrftoken:', window.csrftoken)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': window.csrftoken, // Use window.csrftoken here
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data: ', data);
        location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Event listener for update buttons
var updateButtons = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function() {
        var productId = this.dataset.product; // Set product id
        var action = this.dataset.action;
        console.log('productId: ', productId, 'action: ', action);

        console.log('USER: ', user); // Make sure 'user' is defined
        if (user === 'AnonymousUser') {
            console.log('Not Logged in!');
        } else {
            updateUserOrder(productId, action); // Call the updateUserOrder function
        }
    });
}
