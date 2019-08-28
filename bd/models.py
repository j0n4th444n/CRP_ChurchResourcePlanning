# -*-coding: UTF-8-*- #

from __future__ import unicode_literals

from django.core import validators

from django.db import models


# ----------Validators----------
def PhoneValidator(value):
    a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ' ']
    if not Include(value, a):
        raise validators.ValidationError('Solo puede contener números, guiones(-), o espacios')


def DNIValidator(value):
    a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if not Include(value, a):
        raise validators.ValidationError('Solo puede contener números')


def OnlyLettersValidators(value):
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z', ' ',
         'ñ', 'á', 'é', 'í', 'ó', 'ú', 'Ñ']

    if not Include(value, a):
        raise validators.ValidationError('Solo puede contener letras')

# ----------Others----------
def Include(value, a):
    found = False
    for i in value:
        for j in a:
            if i == j:
                found = True
                break
        if not found:
            return False
        found = False

    return True

def changeSpaces(value):
    s = ''
    start = 0
    end = len(value) - 1
    #remove spaces and - at the beginning and end
    while start < len(value) and (value[start] == ' ' or value[start] == '-'):
        start += 1

    while(value[end] == ' ' or value[end] == '-') and end >= 0:
        end -= 1

    while start <= end:
        if(value[start] == ' ' or value[start] == '-'):
            s += '-'

        while start <= end and (value[start] == ' ' or value[start]== '-'):
                start += 1

        s += value[start]
        start += 1

    return s

def capitalizeFirstLetterOfEachWord(value):
    s = []
    found = False
    i = 0
    while i < len(value):
        a = ''
        while i < len(value) and value[i] != ' ' :
            a += value[i]
            found = True
            i += 1

        if found:
            s.append(a)
            found = False

        i += 1

    result = ''
    for i in  range(0,len(s)-1):
        result += s[i].capitalize() + ' '

    result += s[len(s)-1].capitalize()
    return result
# ----------Others----------

# ----------Validators----------
TYPE_CHOICES = (
    ('pending', 'Pendiente'),
    ('approved', 'Aprobado'),
    ('denied', 'Denegado')
)

EDUCATIONAL_LEVEL_CHOICES=(
    ('inferior', 'Inferior'),
    ('primario','Primario'),
    ('secundario','Secundario'),
    ('preuniversitario','Preuniversitario'),
    ('universitario','Universitario'),
    ('master','Master'),
    ('doctor','Doctor')
)

