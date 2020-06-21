from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Not to disclose')
)


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, gender=2, **extra_fields): # 제일 앞에 _가 있으면 이 클래스 내에서만 사용하겠다는 뜻이다. 없으면 클래스 밖에서도 사용
        """
        Create and Save a user with the given username, email, and password
        """        
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, '', password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True) # unique는 아이디 중복을 방지하기 위함

    username = models.CharField(max_length=30)

    gender = models.SmallIntegerField(choices=GENDER_CHOICES)

    objects = UserManager()
    USERNAME_FIELD = 'email' # 원래는 username으로 로그인하는데 지금은 email로 로그인 할꺼기 때문에 email을 씀
    REQUIRED_FIELDS = [] # 필수로 받고 싶은 필드들 넣기, 원래 소스 코드엔 email필드가 들어가지만 우리는 로그인을 이메일로 하니깐..

    def __str__(self):
        return "<%d> %s" %(self.pk, self.email)