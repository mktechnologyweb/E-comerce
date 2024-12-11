from models.address import Address


class AddressController:
     #Save address   
     def save_adress(self,user_id, address_id, street, number, neighborhood, complement, city, state, zip_code):
        Address.save_or_update_address(user_id, address_id, street, number, neighborhood,complement,city,state,zip_code)
     #show address
     def list_address():
        address = Address.list_address()
        return [{"address_id": address["address_id"], "user_id": address["user_id"],"street": address["street"],"number": address["number"],"neighborhood": address["neighborhood"],"complement": address["complement"],"city": address["city"],"state": address["state"],"zip_code": address["zip_code"]} for address in address]
     #show logged in user address
     def get_address_id(user_id):
         address = Address.get_address_id(user_id)
         return [{"address_id": ad["address_id"], "user_id": ad["user_id"]} for ad in address]