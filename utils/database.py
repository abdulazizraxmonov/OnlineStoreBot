import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.ads = {}

    # Work with categories
    def get_categories(self):
        categories = self.cursor.execute("SELECT id, category_name FROM categories;")
        return categories

    def add_category(self, new_cat):
        categories = self.cursor.execute(
            "SELECT id, category_name FROM categories WHERE category_name=?;",
            (new_cat,)
        ).fetchone()
        # print(categories)
        if not categories:
            try:
                self.cursor.execute(
                    "INSERT INTO categories (category_name) VALUES(?);",
                    (new_cat,)
                )
                self.conn.commit()
                res = {
                    'status': True,
                    'desc': 'Successfully added'
                }
                return res
            except Exception as e:
                res = {
                    'status': False,
                    'desc': 'Something error, please, try again'
                }
                return res
        else:
            res = {
                'status': False,
                'desc': 'exists'
            }
            return res

    def upd_category(self, new_cat, old_cat):
        categories = self.cursor.execute(
            "SELECT id, category_name FROM categories WHERE category_name=?;",
            (new_cat,)
        ).fetchone()

        if not categories:
            try:
                self.cursor.execute(
                    "UPDATE categories SET category_name=? WHERE category_name=?;",
                    (new_cat, old_cat)
                )
                self.conn.commit()
                res = {
                    'status': True,
                    'desc': 'Successfully updated'
                }
                return res
            except Exception as e:
                res = {
                    'status': False,
                    'desc': 'Something error, please, try again'
                }
                return res
        else:
            res = {
                'status': False,
                'desc': 'exists'
            }
            return res

    def edit_category(self, new_name, cat_id):
        try:
            self.cursor.execute(
                "UPDATE categories SET category_name=? WHERE id=?",
                (new_name, cat_id)
            )
            self.conn.commit()
            return True
        except:
            return False

    def del_category(self, cat_name):
        try:
            self.cursor.execute("DELETE FROM categories WHERE category_name=?", (cat_name,))
            self.conn.commit()
            return True
        except:
            return False

    # Work with products
    def get_products(self, cat_id):
        products = self.cursor.execute(
            f"SELECT id, product_name, product_image FROM products WHERE product_category=?;",
            (cat_id,))
        return products

    def insert_ad(self, title, text, price, image, phone, u_id, prod_id, date):
        try:
            self.cursor.execute(
                f"INSERT INTO ads (ad_title, ad_text, ad_price, ad_images, ad_phone, ad_owner, ad_product, ad_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (title, text, price, image, phone, u_id, prod_id, date)
            )
            self.conn.commit()
            return True
        except:
            return False

    def get_my_ads(self, u_id):
        ads = self.cursor.execute(
            f"SELECT id, ad_title, ad_text, ad_price, ad_images FROM ads WHERE ad_owner=?;",
            (u_id,)
        )
        return ads.fetchall()

# Исправленный код для базы данных
    def search_ads_by_text(self, search_query):
        self.cursor.execute("SELECT id, ad_title, ad_text, ad_price, ad_images FROM ads WHERE ad_title LIKE ?", ('%' + search_query + '%',))
        search_results = self.cursor.fetchall()
        ads = []
        for result in search_results:
            ad = {
                'id': result[0],  # Изменено: Теперь выбираем id из запроса
                'ad_title': result[1],
                'ad_text': result[2],
                'ad_price': result[3],
                'ad_images': result[4]
            }
            ads.append(ad)
        return ads if ads else None
    
    def search_ads_by_id(self, ad_id):
        self.cursor.execute("SELECT id, ad_title, ad_text, ad_price, ad_images FROM ads WHERE id = ?", (ad_id,))
        search_result = self.cursor.fetchone()
        if search_result:
            ad = {
                'id': search_result[0],
                'ad_title': search_result[1],
                'ad_text': search_result[2],
                'ad_price': search_result[3],
                'ad_images': search_result[4]
            }
            return [ad]
        else:
            return None
    