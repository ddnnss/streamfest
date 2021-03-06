from django.http import HttpResponse
from django.shortcuts import render,HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from speaker.models import *
from .models import *
from speaker.models import Ticket,Order
from platron.request.request_builders.init_payment_builder import InitPaymentBuilder
from platron.request.clients.post_client import PostClient
from platron.sdk_exception import SdkException
import settings
import xml.etree.ElementTree as ET


def index(request):
    set= Settings.objects.first()
    allSpeakers = Speaker.objects.filter(isAtHome=True).order_by('orderPP')
    indexactive = 'current'
    allBanners = Banner.objects.filter(is_active=True).order_by('order')
    oneDayTicket = Ticket.objects.get(isDefaultOneDayTicket=True)
    twoDayTicket = Ticket.objects.get(isDefaultTwoDayTicket=True)
    posts = Post.objects.filter(isAtHome=True)
    items = range(1,32)
    sponsors = Sponsor.objects.all()
    feedbacks = Feedback.objects.filter(is_active=True)
    content_table = StaticPage.objects.first()
    index_text_about = content_table.index_about_text
    index_img_about = content_table.index_about_image.url

    return render(request, 'staticPages/index.html', locals())

def faq(request):
    faqactive = 'current'
    faqs = list(Faq.objects.all())
    left_faqs = faqs[0::2]
    right_faqs = faqs[1::2]
    return render(request, 'staticPages/faq.html', locals())

def apply(request):
    faqs = list(StandStar.objects.all())
    left_faqs = faqs[0::2]
    right_faqs = faqs[1::2]
    applytactive = 'current'
    content_table = StaticPage.objects.first()
    apply_text = content_table.apply_text
    return render(request, 'staticPages/apply.html', locals())

def contacts(request):
    contactactive = 'current'
    return render(request, 'staticPages/contacts.html', locals())


def order(request, pass_type):
    passArticle = pass_type
    day = pass_type.split('_')[1]
    streamer = pass_type.split('_')[0]
    return render(request, 'staticPages/order.html', locals())

def new_order(request):
    if request.POST:
        print(request.POST)
        customerFio = request.POST.get('username')
        customerPhone = request.POST.get('phone')
        customerEmail = request.POST.get('email')
        passArticle = request.POST.get('passArticle')
        ticket = Ticket.objects.get(article=passArticle)

        streamerNickNameSlug = None
        tiketType = None

        try:
            tiketType = passArticle.split('_')[1]
            streamerNickNameSlug = passArticle.split('_')[0]
            print('tiketType1=', tiketType)
        except:
            tiketType=passArticle
            print('tiketType2=', tiketType)
        print('streamer=',streamerNickNameSlug)

        price = Ticket.objects.get(article=tiketType).price
        if streamerNickNameSlug:
            streamer = Speaker.objects.get(nickNameSlug=streamerNickNameSlug)
            newOrder = Order.objects.create(streamer=streamer,
                             ticket=ticket,
                             customerFio=customerFio,
                             customerEmail=customerEmail,
                             customerPhone=customerPhone,
                             price=price)
        else:
            newOrder = Order.objects.create(ticket=ticket,
                                 customerFio=customerFio,
                                 customerEmail=customerEmail,
                                 customerPhone=customerPhone,
                                 price=price)

        client = PostClient(settings.MERCHANT_ID, settings.SECRET_KEY)
        request = InitPaymentBuilder(price, ticket.__str__())

        try:
            request.add_success_url(f'{settings.SUCCESS_URL}{newOrder.id}/')
            response = client.request(request)
            print(response)
            responseXml = ET.fromstring(response)
            pg_redirect_url = responseXml.find('pg_redirect_url')
            print(pg_redirect_url.text)
            return HttpResponseRedirect(pg_redirect_url.text)

        except SdkException as msg:
            print(msg)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def order_complete(request, order_id):
    if request.POST:
        order = Order.objects.get(id=order_id)
        order.ticket.sells += 1
        order.ticket.save()
        order.isPayed = True
        order.save()
        return render(request, 'staticPages/order_complete.html', locals())
    else:
        return HttpResponse(status=404)


def posts(request):
    allPosts = Post.objects.all()
    return render(request, 'staticPages/posts.html', locals())


def post(request, slug):
    post =  get_object_or_404(Post, nameSlug=slug)
    allPosts = Post.objects.all()[:3]
    return render(request, 'staticPages/post.html', locals())

def about(request):
    activityactive = 'current'
    activities = Activity.objects.all()
    return render(request, 'staticPages/about.html', locals())

def callback(request):
    if request.POST:
        print(request.POST)
        Callback.objects.create(name=request.POST.get('username'),
                                email=request.POST.get('email'),
                                text=request.POST.get('message'))
        messages.success(request, 'Спасибо, форма успешно отправлена')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def check_order(request, qr):
    order = get_object_or_404(Order, codeQR=qr)
    print (order)
    return render(request, 'staticPages/check_order.html', locals())



def speaker(request,nickNameSlug):
    curSpeaker = get_object_or_404(Speaker, nickNameSlug=nickNameSlug)
    streamersactive = 'current'
    oneDayTicket = Ticket.objects.get(isDefaultOneDayTicket=True)
    twoDayTicket = Ticket.objects.get(isDefaultTwoDayTicket=True)
    oneDayTicket_slug = f'{curSpeaker.nickNameSlug}_{oneDayTicket.article}'
    twoDayTicket_slug = f'{curSpeaker.nickNameSlug}_{twoDayTicket.article}'
    return render(request, 'speaker/speaker.html', locals())

def all_speakers(request):
    streamersactive = 'current'
    allSpeakers = Speaker.objects.all().order_by('orderPP')
    return render(request, 'speaker/speakers.html', locals())


def add_to_mail_subscribe(request):
    print(request.POST)
    MailSubscribe.objects.get_or_create(email=request.POST.get('email'))
    return HttpResponseRedirect('/')