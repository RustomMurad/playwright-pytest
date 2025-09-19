from playwright.sync_api import Playwright


class APIUtils:

    def get_token(self, playwright: Playwright, user_credentials):
        user_email = user_credentials['user_email']
        user_password = user_credentials['user_password']
        api_request_context=playwright.request.new_context(base_url='https://rahulshettyacademy.com')
        response = api_request_context.post(url='api/ecom/auth/login',
                                            headers={"Content-Type":"application/json"},
                                            data={"userEmail": user_email,"userPassword": user_password})
        assert response.ok
        response_body = response.json()
        return response_body['token']




    def create_order(self, playwright:Playwright,user_credentials):
        token = self.get_token(playwright, user_credentials)
        api_request_context=playwright.request.new_context(base_url='https://rahulshettyacademy.com/client')
        response = api_request_context.post(url='/api/ecom/order/create-order',
                                 headers={
                                     "Authorization": token,
                                     "Content-Type":"application/json"
                                 },
                                 data={"orders":[{"country":"India","productOrderedId":"68a961719320a140fe1ca57c"}]})
        response_body = response.json()
        order_id = response_body['orders'][0]
        return order_id
