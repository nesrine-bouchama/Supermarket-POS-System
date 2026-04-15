"""
Sales View — Point of Sale with split layout: product browser + cart + payment.
Features: barcode scanning, product search, cart with qty controls, cash/card payment.
"""

import customtkinter as ctk
from tkinter import ttk
from controllers.product_controller import ProductController
from controllers.sale_controller import SaleController
from models.product_model import ProductModel
from utils.notifications import success, error
from views.theme import COLORS, FONTS


class SalesView:

    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=25, pady=25)

        self.cart = []
        self.products = ProductController.get_products()

        # ─── Header ───
        ctk.CTkLabel(
            self.frame, text="🛒  Point of Sale",
            font=FONTS["heading_lg"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 15))

        # ═══════════════════════════════════
        #  SPLIT LAYOUT
        # ═══════════════════════════════════
        main = ctk.CTkFrame(self.frame, fg_color="transparent")
        main.pack(fill="both", expand=True)

        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(0, weight=1)

        # ─────────────────────────────────
        #  LEFT: Products browser
        # ─────────────────────────────────
        left = ctk.CTkFrame(
            main, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Search + Barcode row
        search_row = ctk.CTkFrame(left, fg_color="transparent")
        search_row.pack(fill="x", padx=15, pady=12)

        es = {
            "height": 38,
            "fg_color": COLORS["bg_input"],
            "border_color": COLORS["border"],
            "text_color": COLORS["text_primary"],
            "font": FONTS["body"],
            "corner_radius": 8,
        }

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter_products())

        ctk.CTkEntry(
            search_row,
            placeholder_text="🔍  Search products...",
            width=200, textvariable=self.search_var, **es,
        ).pack(side="left", padx=(0, 8))

        self.barcode_entry = ctk.CTkEntry(
            search_row,
            placeholder_text="📱  Scan barcode...",
            width=170, **es,
        )
        self.barcode_entry.pack(side="left", padx=(0, 8))
        self.barcode_entry.bind("<Return>", self._scan_barcode)

        ctk.CTkButton(
            search_row, text="➕ Add",
            width=80, height=38,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self._add_to_cart,
        ).pack(side="right")

        # Product table
        self.product_tree = ttk.Treeview(
            left,
            columns=("Name", "Category", "Price", "Stock"),
            show="headings", style="Dark.Treeview",
        )

        self.product_tree.heading("Name", text="Product")
        self.product_tree.heading("Category", text="Category")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Stock", text="Stock")

        self.product_tree.column("Name", width=180, minwidth=120)
        self.product_tree.column("Category", width=100, minwidth=70)
        self.product_tree.column("Price", width=80, anchor="center")
        self.product_tree.column("Stock", width=60, anchor="center")

        self.product_tree.tag_configure("low", foreground=COLORS["warning"])
        self.product_tree.tag_configure("out", foreground=COLORS["danger"])
        self.product_tree.tag_configure("ok", foreground=COLORS["text_primary"])

        self.product_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Double-click to add
        self.product_tree.bind("<Double-1>", lambda _: self._add_to_cart())

        self._load_products()

        # ─────────────────────────────────
        #  RIGHT: Cart + Payment
        # ─────────────────────────────────
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")

        # ═══ Cart Card ═══
        cart_card = ctk.CTkFrame(
            right, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        cart_card.pack(fill="both", expand=True, pady=(0, 10))

        # Cart header
        cart_hdr = ctk.CTkFrame(cart_card, fg_color="transparent")
        cart_hdr.pack(fill="x", padx=15, pady=(12, 5))

        ctk.CTkLabel(
            cart_hdr, text="🛒  Cart",
            font=FONTS["heading_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        ctk.CTkButton(
            cart_hdr, text="Clear",
            width=60, height=28,
            fg_color=COLORS["danger"],
            hover_color="#d94040",
            font=FONTS["caption"],
            corner_radius=6,
            command=self._clear_cart,
        ).pack(side="right")

        # Cart table
        self.cart_tree = ttk.Treeview(
            cart_card,
            columns=("Name", "Qty", "Price", "Total"),
            show="headings", style="Dark.Treeview",
            height=8,
        )

        self.cart_tree.heading("Name", text="Item")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Total", text="Total")

        self.cart_tree.column("Name", width=130, minwidth=90)
        self.cart_tree.column("Qty", width=45, anchor="center")
        self.cart_tree.column("Price", width=65, anchor="center")
        self.cart_tree.column("Total", width=75, anchor="center")

        self.cart_tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Cart controls
        ctrl = ctk.CTkFrame(cart_card, fg_color="transparent")
        ctrl.pack(fill="x", padx=15, pady=(0, 5))

        btn_style = {
            "width": 38, "height": 32,
            "fg_color": COLORS["bg_card_hover"],
            "hover_color": COLORS["border_light"],
            "corner_radius": 6,
        }

        ctk.CTkButton(
            ctrl, text="−", font=("Segoe UI", 18, "bold"),
            command=lambda: self._adjust_qty(-1), **btn_style,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            ctrl, text="+", font=("Segoe UI", 18, "bold"),
            command=lambda: self._adjust_qty(1), **btn_style,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            ctrl, text="Remove",
            width=75, height=32,
            fg_color=COLORS["danger"],
            hover_color="#d94040",
            font=FONTS["caption"],
            corner_radius=6,
            command=self._remove_from_cart,
        ).pack(side="left")

        # Total
        self.total_label = ctk.CTkLabel(
            cart_card, text="Total:  0  DZD",
            font=FONTS["heading"],
            text_color=COLORS["success"],
        )
        self.total_label.pack(padx=15, pady=(8, 14))

        # ═══ Payment Card ═══
        pay_card = ctk.CTkFrame(
            right, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        pay_card.pack(fill="x")

        ctk.CTkLabel(
            pay_card, text="💳  Payment",
            font=FONTS["heading_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=15, pady=(12, 8))

        # Payment type
        pay_row = ctk.CTkFrame(pay_card, fg_color="transparent")
        pay_row.pack(fill="x", padx=15)

        self.payment_type = ctk.StringVar(value="cash")

        radio_style = {
            "font": FONTS["body"],
            "text_color": COLORS["text_primary"],
            "fg_color": COLORS["accent"],
            "border_color": COLORS["border"],
        }

        ctk.CTkRadioButton(
            pay_row, text="Cash",
            variable=self.payment_type, value="cash", **radio_style,
        ).pack(side="left", padx=(0, 20))

        ctk.CTkRadioButton(
            pay_row, text="Card",
            variable=self.payment_type, value="card", **radio_style,
        ).pack(side="left")

        # Cash input
        cash_row = ctk.CTkFrame(pay_card, fg_color="transparent")
        cash_row.pack(fill="x", padx=15, pady=8)

        self.cash_entry = ctk.CTkEntry(
            cash_row,
            placeholder_text="Cash received...",
            width=150, **es,
        )
        self.cash_entry.pack(side="left", padx=(0, 10))

        self.change_label = ctk.CTkLabel(
            cash_row, text="Change: —",
            font=FONTS["body_bold"],
            text_color=COLORS["text_secondary"],
        )
        self.change_label.pack(side="left")

        # Checkout button
        ctk.CTkButton(
            pay_card, text="💳   CHECKOUT",
            height=46,
            fg_color=COLORS["success"],
            hover_color="#2ea870",
            font=FONTS["button"],
            corner_radius=10,
            command=self._checkout,
        ).pack(fill="x", padx=15, pady=(5, 15))

    # ══════════════════════════════════════
    #  PRODUCT METHODS
    # ══════════════════════════════════════

    def _load_products(self, filter_text=""):
        self.product_tree.delete(*self.product_tree.get_children())
        for p in self.products:
            name = p.get("name", "")
            if filter_text and filter_text.lower() not in name.lower():
                continue
            stock = p.get("quantity", 0)
            tag = "out" if stock <= 0 else ("low" if stock <= 5 else "ok")
            self.product_tree.insert(
                "", "end",
                iid=str(p["_id"]),
                values=(
                    name,
                    p.get("category", ""),
                    f"{p.get('price', 0):,.0f}",
                    stock,
                ),
                tags=(tag,),
            )

    def _filter_products(self):
        self._load_products(self.search_var.get())

    def _scan_barcode(self, event=None):
        code = self.barcode_entry.get().strip()
        if not code:
            return

        product = ProductModel.find_by_barcode(code)
        if product:
            self._add_item(product)
            success(f"✅  {product['name']} added")
        else:
            error("Product not found for this barcode")

        self.barcode_entry.delete(0, "end")

    # ══════════════════════════════════════
    #  CART METHODS
    # ══════════════════════════════════════

    def _add_to_cart(self):
        selected = self.product_tree.focus()
        if not selected:
            error("Select a product first")
            return

        p = next((x for x in self.products if str(x["_id"]) == selected), None)
        if p:
            self._add_item(p)

    def _add_item(self, product):
        """Add product to cart or increment quantity if already present."""
        available_stock = product.get("quantity", 0)

        # Check how many are already in the cart
        in_cart = 0
        for item in self.cart:
            if str(item["_id"]) == str(product["_id"]):
                in_cart = item["quantity"]
                break

        # Check stock availability
        if available_stock <= 0:
            error(f"'{product['name']}' is out of stock!")
            return
        if in_cart >= available_stock:
            error(f"Cannot add more — only {available_stock} in stock!")
            return

        for item in self.cart:
            if str(item["_id"]) == str(product["_id"]):
                item["quantity"] += 1
                self._refresh_cart()
                return

        self.cart.append({
            "_id": product["_id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": 1,
        })
        self._refresh_cart()

    def _adjust_qty(self, delta):
        selected = self.cart_tree.focus()
        if not selected:
            return

        idx = int(selected)
        if 0 <= idx < len(self.cart):
            # Check stock limit when increasing
            if delta > 0:
                cart_item = self.cart[idx]
                product = next((p for p in self.products if str(p["_id"]) == str(cart_item["_id"])), None)
                if product and cart_item["quantity"] >= product.get("quantity", 0):
                    error(f"Cannot add more — only {product.get('quantity', 0)} in stock!")
                    return
            self.cart[idx]["quantity"] += delta
            if self.cart[idx]["quantity"] <= 0:
                self.cart.pop(idx)
            self._refresh_cart()

    def _remove_from_cart(self):
        selected = self.cart_tree.focus()
        if not selected:
            return

        idx = int(selected)
        if 0 <= idx < len(self.cart):
            self.cart.pop(idx)
            self._refresh_cart()

    def _clear_cart(self):
        self.cart.clear()
        self._refresh_cart()

    def _refresh_cart(self):
        """Rebuild the cart table and update the total."""
        self.cart_tree.delete(*self.cart_tree.get_children())
        total = 0

        for i, item in enumerate(self.cart):
            item_total = item["price"] * item["quantity"]
            total += item_total
            self.cart_tree.insert(
                "", "end", iid=str(i),
                values=(
                    item["name"],
                    item["quantity"],
                    f"{item['price']:,.0f}",
                    f"{item_total:,.0f}",
                ),
            )

        self.total_label.configure(text=f"Total:  {total:,.0f}  DZD")

    def _get_total(self):
        return sum(item["price"] * item["quantity"] for item in self.cart)

    # ══════════════════════════════════════
    #  CHECKOUT
    # ══════════════════════════════════════

    def _checkout(self):
        if not self.cart:
            error("Cart is empty!")
            return

        total = self._get_total()

        # ── VALIDATE CASH *BEFORE* processing the sale ──
        if self.payment_type.get() == "cash":
            try:
                cash = float(self.cash_entry.get())
                if cash < total:
                    error(f"Not enough cash! Need {total:,.0f} DZD")
                    return
                change = cash - total
            except ValueError:
                error("Enter a valid cash amount")
                return

        # ── Process sale (deduct stock, save, generate receipt) ──
        total_result, filepath = SaleController.process_sale(self.cart)

        # Show change for cash payments
        if self.payment_type.get() == "cash":
            self.change_label.configure(
                text=f"Change: {change:,.0f} DZD",
                text_color=COLORS["success"],
            )

        success(
            f"✅ Payment successful ({self.payment_type.get()})\n"
            f"Total: {total_result:,.0f} DZD\n"
            f"Receipt saved!"
        )

        # Refresh everything
        self.products = ProductController.get_products()
        self._load_products()
        self.cart.clear()
        self._refresh_cart()
        self.cash_entry.delete(0, "end")