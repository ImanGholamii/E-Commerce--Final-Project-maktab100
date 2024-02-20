function adjustQuantity(productId, quantityChange) {
    updateQuantity(productId, quantityChange);
    var messageElement = document.getElementById("message");
    var message = quantityChange > 0 ? "+1" : "-1";
    // Clear the message after 1.5 seconds
                setTimeout(function () {
                    messageElement.innerText = "";
                    messageElement.className = "message"; // Reset the color
                }, 1450);

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
