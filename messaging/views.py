# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Message
# from django.db.models import Q 
# # In views.py
# from django.shortcuts import render
# from .models import Agent, Customer, Message  # Ensure Agent is imported
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# import json

# from django.http import JsonResponse

# def ws_messages(request):
#     # Sample response; modify as per your actual requirement
#     return JsonResponse({"status": "success", "message": "WebSocket or simulated HTTP response"})
# CANNED_RESPONSES = [
#     "Thank you for reaching out. We will get back to you shortly.",
#     "We are currently processing your request. Please be patient.",
#     "Please update your app to the latest version to resolve this issue.",
# ]
# # views.py

# from django.shortcuts import redirect, get_object_or_404
# from .models import Agent, Message

# def claim_message(request, message_id):
#     message = get_object_or_404(Message, id=message_id)
    
#     if message.status == 'new':  # Only allow claiming if the message is unclaimed
#         message.agent = request.user.agent  # Assuming each agent has a user account
#         message.status = 'in_progress'
#         message.save()
    
#     return redirect('message_list')

# def send_message_form(request):
#     return render(request, 'messaging/send_message_form.html')
# def assign_message_to_agent(message):
#     # Filter for available agents
#     available_agents = Agent.objects.filter(available=True)
#     if available_agents.exists():
#         # Assign to the first available agent
#         agent = available_agents.first()
#         message.agent = agent
#         message.status = 'in progress'
#         message.save()
        
#         # Mark agent as unavailable for other assignments
#         agent.available = False
#         agent.save()

# def message_list(request):
#     # Filter messages: show "new" messages or those assigned to the current agent
#     if request.user.is_authenticated:
#         # Filter messages by status or agent if the user is logged in
#         messages = Message.objects.filter(
#             Q(status='new') | Q(agent=request.user.agent)
#         )
#     else:
#         # For anonymous users, only show new messages or other suitable content
#         messages = Message.objects.filter(status='new')
#     # messages = Message.objects.filter(
#     #     (Q(status='new') | Q(agent=request.user.agent))  # Assuming `request.user.agent` is available
#     # ).order_by('-urgency', '-timestamp')

#     # # Assign unassigned messages to available agents
#     # unassigned_messages = Message.objects.filter(agent__isnull=True, status='new')
#     # for message in unassigned_messages:
#     #     assign_message_to_agent(message)

#     # query = request.GET.get('q', '')
#     # if query:
#     #     messages = messages.filter(
#     #         Q(content__icontains=query) | Q(customer__name__icontains=query)
#     #     ).order_by('-urgency', '-timestamp')

#     # return render(request, 'messaging/message_list.html', {'messages': messages, 'query': query})
#     messages = Message.objects.all()
#     print(messages) 
#     return render(request, 'messaging/message_list.html', {'messages': messages})
# # In views.py
# def respond_to_message(request, message_id):
#     message = get_object_or_404(Message, id=message_id)
#     if request.method == 'POST':
#         response = request.POST.get('response')
#         message.response = response
#         message.status = 'closed'
#         message.save()
        
#         # Free up the agent
#         if message.agent:
#             message.agent.available = True
#             message.agent.save()
        
#         return redirect('message_list')
#     return render(request, 'messaging/respond.html', {'message': message, 'canned_responses': CANNED_RESPONSES})


# @csrf_exempt
# def send_message(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         customer_name = data.get('customer_name')
#         message_content = data.get('content')
        
#         # Create or get the customer
#         customer, created = Customer.objects.get_or_create(name=customer_name)
        
#         # Create the message
#         message = Message.objects.create(customer=customer, content=message_content)
        
#         return JsonResponse({'status': 'Message sent successfully'}, status=201)
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# def get_messages(request):
#     messages = Message.objects.all().values('id', 'customer__name', 'content', 'timestamp', 'status', 'urgency')
#     return JsonResponse(list(messages), safe=False)
# # views.py


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Agent, Customer, Message
import json

