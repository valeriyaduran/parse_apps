import webbrowser


class HTMLHelper:
    filename = "business_apps.html"

    @classmethod
    def save_data_to_rows(cls, data):
        tbl = "<thead><tr><th>Business app name</th><th>Company name</th><th>Release year<th>Email</th></tr><thead>\n"
        with open(cls.filename, "w") as html_page:
            html_page.write("<table>")
            html_page.write(tbl)
            html_page.write("<tbody>")
            for row in data:
                html_page.write("<tr><td>%s</td>" % row["business_app_name"])
                html_page.write("<td>%s</td>" % row["company_name"])
                html_page.write("<td>%s</td>" % row["release_year"])
                html_page.write("<td>%s</td></tr>" % row["email"])
            html_page.write("/<tbody>")
            html_page.write("</table>")
        HTMLHelper.display_data_on_web_page()

    @classmethod
    def display_data_on_web_page(cls):
        webbrowser.open(cls.filename)




