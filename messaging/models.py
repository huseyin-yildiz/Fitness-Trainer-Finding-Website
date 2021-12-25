from django.db import models

class Message(models.Model):
    sender = models.ForeignKey('auth.User', related_name='sender', on_delete=models.CASCADE, verbose_name='Sender')
    receiver = models.ForeignKey('auth.User', related_name='receiver', on_delete=models.CASCADE, verbose_name='Sender')
    message_text = models.CharField(max_length=250)
    is_read = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Message'
