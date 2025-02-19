from django.db.models import Sum, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Properties, Booking

@api_view(["GET"])
def analytics(request, user_id):
    # Get properties owned by the user
    user_properties = Properties.objects.filter(host_id=user_id)

    # Count of properties owned by the user
    properties_count = user_properties.count()

    # Get only bookings related to the user's properties
    user_property_ids = user_properties.values_list("property_id", flat=True)  # Get property IDs
    user_bookings = Booking.objects.filter(property_id__in=user_property_ids)

    # Sum of booking prices for the user's properties
    total_booking_price = user_bookings.aggregate(total_price=Sum("price"))["total_price"] or 0

    # Count of each property's occurrence in bookings
    property_booking_counts = (
        user_bookings.values("property")
        .annotate(bookings_count=Count("property_id"))
        .order_by("-bookings_count")
    )

    # Formatting property booking counts
    formatted_property_counts = {
        entry["property"]: entry["bookings_count"] for entry in property_booking_counts
    }

    return Response(
        {
            "properties": properties_count,
            "earnings": total_booking_price,
            "guests": formatted_property_counts,
        },
        status=status.HTTP_200_OK,
    )
