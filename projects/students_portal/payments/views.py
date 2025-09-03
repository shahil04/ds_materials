import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from courses.models import Course
from .models import Transaction
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount_paisa = int(course.price * 100)   # razorpay uses paise (int)
    razorpay_order = client.order.create({
        'amount': amount_paisa,
        'currency': 'INR',
        'receipt': f'course_{course.id}_user_{request.user.id}'
    })
    txn = Transaction.objects.create(
        user=request.user,
        course=course,
        amount=course.price,
        gateway_order_id=razorpay_order['id'],
        status='created'
    )
    return render(request, 'payments/checkout.html', {
        'course': course,
        'txn': txn,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount_paisa': amount_paisa,
    })
