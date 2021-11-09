from django.db import models
from django.urls import reverse

# Create your models here.
class Trainer(models.Model):
    Name= models.CharField(max_length=120)
    Surname = models.CharField(max_length=120)
    City = models.CharField(max_length=120)
    # Basinda 0 olmadan girilecek
    Phone = models.CharField(max_length=10)
    Mail = models.EmailField(max_length=120)
    gender_dict = [
        (True, 'Erkek'),
        (False, 'Kadın')
    ]
    Gender = models.BooleanField(blank=False, null=False, choices=gender_dict)
    Address = models.TextField()
    Work_Experience = models.TextField()
    image = models.FileField(null=True,blank=True)
    Birth_Date = models.DateField()
    approval_dict = [
        (True, 'Onaylı'),
        (False, 'Onaylanmamış')
    ]
    is_approved = models.BooleanField(default=False, verbose_name = 'Onay', choices=approval_dict)
    User_ID = models.ForeignKey('auth.User', related_name='trainers', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Kullanıcı Hesabı')

    def __str__(self):
        return self.Name + ' ' + self.Surname

    def get_absolute_url(self):
        return reverse('trainer:detail', kwargs={'id': self.id})

class Comment(models.Model):
    trainer = models.ForeignKey('trainer.Trainer', related_name='comments', on_delete=models.CASCADE, verbose_name='Gönderi')
    name = models.CharField(max_length=200, verbose_name='Başlık')
    content = models.TextField(verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
