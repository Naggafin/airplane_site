from django.shortcuts import render


def index(request):
	context = {
		"page_title": "Home 1",
		"preloader": "preloader-1",
		"header": "header-1",
		"footer": "footer-1",
	}
	return render(request, "pixio/index.html", context)


def index_2(request):
	context = {
		"page_title": "Home 2",
		"preloader": "preloader-2",
		"header": "header-2",
		"footer": "footer-2",
	}
	return render(request, "pixio/index-2.html", context)


def index_3(request):
	context = {
		"page_title": "Home 3",
		"preloader": "preloader-3",
		"header": "header-1",
		"footer": "footer-1",
	}
	return render(request, "pixio/index-3.html", context)


def w3menu(request):
	context = {"page_title": "W3menu"}
	return render(request, "pixio/w3menu.html", context)


def shop_standard(request):
	context = {"page_title": "Shop Standard"}
	return render(request, "pixio/shop-standard.html", context)


def shop_list(request):
	context = {"page_title": "Shop List"}
	return render(request, "pixio/shop-list.html", context)


def shop_with_category(request):
	context = {"page_title": "Shop With Category"}
	return render(request, "pixio/shop-with-category.html", context)


def shop_filters_top_bar(request):
	context = {"page_title": "Shop Filters Top"}
	return render(request, "pixio/shop-filters-top-bar.html", context)


def shop_sidebar(request):
	context = {"page_title": "Shop Sidebar"}
	return render(request, "pixio/shop-sidebar.html", context)


def shop_style_1(request):
	context = {"page_title": "Shop Style 1"}
	return render(request, "pixio/shop-style-1.html", context)


def shop_style_2(request):
	context = {"page_title": "Shop Style 2"}
	return render(request, "pixio/shop-style-2.html", context)


def product_default(request):
	context = {"page_title": "Product Default"}
	return render(request, "pixio/product-default.html", context)


def product_thumbnail(request):
	context = {"page_title": "Product Thumbnail"}
	return render(request, "pixio/product-thumbnail.html", context)


def product_grid_media(request):
	context = {"page_title": "Product Grid Media"}
	return render(request, "pixio/product-grid-media.html", context)


def product_carousel(request):
	context = {"page_title": "Product Carousel"}
	return render(request, "pixio/product-carousel.html", context)


def product_full_width(request):
	context = {"page_title": "Product Full Width"}
	return render(request, "pixio/product-full-width.html", context)


def shop_wishlist(request):
	context = {"page_title": "Shop Wishlist"}
	return render(request, "pixio/shop-wishlist.html", context)


def shop_cart(request):
	context = {"page_title": "Shop Cart"}
	return render(request, "pixio/shop-cart.html", context)


def shop_checkout(request):
	context = {"page_title": "Shop Checkout"}
	return render(request, "pixio/shop-checkout.html", context)


def shop_compare(request):
	context = {
		"page_title": "Shop Compare",
		"preloader": "preloader-1",
		"header": "header-4",
		"footer": "footer-1",
	}
	return render(request, "pixio/shop-compare.html", context)


def shop_order_tracking(request):
	context = {"page_title": "Shop Order Tracking"}
	return render(request, "pixio/shop-order-tracking.html", context)


def shop_my_account(request):
	context = {"page_title": "Shop My Account"}
	return render(request, "pixio/shop-my-account.html", context)


def shop_registration(request):
	context = {"page_title": "Shop Registration"}
	return render(request, "pixio/shop-registration.html", context)


def blog_dark_2_column(request):
	context = {"page_title": "Blog Dark 2 Column"}
	return render(request, "pixio/blog-dark-2-column.html", context)


def blog_dark_2_column_sidebar(request):
	context = {"page_title": "Blog Dark 2 Column Sidebar"}
	return render(request, "pixio/blog-dark-2-column-sidebar.html", context)


def blog_dark_3_column(request):
	context = {"page_title": "Blog Dark 3 Column"}
	return render(request, "pixio/blog-dark-3-column.html", context)


def blog_dark_half_image(request):
	context = {"page_title": "Blog Dark Half Image"}
	return render(request, "pixio/blog-dark-half-image.html", context)


def blog_light_2_column(request):
	context = {"page_title": "Blog Light 2 Column"}
	return render(request, "pixio/blog-light-2-column.html", context)


