from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'description', 'quantity', 'unit_price', 'price']

class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = ['id', 'date', 'customer_name', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        invoice = Invoice.objects.create(**validated_data)
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        instance.date = validated_data.get('date', instance.date)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()

        existing_details = {d.id: d for d in instance.details.all()}
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id:
                detail = existing_details.pop(detail_id, None)
                if detail:
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
            else:
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        for detail in existing_details.values():
            detail.delete()

        return instance
