class ProfileView():
    """user could see profile info"""
    def show_profile(self):
        pass

    def change_profile(self):
        pass

    def show_addresses(self):
        pass


class CustomerPanel():

    def show_history_orders(self):
        pass

    def show_current_orders(self):
        pass

    def show_recent_orders(self):
        pass


class ShoppingCart(LoginRequiredMixin):
    """add to cart and login for final order
    Single page using DRF"""
    pass


class order():
    def add_order(self):
        pass

    def add_discount_to_order(self):
        pass

    def show_order_items(self):
        """items, counts"""
        pass



class login_with_otp_code():
    """using Redis for otp and custome backend for second method"""