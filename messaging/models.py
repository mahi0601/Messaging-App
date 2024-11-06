from django.db import models
from django.contrib.auth.models import User
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')
    name = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    membership_tier = models.CharField(
        max_length=10,
        choices=[('standard', 'Standard'), ('premium', 'Premium'), ('VIP', 'VIP')],
        default='standard'
    )
    profile_link = models.URLField(null=True, blank=True)  # Optional external profile link

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)  # New field for account ID
    loan_status = models.CharField(max_length=50, null=True, blank=True)     # New field for loan status

    def __str__(self):
        return self.name

# class Message(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
#     content = models.TextField()
#     response = models.TextField(null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[('open', 'Open'), ('in progress', 'In Progress'), ('closed', 'Closed')], default='open')
#     urgency = models.BooleanField(default=False)

#     def __str__(self):
#         return f'Message from {self.customer.name} at {self.timestamp}'


class Message(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    URGENCY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='low')
    timestamp = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    response = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    urgency = models.BooleanField(default=False)

    def check_urgency(self):
        urgency_keywords = ["loan approval", "disbursement"]
        if any(keyword.lower() in self.content.lower() for keyword in urgency_keywords):
            self.urgency = True
            self.save()

    def save(self, *args, **kwargs):
        self.check_urgency()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.customer.name}: {self.content[:20]} - {self.get_urgency_display()}"
