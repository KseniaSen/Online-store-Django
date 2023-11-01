from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['pk']

    title = models.CharField(max_length=128, db_index=True)
    active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='subcategories')

    def __str__(self) -> str:
        return self.title


def category_icons_directory_path(instance: "CategoryIcon", filename):
    if instance.category.parent:
        return 'catalog/icons/{parent}/{category}/{filename}'.format(
            parent=instance.category.parent,
            category=instance.category,
            filename=filename,
        )
    else:
        return 'catalog/icons/{category}/{filename}'.format(
            category=instance.category,
            filename=filename,
        )


class CategoryIcon(models.Model):
    class Meta:
        verbose_name = 'Category icon'
        verbose_name_plural = 'Category icons'
        ordering = ['pk']

    icon = models.ImageField(upload_to=category_icons_directory_path, max_length=500)
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="image")

    def href(self):
        return self.icon

    def __str__(self):
        return f'icon of {self.category.title}'


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['pk']

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Specification(models.Model):
    class Meta:
        verbose_name = 'Specification'
        verbose_name_plural = 'Specifications'
        ordering = ['pk']

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['pk']

    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(max_length=200, blank=True, null=False)
    fullDescription = models.TextField(blank=True, null=False)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=False)
    count = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    freeDelivery = models.BooleanField(default=True)
    rating = models.DecimalField(default=0, max_digits=2, decimal_places=1, null=False)
    limited = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='products')
    specifications = models.ManyToManyField(Specification, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self) -> str:
        return f'Product(pk={self.pk}, title={self.title!r})'


def product_images_directory_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/images/{pk}/{filename}'.format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'
        ordering = ['pk']

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    name = models.CharField(max_length=200, null=False, blank=True)

    def __str__(self) -> str:
        return f"/{self.image}"

    def src(self):
        return self.image


class Review(models.Model):

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['pk']

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='product')
    author = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    rate = models.DecimalField(default=0, max_digits=2, decimal_places=1, null=False)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.author}: {self.product.title}"
