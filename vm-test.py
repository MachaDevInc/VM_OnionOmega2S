import time
import stripe

stripe.api_key = "sk_test_51LsZEHJ6Ax4x6yLvtMJTxB5HW6tf4lisGowXk25wzjN0O0JidTjJOUbhNguUFTmQOZxbqWIs5oLIMRmKfHJuG0ae00dtcwgMev"

reader_id = "tmr_FBlQSgkrqMCGX5"

my_currency = "gbp"
my_payment_method_types = ["card_present"]
my_capture_method = "manual"

# create and process payment intent
payment_intent_create_response = stripe.PaymentIntent.create(
    amount=105,
    currency=my_currency,
    payment_method_types=my_payment_method_types,
    capture_method=my_capture_method,
)
print("payment intent id: " + payment_intent_create_response.id)

payment_intent_retrieve_response = stripe.PaymentIntent.retrieve(
    payment_intent_create_response.id)
print("payment intent status: " + payment_intent_retrieve_response.status)

reader_process_payment_intent_response = stripe.terminal.Reader.process_payment_intent(
    reader_id,
    payment_intent=payment_intent_create_response.id
)
print("reader status: " + reader_process_payment_intent_response.status)

print("reader payment process status: " + reader_process_payment_intent_response.action.status)

#stripe.terminal.Reader.TestHelpers.present_payment_method(reader_id,)

time.sleep(20)

payment_intent_retrieve_response = stripe.PaymentIntent.retrieve(
    payment_intent_create_response.id)
print("payment intent status: " + payment_intent_retrieve_response.status)

reader_status = stripe.terminal.Reader.retrieve(reader_id)
print("reader payment process status: " + reader_status.action.status)

if (payment_intent_retrieve_response.status == "requires_payment_method"):
    # wait for the client to process payment
    print("payment is not proceeded yet by client")

elif (payment_intent_retrieve_response.status == "requires_capture"):
    payment_intent_capture_response = stripe.PaymentIntent.capture(
        payment_intent_create_response.id)
    print("payment intent status: " +
        payment_intent_capture_response.status)
    if (payment_intent_capture_response.status == "succeeded"):
        print("payment done successfully")
        #break
    #break
#break
#break
# enjoy in while loop
