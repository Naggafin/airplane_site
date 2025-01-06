from django.shortcuts import render


def render_table_row(request, table_class, object):
	table = table_class(
		[object],
		row_attrs=table_class.Meta.row_attrs | {"hx-swap-oob": "true"},
		request=request,
	)
	return render(
		request, "django_tables2/partials/row_fragment.html", {"table": table}
	)
