from django.db import models
from django.contrib.auth.models import User


# Represents an inventory item 
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    managed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Log for changes made to inventory items, tracking reasons and responsible user
class InventoryLog(models.Model):
    CHANGE_REASON_CHOICES = [
        ('new-item', 'New Item'),
        ('restock', 'Restock'),
        ('rebrand', 'Rebrand'),
        ('sold', 'Sold'),
        ('damaged', 'Damaged'),
        ('unwanted', 'Unwanted'),
    ]

    item = models.ForeignKey('InventoryItem', on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    item_name = models.CharField(max_length=255, blank=True)
    change_type = models.CharField(max_length=20)
    change_reason = models.CharField(max_length=20, choices=CHANGE_REASON_CHOICES, default='new-item')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quantity_before = models.PositiveIntegerField()
    quantity_after = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.change_type} - {self.item.name} by {self.changed_by} ({self.change_reason})"