from django.db import models
from django.shortcuts import resolve_url as r
# Create your models here.

class Speaker(models.Model):
    name = models.CharField('Nome',max_length=255)
    slug = models.SlugField('Slug')
    photo = models.URLField('Foto')
    website = models.URLField('Site', blank=True)
    description = models.TextField('Descrição', blank=True)

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('speaker_detail', slug=self.slug)

class Contact(models.Model):
    EMAIL = 'E'
    PHONE = 'P'

    KINDS = (
        (EMAIL, 'Email'),
        (PHONE, 'Telefone'),

    )

    speaker = models.ForeignKey('Speaker', on_delete=models.CASCADE, verbose_name='Palestrante')
    kind = models.CharField('Tipo', max_length=1, choices=KINDS)
    value = models.CharField('Valor', max_length=255)

    class Meta:
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'

    def __str__(self):
        return self.value

class Talk(models.Model):
    title = models.CharField('Titulo', max_length=200)
    start = models.TimeField('Inicio', blank=True, null=True)
    description = models.TextField('Descrição',blank=True)
    speakers = models.ManyToManyField('Speaker', verbose_name='Palestrantes', blank=True)

    class Meta:
        verbose_name = 'palestras'
        verbose_name_plural = 'palestras'

    def __str__(self):
        return self.title