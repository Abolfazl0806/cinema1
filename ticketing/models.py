from django.db import models


# Create your models here.
class Movie(models.Model):
    """
    Represent a movie
    """

    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم'

    name = models.CharField('عنوان', max_length=100)
    director = models.CharField('کارگردان', max_length=50)
    year = models.IntegerField('سال تولید')
    length = models.IntegerField('زمان فیلم')
    description = models.TextField('توضیحات')
    poster = models.ImageField('پوستر', upload_to='movie_posters/')

    def __str__(self):
        return self.name


class Cinema(models.Model):
    """
    Represent a cinema salon
    """

    class Meta:
        verbose_name = 'سینما'
        verbose_name_plural = 'سینما'

    cinema_code = models.IntegerField(primary_key=True)
    name = models.CharField('نام سینما', max_length=50)
    city = models.CharField('شهر', max_length=50, default="تهران")
    capacity = models.IntegerField('گنجایش')
    phone = models.CharField('تلفن', max_length=20, null=True)
    address = models.TextField('آدرس')
    image = models.ImageField('تصویر', upload_to='cinema_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class ShowTime(models.Model):
    """
    models.CASCADE: Prevents deletion of referenced objects by raising RestrictedError (subclass of Django.DB) (prevents integrity errors)
    models.RESTRICT: Objects referenced through the CASCADE relationship are also deleted.
    models.PROTECT: When the value viewed by the ForeignKeyField is deleted, ProtectedError is raised to prevent deletion.
    models.SET_NULL: When the value viewed by the ForeignKeyField is deleted, the ForeignKeyField value is set to NULL.
    models.DO_NOTHING: Takes no action when the value the ForeignKeyField looks at is deleted.
"""

    class Meta:
        verbose_name = 'سانس'
        verbose_name_plural = 'سانس'

    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='فیلم')
    cinema = models.ForeignKey('Cinema', on_delete=models.PROTECT, verbose_name='سینما')

    start_time = models.DateTimeField('زمان شروع نمایش')
    price = models.IntegerField('قیمت')
    salable_seate = models.IntegerField('صندلی های قابل فروش')
    free_eats = models.IntegerField('صندلی های خالی')

    SALE_NOTE_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYER = 5
    SHOW_CANSELED = 6
    status_choises = (
        (SALE_NOTE_STARTED, 'فروش آغاز نشد'),
        (SALE_OPEN, 'در حال فروش بلیت'),
        (TICKETS_SOLD, 'بلیت ها تمام شد'),
        (SALE_CLOSED, 'فروش بلیت بسته شد'),
        (MOVIE_PLAYER, 'فیلم پخش شد'),
        (SHOW_CANSELED, 'سانس لغو شد')
    )

    status = models.IntegerField(choices=status_choises)

    def __str__(self):
        return '{} - {} - {}'.format(self.movie, self.cinema, self.start_time)

    def get_price_display(self):
        return '{} تومان'.format(self.price)

    def is_full(self):
        return self.free_eats == 0

    def reserve_seats(self, seat_count):
        """
        Reserves one or more seats for a customer
        :param seat_count: An integer as the number of seats to be reserved
        """
        assert isinstance(seat_count, int) and seat_count > 0, 'Number of seats should be a positive integer'
        assert self.status == ShowTime.SALE_OPEN, 'Sale is not open'
        assert self.free_eats >= seat_count, 'Not enough free seats'
        self.free_eats -= seat_count
        if self.free_eats == 0:
            self.status = ShowTime.TICKETS_SOLD
        self.save()


class Ticket(models.Model):
    """
    Represents one or more tickets, bought by a user in an order
    """

    class Meta:
        verbose_name = 'بلیت'
        verbose_name_plural = 'بلیت'

    showtime = models.ForeignKey('ShowTime', on_delete=models.PROTECT, verbose_name='سانس')
    customer = models.ForeignKey('accounts.Profile', on_delete=models.PROTECT, verbose_name='خریدار')
    seat_count = models.IntegerField('تعداد صندلی')
    order_time = models.DateTimeField('زمان خرید', auto_now_add=True)

    def __str__(self):
        return "{} بلیت به نام {} برای فیلم {}".format(self.seat_count, self.customer, self.showtime.movie)
