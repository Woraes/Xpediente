from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponseRedirect


class GeraPDF:
    
    def render_to_pdf(self, template_end, context_dict={}):
        template = get_template(template_end)
        html = template.render(context_dict)
        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode("")), result)
            return HttpResponseRedirect(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
            return None