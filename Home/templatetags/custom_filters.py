from django import template

register = template.Library()

@register.filter
def is_instance_of(obj, class_path):
    try:
        module_name, class_name = class_path.rsplit(".", 1)
        module = __import__(module_name, fromlist=[class_name])
        cls = getattr(module, class_name)
        return isinstance(obj, cls)
    except (ImportError, AttributeError):
        return False
