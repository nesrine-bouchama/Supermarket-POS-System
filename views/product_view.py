"""
Product View — Product management with search, advanced filters,
table, add/edit form, and delete.
"""

import customtkinter as ctk
from tkinter import ttk
from controllers.product_controller import ProductController
from models.product_model import ProductModel
from utils.notifications import success, error, confirm
from views.theme import COLORS, FONTS


class ProductView:

    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=25, pady=25)

        # ═══════════════════════════════════
        #  HEADER
        # ═══════════════════════════════════
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header, text="📦  Product Management",
            font=FONTS["heading_lg"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        # ═══════════════════════════════════
        #  ADVANCED FILTERS ROW
        # ═══════════════════════════════════
        filter_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        filter_card.pack(fill="x", pady=(0, 12))

        filter_inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        filter_inner.pack(fill="x", padx=18, pady=12)

        ctk.CTkLabel(
            filter_inner, text="🔍  Filters",
            font=FONTS["body_bold"],
            text_color=COLORS["text_primary"],
        ).pack(side="left", padx=(0, 15))

        es = {
            "height": 36,
            "fg_color": COLORS["bg_input"],
            "border_color": COLORS["border"],
            "text_color": COLORS["text_primary"],
            "font": FONTS["body"],
            "corner_radius": 8,
        }

        # Name search
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.apply_filters())

        ctk.CTkEntry(
            filter_inner,
            placeholder_text="Product name...",
            width=180, textvariable=self.search_var, **es,
        ).pack(side="left", padx=(0, 8))

        # Category filter
        ctk.CTkLabel(
            filter_inner, text="Category:",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
        ).pack(side="left", padx=(5, 4))

        categories = ["All"] + ProductController.get_categories()
        self.category_var = ctk.StringVar(value="All")

        ctk.CTkOptionMenu(
            filter_inner, variable=self.category_var,
            values=categories if len(categories) > 1 else ["All"],
            width=140, height=36,
            fg_color=COLORS["bg_input"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            text_color=COLORS["text_primary"],
            font=FONTS["body"],
            corner_radius=8,
            command=lambda _: self.apply_filters(),
        ).pack(side="left", padx=(0, 8))

        # Min price
        ctk.CTkLabel(
            filter_inner, text="Price:",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
        ).pack(side="left", padx=(5, 4))

        self.min_price_entry = ctk.CTkEntry(
            filter_inner, placeholder_text="Min",
            width=80, **es,
        )
        self.min_price_entry.pack(side="left", padx=(0, 4))

        ctk.CTkLabel(
            filter_inner, text="—",
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
        ).pack(side="left", padx=2)

        self.max_price_entry = ctk.CTkEntry(
            filter_inner, placeholder_text="Max",
            width=80, **es,
        )
        self.max_price_entry.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            filter_inner, text="Apply",
            width=70, height=36,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self.apply_filters,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            filter_inner, text="Reset",
            width=70, height=36,
            fg_color=COLORS["bg_card_hover"],
            hover_color=COLORS["border_light"],
            text_color=COLORS["text_secondary"],
            font=FONTS["body"],
            corner_radius=8,
            command=self.reset_filters,
        ).pack(side="left")

        # ═══════════════════════════════════
        #  PRODUCT TABLE
        # ═══════════════════════════════════
        table_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        table_card.pack(fill="both", expand=True, pady=(0, 12))

        columns = ("Name", "Category", "Price", "Stock", "Barcode", "Description")
        self.tree = ttk.Treeview(
            table_card, columns=columns,
            show="headings", style="Dark.Treeview",
        )

        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Price", text="Price (DZD)")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Description", text="Description")

        self.tree.column("Name", width=170, minwidth=120)
        self.tree.column("Category", width=110, minwidth=80)
        self.tree.column("Price", width=90, anchor="center")
        self.tree.column("Stock", width=60, anchor="center")
        self.tree.column("Barcode", width=100, anchor="center")
        self.tree.column("Description", width=200, minwidth=120)

        # Tags
        self.tree.tag_configure("low_stock", foreground=COLORS["danger"])
        self.tree.tag_configure("out_stock", foreground=COLORS["text_muted"])
        self.tree.tag_configure("normal", foreground=COLORS["text_primary"])

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_card, orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 6))

        self.load_products()

        # ═══════════════════════════════════
        #  ADD PRODUCT FORM
        # ═══════════════════════════════════
        form_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        form_card.pack(fill="x")

        # Form header
        ctk.CTkLabel(
            form_card, text="➕  Add New Product",
            font=FONTS["heading_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=20, pady=(15, 10))

        # Form row
        form_row = ctk.CTkFrame(form_card, fg_color="transparent")
        form_row.pack(fill="x", padx=20, pady=(0, 6))

        es_form = {
            "height": 40,
            "fg_color": COLORS["bg_input"],
            "border_color": COLORS["border"],
            "text_color": COLORS["text_primary"],
            "font": FONTS["body"],
            "corner_radius": 8,
        }

        self.name_entry = ctk.CTkEntry(form_row, placeholder_text="Name", width=150, **es_form)
        self.category_entry = ctk.CTkEntry(form_row, placeholder_text="Category", width=110, **es_form)
        self.price_entry = ctk.CTkEntry(form_row, placeholder_text="Price", width=90, **es_form)
        self.qty_entry = ctk.CTkEntry(form_row, placeholder_text="Qty", width=70, **es_form)
        self.barcode_entry = ctk.CTkEntry(form_row, placeholder_text="Barcode", width=110, **es_form)

        self.name_entry.pack(side="left", padx=(0, 5))
        self.category_entry.pack(side="left", padx=(0, 5))
        self.price_entry.pack(side="left", padx=(0, 5))
        self.qty_entry.pack(side="left", padx=(0, 5))
        self.barcode_entry.pack(side="left", padx=(0, 5))

        # Description row
        form_row2 = ctk.CTkFrame(form_card, fg_color="transparent")
        form_row2.pack(fill="x", padx=20, pady=(0, 14))

        self.desc_entry = ctk.CTkEntry(
            form_row2, placeholder_text="Product description...",
            width=400, **es_form,
        )
        self.desc_entry.pack(side="left", padx=(0, 10))

        # Buttons
        ctk.CTkButton(
            form_row2, text="✓  Add",
            width=100, height=40,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self.add_product,
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            form_row2, text="✏️  Edit",
            width=100, height=40,
            fg_color=COLORS["warning"],
            hover_color="#d99520",
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self.open_edit_dialog,
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            form_row2, text="🗑  Delete",
            width=100, height=40,
            fg_color=COLORS["danger"],
            hover_color="#d94040",
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self.delete_product,
        ).pack(side="left")

    # ─── Load / reload products ───
    def load_products(self, products=None):
        self.tree.delete(*self.tree.get_children())
        if products is None:
            products = ProductController.get_products()

        for p in products:
            stock = p.get("quantity", 0)
            if stock <= 0:
                tag = "out_stock"
            elif stock <= 5:
                tag = "low_stock"
            else:
                tag = "normal"

            self.tree.insert(
                "", "end",
                iid=str(p["_id"]),
                values=(
                    p.get("name", ""),
                    p.get("category", "N/A"),
                    f"{p.get('price', 0):,.0f}",
                    stock,
                    p.get("barcode", "N/A"),
                    p.get("description", "—"),
                ),
                tags=(tag,),
            )

    # ─── Apply advanced filters ───
    def apply_filters(self):
        name = self.search_var.get().strip() or None
        category = self.category_var.get()

        min_price = None
        max_price = None
        try:
            val = self.min_price_entry.get().strip()
            if val:
                min_price = float(val)
        except ValueError:
            pass
        try:
            val = self.max_price_entry.get().strip()
            if val:
                max_price = float(val)
        except ValueError:
            pass

        products = ProductController.filter_products(
            category=category if category != "All" else None,
            min_price=min_price,
            max_price=max_price,
            name=name,
        )
        self.load_products(products)

    # ─── Reset all filters ───
    def reset_filters(self):
        self.search_var.set("")
        self.category_var.set("All")
        self.min_price_entry.delete(0, "end")
        self.max_price_entry.delete(0, "end")
        self.load_products()

    # ─── Add product from form ───
    def add_product(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                error("Product name is required")
                return

            ProductController.add_product({
                "name": name,
                "category": self.category_entry.get().strip(),
                "price": float(self.price_entry.get()),
                "quantity": int(self.qty_entry.get()),
                "barcode": self.barcode_entry.get().strip(),
                "description": self.desc_entry.get().strip(),
            })

            # Clear form fields
            for entry in (self.name_entry, self.category_entry,
                          self.price_entry, self.qty_entry,
                          self.barcode_entry, self.desc_entry):
                entry.delete(0, "end")

            self.load_products()
            success("✅ Product added successfully!")

        except ValueError as e:
            error(f"Invalid input: {e}")
        except Exception as e:
            error(f"Error: {e}")

    # ─── Open edit dialog for selected product ───
    def open_edit_dialog(self):
        selected = self.tree.focus()
        if not selected:
            error("Select a product to edit")
            return

        # Fetch the current product data from the DB
        products = ProductController.get_products()
        product = next((p for p in products if str(p["_id"]) == selected), None)
        if not product:
            error("Product not found")
            return

        # Create edit dialog
        dialog = ctk.CTkToplevel()
        dialog.title("✏️ Edit Product")
        dialog.geometry("500x520")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS["bg_darkest"])
        dialog.grab_set()
        dialog.focus_set()

        # Center the dialog
        dialog.update_idletasks()
        sw = dialog.winfo_screenwidth()
        sh = dialog.winfo_screenheight()
        x = (sw // 2) - 250
        y = (sh // 2) - 260
        dialog.geometry(f"500x520+{x}+{y}")

        # Dialog content
        card = ctk.CTkFrame(
            dialog, fg_color=COLORS["bg_card"],
            corner_radius=14, border_width=1,
            border_color=COLORS["border"],
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            card, text="✏️  Edit Product",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"],
        ).pack(pady=(20, 18))

        es = {
            "height": 40,
            "fg_color": COLORS["bg_input"],
            "border_color": COLORS["border"],
            "text_color": COLORS["text_primary"],
            "font": FONTS["body"],
            "corner_radius": 8,
        }

        fields = {}
        field_defs = [
            ("Name", "name", product.get("name", "")),
            ("Category", "category", product.get("category", "")),
            ("Price (DZD)", "price", str(product.get("price", ""))),
            ("Quantity", "quantity", str(product.get("quantity", ""))),
            ("Barcode", "barcode", product.get("barcode", "")),
            ("Description", "description", product.get("description", "")),
        ]

        for label_text, key, default_val in field_defs:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=3)

            ctk.CTkLabel(
                row, text=label_text,
                font=FONTS["body"],
                text_color=COLORS["text_secondary"],
                width=100, anchor="w",
            ).pack(side="left")

            entry = ctk.CTkEntry(row, width=280, **es)
            entry.insert(0, default_val)
            entry.pack(side="left", padx=(5, 0))
            fields[key] = entry

        # Buttons row
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=(20, 20))

        def save_edit():
            try:
                data = {
                    "name": fields["name"].get().strip(),
                    "category": fields["category"].get().strip(),
                    "price": float(fields["price"].get()),
                    "quantity": int(fields["quantity"].get()),
                    "barcode": fields["barcode"].get().strip(),
                    "description": fields["description"].get().strip(),
                }
                ProductController.update_product(selected, data)
                dialog.destroy()
                self.load_products()
                success("✅ Product updated successfully!")
            except ValueError as e:
                error(f"Invalid input: {e}")
            except Exception as e:
                error(f"Error: {e}")

        ctk.CTkButton(
            btn_row, text="💾  Save Changes",
            width=160, height=42,
            fg_color=COLORS["success"],
            hover_color="#2ea870",
            font=FONTS["button"],
            corner_radius=10,
            command=save_edit,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_row, text="Cancel",
            width=100, height=42,
            fg_color=COLORS["bg_card_hover"],
            hover_color=COLORS["border_light"],
            text_color=COLORS["text_secondary"],
            font=FONTS["body_bold"],
            corner_radius=10,
            command=dialog.destroy,
        ).pack(side="left")

    # ─── Delete selected product ───
    def delete_product(self):
        selected = self.tree.focus()
        if not selected:
            error("Select a product to delete")
            return

        if confirm("Are you sure you want to delete this product?"):
            ProductModel.delete_product(selected)
            self.load_products()
            success("🗑  Product deleted")