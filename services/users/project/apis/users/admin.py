from flask_admin.contrib.sqla import ModelView


class UsersAdminView(ModelView):
    column_searchable_list = ("email",)
    column_editable_list = ("email", "created_date")
    column_filters = ("email",)
    column_sortable_list = ("email", "active", "created_date")
    column_default_sort = ("created_date", True)