def blog_light_2_column_sidebar(request):
	context = {"page_title": "Blog Light 2 Column Sidebar"}
	return render(request, "pixio/blog-light-2-column-sidebar.html", context)


def blog_light_half_image(request):
	context = {"page_title": "Blog Light Half Image"}
	return render(request, "pixio/blog-light-half-image.html", context)


def blog_exclusive(request):
	context = {"page_title": "Blog Exclusive"}
	return render(request, "pixio/blog-exclusive.html", context)


def blog_left_sidebar(request):
	context = {"page_title": "Blog Left Sidebar"}
	return render(request, "pixio/blog-left-sidebar.html", context)


def blog_right_sidebar(request):
	context = {"page_title": "Blog Right Sidebar"}
	return render(request, "pixio/blog-right-sidebar.html", context)


def blog_both_sidebar(request):
	context = {"page_title": "Blog Both Sidebar"}
	return render(request, "pixio/blog-both-sidebar.html", context)


def blog_wide_sidebar(request):
	context = {"page_title": "Blog Wide Sidebar"}
	return render(request, "pixio/blog-wide-sidebar.html", context)


def blog_archive(request):
	context = {"page_title": "Blog Archive"}
	return render(request, "pixio/blog-archive.html", context)


def blog_author(request):
	context = {"page_title": "Blog Author"}
	return render(request, "pixio/blog-author.html", context)


def blog_category(request):
	context = {"page_title": "Blog Category"}
	return render(request, "pixio/blog-category.html", context)


def blog_tag(request):
	context = {"page_title": "Blog Tag"}
	return render(request, "pixio/blog-tag.html", context)


def post_standard(request):
	context = {"page_title": "Post Standard"}
	return render(request, "pixio/post-standard.html", context)


def post_left_sidebar(request):
	context = {"page_title": "Post Left Sidebar"}
	return render(request, "pixio/post-left-sidebar.html", context)


def post_header_image(request):
	context = {
		"page_title": "Post Header Image",
		"preloader": "preloader-1",
		"header": "header-4",
		"footer": "footer",
	}
	return render(request, "pixio/post-header-image.html", context)


def post_slide_show(request):
	context = {"page_title": "Post Slide Show"}
	return render(request, "pixio/post-slide-show.html", context)


def post_side_image(request):
	context = {"page_title": "Post Side Image"}
	return render(request, "pixio/post-side-image.html", context)


def post_gallery(request):
	context = {"page_title": "Post Gallery"}
	return render(request, "pixio/post-gallery.html", context)


def post_gallery_alternative(request):
	context = {"page_title": "Post Gallery Alternative"}
	return render(request, "pixio/post-gallery-alternative.html", context)


def post_open_gutenberg(request):
	context = {"page_title": "Post Open Gutenberg"}
	return render(request, "pixio/post-open-gutenberg.html", context)


def post_link(request):
	context = {"page_title": "Post Link"}
	return render(request, "pixio/post-link.html", context)


def post_audio(request):
	context = {"page_title": "Post Audio"}
	return render(request, "pixio/post-audio.html", context)


def post_video(request):
	context = {"page_title": "Post Video"}
	return render(request, "pixio/post-video.html", context)


def portfolio_tiles(request):
	context = {"page_title": "Portfolio Tiles"}
	return render(request, "pixio/portfolio-tiles.html", context)


def collage_style_1(request):
	context = {"page_title": "Collage Style 1"}
	return render(request, "pixio/collage-style-1.html", context)


def collage_style_2(request):
	context = {"page_title": "Collage Style 2"}
	return render(request, "pixio/collage-style-2.html", context)


def masonry_grid(request):
	context = {"page_title": "Masonry Grid"}
	return render(request, "pixio/masonry-grid.html", context)


def cobble_style_1(request):
	context = {"page_title": "Cobble Style 1"}
	return render(request, "pixio/cobble-style-1.html", context)


def cobble_style_2(request):
	context = {"page_title": "Cobble Style 2"}
	return render(request, "pixio/cobble-style-2.html", context)


def portfolio_thumbs_slider(request):
	context = {"page_title": "Portfolio Thumbs Slider"}
	return render(request, "pixio/portfolio-thumbs-slider.html", context)


