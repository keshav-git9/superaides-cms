from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='parse_shortcodes')
def parse_shortcodes(content):
    if not content:
        return ""

    # Example: [testimonial]
    content = re.sub(
        r'\[testimonial\]',
        '<div class="testimonial">This is a testimonial block.</div>',
        content
    )

    # Example: [gallery id=5]
    def render_gallery(match):
        gallery_id = match.group(1)
        return f'<div class="gallery">Gallery #{gallery_id} goes here.</div>'

    content = re.sub(
        r'\[gallery id=(\d+)\]',
        render_gallery,
        content
    )

    return mark_safe(content)
