from django.db import models
import uuid

# Create your models here.

class Subscription(models.Model):
    hashid = models.UUIDField('hashID', default=uuid.uuid4, editable=False)
    name = models.CharField('Nome',max_length=100)
    cpf = models.CharField('CPF',max_length=11)
    email = models.EmailField('E-mail')
    phone = models.CharField('Telefone', max_length=20)
    created_at = models.DateTimeField('Criado Em',auto_now_add=True)
    paid = models.BooleanField('Pago',default=False)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscricao'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name