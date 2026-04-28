from random import randint, choice

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from categories.models import Category
from products.models import Product
from customers.models import Customer
from orders.models import Order, OrderItem

try:
    from faker import Faker
    fake = Faker("en_US")
except ImportError:
    fake = None

User = get_user_model()


class Command(BaseCommand):
    help = "Ma'lumotlar bazasini test ma'lumotlar bilan to'ldiradi"

    def handle(self, *args, **options):
        if not fake:
            self.stderr.write("faker kutubxonasi o'rnatilmagan: pip install faker")
            return

        self._seed_superuser()
        self._seed_customers()
        self._seed_categories()
        self._seed_products()
        self._seed_orders()
        self.stdout.write(self.style.SUCCESS("Seed muvaffaqiyatli yakunlandi."))

    def _seed_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', '', 'admin123')
            self.stdout.write("Superuser 'admin' yaratildi (parol: admin123)")

    def _seed_customers(self):
        Customer.objects.all().delete()
        customers = []
        for _ in range(10):
            c = Customer(
                full_name=fake.name(),
                phone=fake.phone_number()[:30],
                default_address=fake.address().replace("\n", ", "),
            )
            c.set_password("customer123")
            customers.append(c)
        Customer.objects.bulk_create(customers)
        self.stdout.write(f"10 ta mijoz yaratildi (parol: customer123)")

    def _seed_categories(self):
        Category.objects.all().delete()
        data = [
            ("Elektronika", "piece"),
            ("Kiyim-kechak", "piece"),
            ("Oziq-ovqat", "weight"),
            ("Kitoblar", "piece"),
        ]
        Category.objects.bulk_create([Category(name=n, unit_type=u) for n, u in data])
        self.stdout.write(f"{len(data)} ta kategoriya yaratildi")

    def _seed_products(self):
        Product.objects.all().delete()
        categories = list(Category.objects.all())
        products = []
        for cat in categories:
            for _ in range(10):
                products.append(Product(
                    name=f"{cat.name} {fake.word().capitalize()}",
                    price=randint(5000, 200000),
                    description=fake.sentence(),
                    status=Product.STATUS_ACTIVE,
                    is_top=choice([True, False]),
                    category=cat,
                    image_path=f"https://picsum.photos/seed/{randint(1, 10000)}/400/400",
                ))
        Product.objects.bulk_create(products)
        self.stdout.write(f"{len(products)} ta mahsulot yaratildi")

    def _seed_orders(self):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        customers = list(Customer.objects.all())
        products = list(Product.objects.all())
        statuses = [Order.STATUS_NEW, Order.STATUS_COMPLETED, Order.STATUS_CANCELED]
        for _ in range(15):
            customer = choice(customers)
            order = Order.objects.create(
                customer=customer,
                customer_name=customer.full_name,
                customer_phone=customer.phone,
                address=customer.default_address or "Unknown",
                status=choice(statuses),
                total_price=0,
            )
            total = 0
            for _ in range(randint(1, 3)):
                p = choice(products)
                qty = randint(1, 5)
                line_total = p.price * qty
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    product_name=p.name,
                    unit_price=p.price,
                    quantity=qty,
                    total_price=line_total,
                )
                total += line_total
            order.total_price = total
            order.save()
        self.stdout.write("15 ta buyurtma yaratildi")
