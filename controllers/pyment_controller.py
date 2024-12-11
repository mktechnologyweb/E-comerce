from models.payment import Payment

class PymentController:
    #Save payment
    def save_payment(self, payment_id,order_id, card_number, card_name, expiry_date, cvv, amount, payment_status,user_id):
        Payment.save_payment(payment_id,order_id, card_number, card_name, expiry_date, cvv, amount, payment_status,user_id)

    #Update payment information
    def update_payment(self,payment_id, order_id, card_number, card_name, expiry_date, cvv):
        Payment.update_payment(payment_id,order_id, card_number, card_name, expiry_date, cvv)
    

    #Show payment

    def list_payments():
        payments = Payment.list_pyment()
     
 
        if isinstance(payments, list):
        # Se for uma lista, retorna os dados estruturados
           return [{"card_number": payment["card_number"], 
                 "card_name": payment["card_name"], 
                 "payment_id": payment["payment_id"], 
                 "order_id": payment["order_id"], 
                 "cvv": payment["cvv"], 
                 "expiry_date": payment["expiry_date"]} for payment in payments]
        else:
        # Se não for uma lista, retorna uma lista vazia (ou lida com o erro conforme necessário)
         return []

    #Show payment by id
    def list_pyment_id(user_id):
         pyments= Payment.list_pyment_id(user_id)
         return [{"payment_id": ad["payment_id"], "card_number": ad["card_number"], 
                "card_name": ad["card_name"], "expiry_date": ad["expiry_date"],
                 "cvv": ad["cvv"], "user_pyment_id ": ad["user_pyment_id"]} for ad in pyments]     

   