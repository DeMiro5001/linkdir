from django.db import models
from django.utils.html import mark_safe
import re
from colorfield.fields import ColorField

class LinkCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    color = ColorField(format="hexa")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Link(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    category = models.ForeignKey('LinkCategory', on_delete=models.CASCADE, related_name='links')
    icon_class = models.CharField(
        max_length=100, 
        default='fas fa-link',
        help_text=mark_safe(
            'Font Awesome icon class. '
            '<a href="https://fontawesome.com/icons?d=gallery&m=free" target="_blank">Browse icons</a>'
        )
    )
    order = models.IntegerField(default=0)
    authenticated_only = models.BooleanField(
        default=False,
        help_text='Only show this link to authenticated users'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category__order', 'order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Clean the icon_class field before saving
        if self.icon_class:
            self.icon_class = self.clean_icon_class(self.icon_class)
        super().save(*args, **kwargs)
    
    def clean_icon_class(self, icon_string):
        """
        Extract just the Font Awesome classes from HTML snippet or return as-is
        """
        if not icon_string:
            return 'fas fa-link'
            
        # Pattern to match <i class="..."></i> format
        pattern = r'<i\s+class="([^"]+)"\s*></i>'
        match = re.search(pattern, icon_string.strip())
        
        if match:
            # Extract the class from the HTML snippet
            return match.group(1)
        else:
            # Return as-is if it's already just the classes
            return icon_string.strip()