# Define canned responses for reuse
CANNED_RESPONSES = [
    "Thank you for reaching out. We will get back to you shortly.",
    "We are currently processing your request. Please be patient.",
    "Please update your app to the latest version to resolve this issue.",
]

@login_required
def ws_messages(request):
    # Sample response; modify as per your actual requirement
    return JsonResponse({"status": "success", "message": "WebSocket or simulated HTTP response"})

@login_required
def claim_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Allow claiming only if the message is new
    if message.status == 'new':
        message.agent = request.user.agent  # Assumes each agent has a user account
        message.status = 'in_progress'
        message.save()
    
    return redirect('message_list')

@login_required
def send_message_form(request):
    return render(request, 'messaging/send_message_form.html')

def assign_message_to_agent(message):
    # Find an available agent and assign them to the message
    available_agents = Agent.objects.filter(available=True)
    if available_agents.exists():
        agent = available_agents.first()
        message.agent = agent
        message.status = 'in_progress'
        message.save()
        
        # Mark agent as unavailable for other assignments
        agent.available = False
        agent.save()

@login_required
def message_list(request):
    # Check if the user is authenticated and has an associated agent
    if request.user.is_authenticated and hasattr(request.user, 'agent'):
        # Filter messages based on the user's agent if the agent exists
        messages = Message.objects.filter(
            Q(status='new') | Q(agent=request.user.agent)
        ).order_by('-urgency', '-timestamp')
    else:
        # If no agent exists for the user, just filter for new messages
        messages = Message.objects.filter(status='new').order_by('-urgency', '-timestamp')
    messages = messages.order_by('-urgency', '-timestamp')
    query = request.GET.get('q', '')
    if query:
        # Apply search filter if a query is provided
        messages = Message.objects.filter(
            Q(content__icontains=query) | Q(customer__name__icontains=query) | Q(customer__phone__icontains=query)
        )
    else:
        messages = Message.objects.all()

 
    # messages = Message.objects.all()
    return render(request, 'messaging/message_list.html', {'messages': messages, 'query': query})
# def message_list(request):
#     # Only authenticated users can see messages
#     if request.user.is_authenticated:
#         # Filter to show new messages or those assigned to the current agent
#         messages = Message.objects.filter(
#             Q(status='new') | Q(agent=request.user.agent)
#         ).order_by('-urgency', '-timestamp')
#     else:
#         messages = Message.objects.none()  # Anonymous users should see no messages

#     query = request.GET.get('q', '')
#     if query:
#         # Apply search filter if a query is provided
#         messages = messages.filter(
#             Q(content__icontains=query) | Q(customer__name__icontains=query)
#         )

#     # Render the message list template with the filtered messages
#     return render(request, 'messaging/message_list.html', {'messages': messages, 'query': query})

def respond_to_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    customer = message.customer 
    if request.method == 'POST':
        response = request.POST.get('response')
        print("Response received:", response)  
        message.response = response
        message.status = 'closed'
        message.save()
        
        # Free up the agent once the message is closed
        if message.agent:
            message.agent.available = True
            message.agent.save()
        print("Message saved successfully.")
        return redirect('message_list')


    return render(request, 'messaging/respond.html', {'message': message,'customer': customer,  'canned_responses': CANNED_RESPONSES,'confirmation': 'Response saved successfully!'})


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_name = data.get('customer_name')
        message_content = data.get('content')
        
        # Create or retrieve the customer
        customer, created = Customer.objects.get_or_create(name=customer_name)
        
        # Create a new message linked to the customer
        message = Message.objects.create(customer=customer, content=message_content)
        
        return JsonResponse({'status': 'Message sent successfully'}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def get_messages(request):
    # Retrieve messages and serialize them for JSON response
    messages = Message.objects.values('id', 'customer__name', 'content', 'timestamp', 'status', 'urgency')
    return JsonResponse(list(messages), safe=False)
