from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password




class User(AbstractUser):
    birthday = models.DateField(null=True)
    image = models.ImageField(null=True)
    point = models.PositiveIntegerField(default=0)
    following = models.ManyToManyField('self',symmetrical=False, related_name="followers", blank=True)
    email = models.EmailField(unique=True)
        # 비밀번호 필드 추가
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        # 비밀번호를 해싱하여 저장
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # 저장된 비밀번호와 사용자가 제공한 비밀번호 일치 확인
        return check_password(raw_password, self.password)
