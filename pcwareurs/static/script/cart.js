
document.querySelector('.cart-btn').addEventListener('click', function() {
    document.querySelector('#cart').classList.toggle('cart-toggle');
});

document.querySelector('#close-cart-btn').addEventListener('click', function() {
    document.querySelector('#cart').classList.remove('cart-toggle');
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

            if (!document.querySelector('#cart').classList.contains("cart-toggle")) {
                document.querySelector('#cart').classList.toggle('cart-toggle');
            }
            
            document.querySelector('#cart-content').innerHTML = data.cart_html
        } else {
            // show an error message
            console.log(data)
        }
    });
}

function removeFromCart(productId) {
    let csrf_token = document.getElementById("csrf_token").value;

    return fetch('/cart/remove/', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token 
        },
        body: JSON.stringify({ 'product_id': productId })
    })
    .then(response => response.json())
    .then(data => {
        // handle the response from the server
        if (data.success) {
            console.log("success")
            
            if (!document.querySelector('#cart').classList.contains("cart-toggle")) {
                document.querySelector('#cart').classList.toggle('cart-toggle');
            }

            document.querySelector('#cart-content').innerHTML = data.cart_html
        } else {
            // show an error message
            console.log(data)
        }
    });
}


function updateCart(productId, quantity) {
    let csrf_token = document.getElementById("csrf_token").value;

    return fetch('/cart/update/', {
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
            
            if (!document.querySelector('#cart').classList.contains("cart-toggle")) {
                document.querySelector('#cart').classList.toggle('cart-toggle');
            }
            
            document.querySelector('#cart-content').innerHTML = data.cart_html
        } else {
            // show an error message
            console.log(data)
        }
    });
}