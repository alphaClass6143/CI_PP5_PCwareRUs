const stripePublic = JSON.parse(document.getElementById('stripePublic').textContent);
const clientSecret = JSON.parse(document.getElementById('clientSecret').textContent);

var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
event.preventDefault();
stripe.createToken(cardElement).then(function(result) {
if (result.error) {
  // Handle errors
} else {
  // Send the token to your server
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', result.token.id);
  form.appendChild(hiddenInput);
  form.submit();
}
});
});

// This is your test publishable API key.
const stripe = Stripe(stripePublic);

let elements;

initialize();
checkStatus();

document.querySelector("#payment-form").addEventListener("submit", handleSubmit);

var emailAddress = '';
// Fetches a payment intent and captures the client secret
async function initialize() {

    const appearance = {
            theme: 'stripe',
        };
        elements = stripe.elements({ appearance, clientSecret });


    const paymentElementOptions = {
        layout: "tabs",
    };

    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.mount("#payment-element");

}

async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
        receipt_email: emailAddress,
        return_url: returnUrl
        },
    });


    if (error.type === "card_error" || error.type === "validation_error") {
        showMessage(error.message);
    } else {
        console.log(error.message)
        showMessage("An unexpected error occurred.");
    }

    setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
const clientSecret = new URLSearchParams(window.location.search).get(
"payment_intent_client_secret"
);

if (!clientSecret) {
return;
}

const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

switch (paymentIntent.status) {
    case "succeeded":
    showMessage("Payment succeeded!");
    break;
    case "processing":
    showMessage("Your payment is processing.");
    break;
    case "requires_payment_method":
    showMessage("Your payment was not successful, please try again.");
    break;
    default:
    showMessage("Something went wrong.");
    break;
    }
}

// ------- UI helpers -------

function showMessage(messageText) {
const messageContainer = document.querySelector("#payment-message");

messageContainer.classList.remove("hidden");
messageContainer.textContent = messageText;

    setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageText.textContent = "";
    }, 4000);
}

// Show a spinner on payment submission
    function setLoading(isLoading) {
    if (isLoading) {
        // Disable the button and show a spinner
        document.querySelector("#submit").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("#submit").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
}