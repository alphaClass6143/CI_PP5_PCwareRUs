
document.querySelector('#cart-btn').addEventListener('click', function() {
    document.querySelector('#cart').classList.toggle('cart-toggle');
    console.log("Used")
});


function addToCart(productId, quantity) {
    let csrf_token = document.getElementById("csrf_token").value;

    return fetch('/cart/add/', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token 
        },
        body: JSON.stringify({ 'product_id': productId, 'quantity': quantity })
    })
    .then(response => response.json())
    .then(data => {
        // handle the response from the server
        if (data.success) {
            console.log("success")
            document.querySelector('#cart').classList.toggle('cart-toggle');
            document.querySelector('#cart').innerHTML = data.cart_html
        } else {
            // show an error message
            console.log(data)
        }
    });
}