def portfolio_film_strip(request):
	context = {"page_title": "Portfolio Film Strip"}
	return render(request, "pixio/portfolio-film-strip.html", context)


def carousel_showcase(request):
	context = {"page_title": "Carousel Showcase"}
	return render(request, "pixio/carousel-showcase.html", context)


def portfolio_split_slider(request):
	context = {"page_title": "portfolio Split Slider"}
	return render(request, "pixio/portfolio-split-slider.html", context)


def portfolio_details_1(request):
	context = {"page_title": "Portfolio Details 1"}
	return render(request, "pixio/portfolio-details-1.html", context)


def portfolio_details_2(request):
	context = {"page_title": "Portfolio Details 2"}
	return render(request, "pixio/portfolio-details-2.html", context)


def portfolio_details_3(request):
	context = {"page_title": "Portfolio Details 3"}
	return render(request, "pixio/portfolio-details-3.html", context)


def portfolio_details_4(request):
	context = {"page_title": "Portfolio Details 4"}
	return render(request, "pixio/portfolio-details-4.html", context)


def portfolio_details_5(request):
	context = {"page_title": "Portfolio Details 5"}
	return render(request, "pixio/portfolio-details-5.html", context)


def about_us(request):
	context = {"page_title": "About Us"}
	return render(request, "pixio/about-us.html", context)


def about_me(request):
	context = {"page_title": "About Me"}
	return render(request, "pixio/about-me.html", context)


def pricing_table(request):
	context = {"page_title": "Pricing Table"}
	return render(request, "pixio/pricing-table.html", context)


def our_gift_vouchers(request):
	context = {"page_title": "Our Gift Vouchers"}
	return render(request, "pixio/our-gift-vouchers.html", context)


def what_we_do(request):
	context = {"page_title": "What We Do"}
	return render(request, "pixio/what-we-do.html", context)


def faqs_1(request):
	context = {"page_title": "Faq 1"}
	return render(request, "pixio/faqs-1.html", context)


def faqs_2(request):
	context = {"page_title": "Faq 2"}
	return render(request, "pixio/faqs-2.html", context)


def our_team(request):
	context = {"page_title": "Our Team"}
	return render(request, "pixio/our-team.html", context)


def contact_us_1(request):
	context = {"page_title": "Contact Us 1"}
	return render(request, "pixio/contact-us-1.html", context)


def contact_us_2(request):
	context = {"page_title": "Contact Us 2"}
	return render(request, "pixio/contact-us-2.html", context)


def contact_us_3(request):
	context = {"page_title": "Contact Us 3"}
	return render(request, "pixio/contact-us-3.html", context)


def error_404(request):
	context = {"page_title": "Error 404"}
	return render(request, "404.html", context)


def error_2(request):
	context = {"page_title": "Error 404 2"}
	return render(request, "pixio/error-2.html", context)


def coming_soon(request):
	context = {"page_title": "Coming Soon"}
	return render(request, "pixio/coming-soon.html", context)


def under_construction(request):
	context = {"page_title": "Under Construction"}
	return render(request, "pixio/under-construction.html", context)


def banner_with_bg_color(request):
	context = {"page_title": "Banner With Bg-Color", "banner": "banner-with-bg-color"}
	return render(request, "pixio/banner-with-bg-color.html", context)


def banner_with_image(request):
	context = {"page_title": "Banner With Image", "banner": "banner-with-image"}
	return render(request, "pixio/banner-with-image.html", context)


def banner_with_video(request):
	context = {"page_title": "Banner With Video", "banner": "banner-with-video"}
	return render(request, "pixio/banner-with-video.html", context)


def banner_with_kanbern(request):
	context = {"page_title": "Banner With Kanbern", "banner": "banner-with-kanbern"}
	return render(request, "pixio/banner-with-kanbern.html", context)


def banner_small(request):
	context = {"page_title": "Banner Small", "banner": "banner-small"}
	return render(request, "pixio/banner-small.html", context)


def banner_medium(request):
	context = {"page_title": "Banner Medium", "banner": "banner-medium"}
	return render(request, "pixio/banner-medium.html", context)


def banner_large(request):
	context = {"page_title": "Banner Large", "banner": "banner-large"}
	return render(request, "pixio/banner-large.html", context)


