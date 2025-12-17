from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        verbose_name='닉네임'
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        verbose_name='프로필 이미지'
    )

    def get_profile_image_url(self):
        """프로필 이미지 URL 반환, 없으면 None"""
        if self.profile_image:
            return self.profile_image.url
        return None
    
    def get_display_initial(self):
        """프로필 이미지가 없을 때 표시할 이니셜(이름 첫 글자)"""
        if self.first_name:
            return self.first_name[0].upper()
        if self.nickname:
            return self.nickname[0].upper()
        return self.username[0].upper()