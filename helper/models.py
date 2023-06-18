from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta,date


class Help(models.Model):
    HELP_TYPES = [
        ('U', 'Urgent'),
        ('H', 'High Priority'),
        ('N', 'Normal'),
    ]
    REQUEST_STATUSES = [
        ('S', 'Sent to All'),
        ('H', 'On Hold'),
        ('C', 'Complete'),
    ]
    EXPIRATION_PERIODS = {
        'U': 5,   # 5 days
        'H': 15,  # 15 days
        'N': 30,  # 30 days
    }
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_helps',default=None)
    help_type = models.CharField(max_length=1, choices=HELP_TYPES)
    status = models.CharField(max_length=2, choices=REQUEST_STATUSES)
    created_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField()
    deleted_by = models.ManyToManyField(User, related_name='deleted_helps')
    referred_to = models.ManyToManyField('self', through='Referral', symmetrical=False, blank=True)
    
    def __str__(self):
        return f"Help: {self.id}, Creator: {self.creator.username}"
    
    def is_expired(self):
        expiration_period = self.EXPIRATION_PERIODS.get(self.help_type, 0)
        if expiration_period:
            return (self.created_time.date() + timedelta(days=expiration_period)) <= date.today()
        return False

    def get_referral_pairs(self):
        referral_pairs = []
        referrals = self.referrals.order_by('created_time')
        
        for referral in referrals:
            referral_pairs.append((referral.referrer, referral.referred_to.creator))
        
        return referral_pairs
    

class Referral(models.Model):
    help = models.ForeignKey(Help, on_delete=models.CASCADE)
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_to = models.ForeignKey(Help, on_delete=models.CASCADE, related_name='referring_users')
    created_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Referrer: {self.referrer.username}, Referred To: {self.referred_to.creator.username}"
