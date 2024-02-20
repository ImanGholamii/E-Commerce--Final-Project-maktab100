function adjustQuantity(productId, quantityChange) {
    updateQuantity(productId, quantityChange);
    // var messageElement = document.getElementById("message");
    var message = quantityChange > 0 ? "+1" : "-1";
    var bubble = document.createElement("div");
    bubble.textContent = message;
    bubble.className = quantityChange > 0 ? "bubble green" : "bubble red";

    document.getElementById("bubble-container").appendChild(bubble);

    // Clear the message after 1.5 seconds
    setTimeout(function () {
        bubble.remove();
    }, 1500);
    // Set the message and color
    messageElement.innerText = message;
    messageElement.className = quantityChange > 0 ? "message green" : "message red";

    function updateQuantity(productId, quantityChange) {
        fetch('/en/api/orders/items/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product: productId,
                quantities: quantityChange
            })
        })
            .then(response => response.json())
            .then(data => {

                document.getElementById('quantity-' + productId).innerText = data.quantities;

            })
            .catch(error => console.error('Error:', error));
    }
}


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
