from util.db.accounts import retrieve_account, update_xsrf_token, guest_username

def create_home_page_html(auth_token, visits):
    username = guest_username
    account = retrieve_account(auth_token)
    if account is not None:
        username = account.get("username")
    xsrf_token = update_xsrf_token(account)
    template = open("./public/home_page.html", "r").read()
    template = replace_conditional(template, account is not None, "{{startif-1}}", "{{endif-1}}", "")
    template = replace_conditional(template, account is None, "{{startif-2}}", "{{endif-2}}", "")
    template = replace_conditional(template, account is not None, "{{startif-3}}", "{{endif-3}}", "")
    template = template.replace("{{username}}", username)
    if xsrf_token != None:
        template = template.replace("{{xsrf_token}}", xsrf_token)
    template = template.replace("{{visits}}", str(visits))
    return template

def replace_conditional(template, boolean, start_tag, end_tag, replacement):
    if boolean:
        start_index = template.find(start_tag)
        end_index = template.find(end_tag) + len(end_tag)
        template = template[:start_index] + replacement + template[end_index:]
    template = template.replace(start_tag, "")
    template = template.replace(end_tag, "")
    return template