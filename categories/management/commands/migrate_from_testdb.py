import sqlite3
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connection


SOURCE_DB = Path(__file__).resolve().parents[3] / 'test.db'


class Command(BaseCommand):
    help = 'test.db (FastAPI) dan Django db.sqlite3 ga ma\'lumotlarni ko\'chiradi'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Ko\'chirishdan oldin Django DB dagi mavjud ma\'lumotlarni o\'chiradi'
        )
        parser.add_argument(
            '--source', type=str, default=str(SOURCE_DB),
            help=f'Manba DB fayl yo\'li (default: {SOURCE_DB})'
        )

    def handle(self, *args, **options):
        source_path = Path(options['source'])
        if not source_path.exists():
            raise CommandError(f"Fayl topilmadi: {source_path}")

        self.stdout.write(f"Manba: {source_path}")

        src = sqlite3.connect(source_path)
        src.row_factory = sqlite3.Row

        try:
            with transaction.atomic():
                if options['clear']:
                    self._clear_django_data()

                stats = {}
                stats['categories'] = self._migrate_categories(src)
                stats['products']   = self._migrate_products(src)
                stats['customers']  = self._migrate_customers(src)
                stats['orders']     = self._migrate_orders(src)
                stats['order_items']= self._migrate_order_items(src)
                stats['carts']      = self._migrate_carts(src)
                stats['cart_items'] = self._migrate_cart_items(src)

                # SQLite sequence larni yangilash (keyingi INSERT to'g'ri ID olishi uchun)
                self._reset_sequences()

        finally:
            src.close()

        self.stdout.write(self.style.SUCCESS('\n✓ Ko\'chirish yakunlandi:'))
        for model, count in stats.items():
            self.stdout.write(f'  {model}: {count} ta yozuv')

    # ------------------------------------------------------------------ helpers

    def _clear_django_data(self):
        from cart.models import CartItem, Cart
        from orders.models import OrderItem, Order
        from products.models import Product
        from customers.models import Customer
        from categories.models import Category

        self.stdout.write('Eski Django ma\'lumotlari o\'chirilmoqda...')
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Category.objects.all().delete()

    def _reset_sequences(self):
        """SQLite da auto-increment sequence ni max(id)+1 ga sozlaydi."""
        tables = [
            'categories_category',
            'products_product',
            'customers_customer',
            'orders_order',
            'orders_orderitem',
            'cart_cart',
            'cart_cartitem',
        ]
        with connection.cursor() as cur:
            for table in tables:
                try:
                    cur.execute(f'SELECT MAX(id) FROM "{table}"')
                    max_id = cur.fetchone()[0] or 0
                    cur.execute(
                        'INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES (%s, %s)',
                        [table, max_id]
                    )
                except Exception:
                    pass

    # ------------------------------------------------------------------ migrations

    def _migrate_categories(self, src):
        from categories.models import Category

        rows = src.execute('SELECT id, name, unit_type FROM categories ORDER BY id').fetchall()
        created = 0
        for row in rows:
            _, made = Category.objects.update_or_create(
                id=row['id'],
                defaults={'name': row['name'], 'unit_type': row['unit_type']}
            )
            if made:
                created += 1
        self.stdout.write(f'  categories: {len(rows)} ta ({created} yangi)')
        return len(rows)

    def _migrate_products(self, src):
        from products.models import Product

        rows = src.execute(
            'SELECT id, name, price, description, image_path, is_top, status, category_id FROM products ORDER BY id'
        ).fetchall()
        created = 0
        for row in rows:
            _, made = Product.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name':        row['name'],
                    'price':       row['price'],
                    'description': row['description'],
                    'image_path':  row['image_path'],
                    'is_top':      bool(row['is_top']),
                    'status':      row['status'] or 'active',
                    'category_id': row['category_id'],
                }
            )
            if made:
                created += 1
        self.stdout.write(f'  products: {len(rows)} ta ({created} yangi)')
        return len(rows)

    def _migrate_customers(self, src):
        from customers.models import Customer

        rows = src.execute(
            'SELECT id, full_name, phone, hashed_password, default_address, created_at FROM customers ORDER BY id'
        ).fetchall()
        created = 0
        for row in rows:
            _, made = Customer.objects.update_or_create(
                id=row['id'],
                defaults={
                    'full_name':       row['full_name'],
                    'phone':           row['phone'],
                    'hashed_password': row['hashed_password'],  # passlib hash saqlanadi
                    'default_address': row['default_address'],
                }
            )
            if made:
                created += 1

        # created_at ni to'g'ridan-to'g'ri SQL orqali yangilaymiz (auto_now_add o'zgartirish imkoni yo'q)
        with connection.cursor() as cur:
            for row in rows:
                if row['created_at']:
                    cur.execute(
                        'UPDATE customers_customer SET created_at=%s WHERE id=%s',
                        [row['created_at'], row['id']]
                    )

        self.stdout.write(f'  customers: {len(rows)} ta ({created} yangi)')
        return len(rows)

    def _migrate_orders(self, src):
        from orders.models import Order

        rows = src.execute(
            'SELECT id, customer_id, customer_name, customer_phone, address, status, total_price, created_at, updated_at FROM orders ORDER BY id'
        ).fetchall()
        created = 0
        for row in rows:
            _, made = Order.objects.update_or_create(
                id=row['id'],
                defaults={
                    'customer_id':    row['customer_id'],
                    'customer_name':  row['customer_name'],
                    'customer_phone': row['customer_phone'],
                    'address':        row['address'],
                    'status':         row['status'] or 'new',
                    'total_price':    row['total_price'] or 0,
                }
            )
            if made:
                created += 1

        with connection.cursor() as cur:
            for row in rows:
                cur.execute(
                    'UPDATE orders_order SET created_at=%s, updated_at=%s WHERE id=%s',
                    [row['created_at'], row['updated_at'], row['id']]
                )

        self.stdout.write(f'  orders: {len(rows)} ta ({created} yangi)')
        return len(rows)

    def _migrate_order_items(self, src):
        from orders.models import OrderItem
        from products.models import Product

        existing_products = set(Product.objects.values_list('id', flat=True))
        rows = src.execute(
            'SELECT id, order_id, product_id, product_name, unit_price, quantity, total_price FROM order_items ORDER BY id'
        ).fetchall()
        created = skipped_fk = 0
        for row in rows:
            # Mahsulot o'chirilgan bo'lsa product_id=NULL (product_name saqlanadi)
            product_id = row['product_id'] if row['product_id'] in existing_products else None
            if row['product_id'] not in existing_products:
                skipped_fk += 1
            _, made = OrderItem.objects.update_or_create(
                id=row['id'],
                defaults={
                    'order_id':     row['order_id'],
                    'product_id':   product_id,
                    'product_name': row['product_name'],
                    'unit_price':   row['unit_price'],
                    'quantity':     row['quantity'],
                    'total_price':  row['total_price'],
                }
            )
            if made:
                created += 1
        if skipped_fk:
            self.stdout.write(
                self.style.WARNING(f'  order_items: {len(rows)} ta ({created} yangi, {skipped_fk} ta product_id=NULL — eski o\'chirilgan mahsulot)')
            )
        else:
            self.stdout.write(f'  order_items: {len(rows)} ta ({created} yangi)')
        return len(rows)

    def _migrate_carts(self, src):
        from cart.models import Cart

        rows = src.execute(
            'SELECT id, session_id, status, created_at, updated_at FROM carts ORDER BY id'
        ).fetchall()
        created = 0
        for row in rows:
            _, made = Cart.objects.update_or_create(
                id=row['id'],
                defaults={
                    'session_id': row['session_id'],
                    'status':     row['status'] or 'open',
                }
            )
            if made:
                created += 1

        with connection.cursor() as cur:
            for row in rows:
                if row['created_at']:
                    cur.execute(
                        'UPDATE cart_cart SET created_at=%s, updated_at=%s WHERE id=%s',
                        [row['created_at'], row['updated_at'], row['id']]
                    )

        self.stdout.write(f'  carts: {len(rows)} ta ({created} yangi)')
        return len(rows)

    def _migrate_cart_items(self, src):
        from cart.models import CartItem
        from products.models import Product

        existing_products = set(Product.objects.values_list('id', flat=True))
        rows = src.execute(
            'SELECT id, cart_id, product_id, quantity, unit_price FROM cart_items ORDER BY id'
        ).fetchall()
        created = skipped = 0
        for row in rows:
            if row['product_id'] not in existing_products:
                skipped += 1
                continue
            _, made = CartItem.objects.update_or_create(
                id=row['id'],
                defaults={
                    'cart_id':    row['cart_id'],
                    'product_id': row['product_id'],
                    'quantity':   row['quantity'],
                    'unit_price': row['unit_price'],
                }
            )
            if made:
                created += 1
        if skipped:
            self.stdout.write(
                self.style.WARNING(f'  cart_items: {len(rows) - skipped} ta ko\'chirildi ({created} yangi, {skipped} ta o\'tkazib yuborildi — eski o\'chirilgan mahsulot)')
            )
        else:
            self.stdout.write(f'  cart_items: {len(rows)} ta ({created} yangi)')
        return len(rows)
