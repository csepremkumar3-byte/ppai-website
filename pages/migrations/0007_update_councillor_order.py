from django.db import migrations

def update_councillor_orders(apps, schema_editor):
    ExecutiveMember = apps.get_model('pages', 'ExecutiveMember')
    
    # Target order requested:
    # 11: Dr. K Rameash
    # 12: Dr. J Stanley
    # 13: Dr. Alpesh Kumar Valjibhai Khanpara
    # 14: Dr. B S Gotyal
    # 15: Dr. D Sagar
    
    order_map = {
        'Dr. K Rameash': 11,
        'Dr. J Stanley': 12,
        'Dr. Alpesh Kumar Valjibhai Khanpara': 13,
        'Dr. B S Gotyal': 14,
        'Dr. D Sagar': 15,
    }
    
    for name, new_order in order_map.items():
        ExecutiveMember.objects.filter(name__icontains=name).update(order=new_order)

def reverse_orders(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_editorialboardmember_options_and_more'),
    ]

    operations = [
        migrations.RunPython(update_councillor_orders, reverse_orders),
    ]
