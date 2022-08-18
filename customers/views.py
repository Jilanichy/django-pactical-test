from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from customers.models import SubscriptionInfo
from customers.serializers import UserSerializer, SubscriptionInfoSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from customers.permissions import IsSubscriberOrReadOnly


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
    Using Generic Class-Based Views the below two views are trim down into super concise
    and DRY principled way.
    We can see the exact two views are also defined below, commented out, using Function-Based Views
'''
class SubscriptionList(generics.ListCreateAPIView):
    queryset = SubscriptionInfo.objects.all()
    serializer_class = SubscriptionInfoSerializer

    '''
        'IsAuthenticatedOrReadOnly' ensures that authenticated requests get read-write access, 
        and unauthenticated requests get read-only access.
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # overriding .perform_create() method to represent individual admin instance
    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionInfo.objects.all()
    serializer_class = SubscriptionInfoSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, 
                            IsSubscriberOrReadOnly]


'''
	below two function views are exact same as upper two class based views
'''

# @api_view(['GET', 'POST'])
# def subscription_list(request, format=None):
#     """
#     List all subscriptions, or create a new subscription.
#     """
#     if request.method == 'GET':
#         subscriptions = SubscriptionInfo.objects.all()
#         serializer = SubscriptionInfoSerializer(subscriptions, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SubscriptionInfoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def subscription_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a subscription
#     """
#     try:
#         subscriber = SubscriptionInfo.objects.get(pk=pk)
#     except SubscriptionInfo.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SubscriptionInfoSerializer(subscriber)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SubscriptionInfoSerializer(subscriber, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         subscriber.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




'''
- Placeholder code on Stripe payment integration with customers
- create_checkout_session view which will do AJAX request to the server to generate a new Checkout Session ID
- stripe_webhook will create a new StripeCustomer every time customer subscribe to a service/plan
'''
# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)


# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = 'http://localhost:8000/'
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 client_reference_id=request.user.id if request.user.is_authenticated else None,
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancel/',
#                 payment_method_types=['card'],
#                 mode='subscription',
#                 line_items=[
#                     {
#                         'price': settings.STRIPE_PRICE_ID,
#                         'quantity': 1,
#                     }
#                 ]
#             )
#             return JsonResponse({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})


# @csrf_exempt
# def stripe_webhook(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)

#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']

#         # Fetch all the required data from session
#         client_reference_id = session.get('client_reference_id')
#         stripe_customer_id = session.get('customer')
#         stripe_subscription_id = session.get('subscription')

#         # Get the user and create a new StripeCustomer
#         user = User.objects.get(id=client_reference_id)
#         StripeCustomer.objects.create(
#             user=user,
#             stripeCustomerId=stripe_customer_id,
#             stripeSubscriptionId=stripe_subscription_id,
#         )
#         print(user.username + ' just subscribed.')

#     return HttpResponse(status=200)


# @login_required
# def home(request):
#     try:
#         # Retrieve the subscription & product
#         stripe_customer = StripeCustomer.objects.get(user=request.user)
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
#         product = stripe.Product.retrieve(subscription.plan.product)
#         return render(request, 'home.html', {
#             'subscription': subscription,
#             'product': product,
#         })
#     except StripeCustomer.DoesNotExist:
#         return render(request, 'home.html')