def header_style_1(request):
	context = {"page_title": "Header Style 1", "header": "header"}
	return render(request, "pixio/header-style-1.html", context)


def header_style_2(request):
	context = {"page_title": "Header Style 2", "header": "header-2"}
	return render(request, "pixio/header-style-2.html", context)


def header_style_3(request):
	context = {"page_title": "Header Style 3", "header": "header-3"}
	return render(request, "pixio/header-style-3.html", context)


def header_style_4(request):
	context = {"page_title": "Header Style 4", "header": "header-4"}
	return render(request, "pixio/header-style-4.html", context)


def header_style_5(request):
	context = {"page_title": "Header Style 5", "header": "header-5"}
	return render(request, "pixio/header-style-5.html", context)


def header_style_6(request):
	context = {"page_title": "Header Style 6", "header": "header-6"}
	return render(request, "pixio/header-style-6.html", context)


def header_style_7(request):
	context = {"page_title": "Header Style 7", "header": "header-7"}
	return render(request, "pixio/header-style-7.html", context)


def footer_style_1(request):
	context = {"page_title": "Footer Style 1", "footer": "footer"}
	return render(request, "pixio/footer-style-1.html", context)


def footer_style_2(request):
	context = {"page_title": "Footer Style 2", "footer": "footer-3"}
	return render(request, "pixio/footer-style-2.html", context)


def footer_style_3(request):
	context = {"page_title": "Footer Style 3", "footer": "footer-4"}
	return render(request, "pixio/footer-style-3.html", context)


def footer_style_4(request):
	context = {"page_title": "Footer Style 4", "footer": "footer-5"}
	return render(request, "pixio/footer-style-4.html", context)


def footer_style_5(request):
	context = {"page_title": "Footer Style 5", "footer": "footer-6"}
	return render(request, "pixio/footer-style-5.html", context)


def footer_style_6(request):
	context = {"page_title": "Footer Style 6", "footer": "footer-7"}
	return render(request, "pixio/footer-style-6.html", context)


def footer_style_7(request):
	context = {"page_title": "Footer Style 7", "footer": "footer-8"}
	return render(request, "pixio/footer-style-7.html", context)


def account_dashboard(request):
	context = {"page_title": "Dashboard"}
	return render(request, "pixio/account-dashboard.html", context)


def account_orders(request):
	context = {"page_title": "Orders"}
	return render(request, "pixio/account-orders.html", context)


def account_order_details(request):
	context = {"page_title": "Order Details"}
	return render(request, "pixio/account-order-details.html", context)


def account_order_confirmation(request):
	context = {"page_title": "Order Confirmation"}
	return render(request, "pixio/account-order-confirmation.html", context)


def account_downloads(request):
	context = {"page_title": "Account Downloads"}
	return render(request, "pixio/account-downloads.html", context)


def account_return_request(request):
	context = {"page_title": "Return Request"}
	return render(request, "pixio/account-return-request.html", context)


def account_return_request_detail(request):
	context = {"page_title": "Return Request Detail"}
	return render(request, "pixio/account-return-request-detail.html", context)


def account_refund_request_confirmed(request):
	context = {"page_title": "Refund Requests Confirmed"}
	return render(request, "pixio/account-refund-request-confirmed.html", context)


def account_profile(request):
	context = {"page_title": "Account Profile"}
	return render(request, "pixio/account-profile.html", context)


def account_address(request):
	context = {"page_title": "Account Address"}
	return render(request, "pixio/account-address.html", context)


def account_shipping_methods(request):
	context = {"page_title": "Account Shipping Methods"}
	return render(request, "pixio/account-shipping-methods.html", context)


def account_payment_methods(request):
	context = {"page_title": "Account Payment Methods"}
	return render(request, "pixio/account-payment-methods.html", context)


def account_review(request):
	context = {"page_title": "Account Review"}
	return render(request, "pixio/account-review.html", context)


def account_billing_address(request):
	context = {"page_title": "Account Billing Address"}
	return render(request, "pixio/account-billing-address.html", context)


def account_shipping_address(request):
	context = {"page_title": "Account Shipping Address"}
	return render(request, "pixio/account-shipping-address.html", context)


def account_cancellation_requests(request):
	context = {"page_title": "Account Cancellation Requests"}
	return render(request, "pixio/account-cancellation-requests.html", context)