class Song(models.Model):
    name = models.CharField('nombre', max_length=25)
    lyric = models.TextField('letra')
    mp3 = models.BinaryField('mp3', null=True, blank=True)
    video = models.FileField(upload_to='videosTutoriales',verbose_name='videotutoriales',null=True)
    author = models.CharField('autor', max_length=25, blank=True)
    status = models.CharField('estado', default='', max_length=32, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Canción'
        verbose_name_plural = 'Canciones'


class Praise(models.Model):
    date = models.DateField('fecha')
    Songs = models.ManyToManyField(Song, blank=True, verbose_name='Canciones')

    def __str__(self):
        return (str)(self.date)

    #TODO: hacer que funciones \n
    def get_songs(self):
        return ',\n'.join([p.name for p in self.Songs.order_by('name').all()])
    get_songs.short_description = 'Canciones'

    class Meta:
        verbose_name = 'Alabanza'


class Instrument(models.Model):
    name = models.CharField('nombre', max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Instrumento'


class Designation(models.Model):
    name = models.CharField('nombre', max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Denominación'
        verbose_name_plural = 'Denominaciones'


class Cell(models.Model):
    address = models.CharField('dirección', max_length=124)
    directing = models.ForeignKey('Member', null=True, related_name='directing', verbose_name='dirigente')
    host = models.ForeignKey('Member', null=True, related_name='host', verbose_name='anfitrión')
    #church = models.ForeignKey(Church, null=True, verbose_name='Iglesia')
    members = models.ManyToManyField('Member', blank=True, verbose_name='miembro')

    def __str__(self):
        return self.address

    #TODO: poner en la pagina de detalles
    def get_members(self):
        return ',\n'.join([p.name for p in self.members.order_by('name').all()])
    get_members.short_description = 'Participantes'

    class Meta:
        verbose_name = 'Célula'


class Member(models.Model):
    TYPE_CHOICES = (
        ('femmale', 'Femenino'),
        ('male', 'Masculino')
    )

    dni = models.CharField('número de identidad', max_length=11, primary_key=True
                           , validators=[validators.MinLengthValidator(11, 'El número debe tener 11 dígitos'),
                                         validators.MaxLengthValidator(11, 'El número debe tener 11 dígitos'),
                                         DNIValidator])

    name = models.CharField('nombre', max_length=65, validators=[OnlyLettersValidators])
    gender = models.CharField('género', max_length=32, choices=TYPE_CHOICES)
    address = models.CharField('direción', max_length=128)
    phone = models.CharField('teléfono', max_length=32, blank=True,
                             validators=[PhoneValidator])
    occupation = models.CharField('ocupación', max_length=65, blank=True)
    level = models.CharField('nivel educacional', max_length=65, choices=EDUCATIONAL_LEVEL_CHOICES)
    praises = models.ManyToManyField(Praise, through='member_praises', verbose_name='alabanzas en que participa')

    def __str__(self):  # agregarle el dni
        return self.name + ' ' + self.dni

    #TODO:poner en la pagina de detalles con un mostrar u ocultar
    def get_praises(self):
        return  ',\n'.join([(str)(p.date) for p in self.praises.order_by('date').all()])
    get_praises.short_description = 'Alabanzas Participadas'

    class Meta:
        verbose_name = 'Miembro'

    def save(self, *args, **kwargs):
        if self.phone is not '':
            self.phone = changeSpaces(self.phone)

        self.name = capitalizeFirstLetterOfEachWord(self.name)
        super(Member,self).save(*args,**kwargs)


class member_praises(models.Model):
    member = models.ForeignKey(Member)
    praise = models.ForeignKey(Praise)
    instruments = models.ManyToManyField(Instrument)
    score = models.FileField(upload_to='Partituras',verbose_name='partitura',null=True ) #partitura

    class Meta:
        verbose_name = 'Participante'


class Ministry(models.Model):
    name = models.CharField('nombre', max_length=32)
    members = models.ManyToManyField(Member, related_name='members', verbose_name='miembros')
    directings = models.ManyToManyField(Member, through='Ministry_Directing', verbose_name='dirigente')
    #church = models.ForeignKey(Church, null=True, verbose_name='iglesia')

    def __str__(self):
        return self.name

    def get_members(self):
        return ',\n'.join([p.name for p in self.members.order_by('name').all()])
    get_members.short_description = 'Integrantes'

    def get_directings(self):
        return ',\n'.join([p.name for p in self.directings.order_by('name').all()])
    get_directings.short_description = 'Dirigentes'

    class Meta:
        verbose_name = 'Ministerio'


class Ministry_Directing(models.Model):
    member = models.ForeignKey(Member)
    directing = models.ForeignKey(Ministry)
    name = models.CharField('nombre', max_length=32)

    class Meta:
        verbose_name = 'Dirigente'


class Institution(models.Model):
    name = models.CharField('nombre', max_length=25)
    email = models.CharField('correo electrónico', max_length=65,
                             validators=[validators.EmailValidator('El correo no es válido')])
    phone = models.CharField('teléfono', max_length=32,
                             validators=[PhoneValidator])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'


class MoneyTransaction(models.Model):
    TYPE_CHOICES = (
        ('in', 'Entrada'),
        ('out', 'Salida')
    )

    date = models.DateField('fecha')
    amount = models.IntegerField('monto', default=0,
                                 validators=[validators.MinValueValidator(1,
                                                                          message='Las transacciones tiene que tener monto mayor que 0')])

    description = models.CharField('descripción', max_length=124)
    type = models.CharField('tipo', max_length=32, choices=TYPE_CHOICES)
    institution = models.ForeignKey(Institution, null=True, blank=True, verbose_name='institución que dona/recibe')
    member = models.ForeignKey(Member, null=True, blank=True, verbose_name='miembro que dona/recibe')
    status = models.BooleanField('estado',default=False)

    class Meta:
        verbose_name = 'Transacción Monetaria'
        verbose_name_plural = 'Transacciones Monetarias'

    def __str__(self):
        return (str)(self.date)

    def clean(self):
        if (self.institution is None and self.member is None) or (self.institution is not None and self.member is not None):
            raise validators.ValidationError('La transacción debe tener un miembro o una institución')


class Charge(models.Model):
    maxCount = models.IntegerField('cantidad Máxima', default=1, validators=[
        validators.MinValueValidator(1, message='La cantidad maxima de personas en un cargo debe ser mayor que 1')])
    name = models.CharField(max_length=64, validators=[OnlyLettersValidators])
    members = models.ManyToManyField(Member, verbose_name='ocupan el cargo:')

    def clean(self):
        if  self.members.count()  > self.maxCount:
            raise validators.ValidationError((str)(self.members.count()) +' '+(str)(self.maxCount) + ' Ha excedido el numero de ocupantes en ese cargo')

    def get_members(self):
        return ',\n'.join([p.name for p in self.members.order_by('name').all()])
    get_members.short_description = 'Ocupantes'

    class Meta:
        verbose_name = 'Cargo'

    def __str__(self):
        return self.name
