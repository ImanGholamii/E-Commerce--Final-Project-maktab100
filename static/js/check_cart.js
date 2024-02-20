function adjustQuantity(productId, amount) {
    var messageElement = document.getElementById("message");
    var message = amount > 0 ? "+1" : "-1";

    // Set the message and color
    messageElement.innerText = message;
    messageElement.className = amount > 0 ? "message green" : "message red";

    updateQuantity(productId, amount);
    // AJAX request to update the quantity
    fetch('/en/api/orders/items/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            product: productId,
            quantities: amount
        })
    })
    .then(response => response.json())
    .then(data => {
        // Clear the message after 2 seconds
        setTimeout(function() {
            messageElement.innerText = "";
            messageElement.className = "message"; // Reset the color
        }, 2000);
    })
    .catch(error => console.error('Error:', error));
}



function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
