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

function adjustQuantity(productId, amount) {
    updateQuantity(productId, amount);
}


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
