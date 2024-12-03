from django.shortcuts import render


def index(request):
	context = {
		"preloader": "preloader-1",
	}
	return render(request, "pixio/index.html", context)


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


def pricing_table(request):
	context = {"page_title": "Pricing Table"}
	return render(request, "pixio/pricing-table.html", context)


def our_gift_vouchers(request):
	context = {"page_title": "Our Gift Vouchers"}
	return render(request, "pixio/our-gift-vouchers.html", context)


def what_we_do(request):
	context = {"page_title": "What We Do"}
	return render(request, "pixio/what-we-do.html", context)


def faq(request):
	context = {"page_title": "Faq 2"}
	return render(request, "pixio/faq.html", context)


def our_team(request):
	context = {"page_title": "Our Team"}
	return render(request, "pixio/our-team.html", context)


def contact_us(request):
	context = {"page_title": "Contact Us 1"}
	return render(request, "pixio/contact-us.html", context)


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
