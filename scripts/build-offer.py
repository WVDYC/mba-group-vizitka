import json
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

root=Path(__file__).resolve().parents[1]
out=root/'dist/assets/mba-group-commercial-offer.pdf'
config=json.loads((root/'dist/company.json').read_text())
items=json.loads((root/'dist/catalog.json').read_text())
for name,file in [('Arial','Arial.ttf'),('Arial-Bold','Arial Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold')
ink=colors.HexColor('#20251b');gray=colors.HexColor('#626956');yellow=colors.HexColor('#e6f557');line=colors.HexColor('#dce1d3');paper=colors.HexColor('#f4f6ef')
body=ParagraphStyle('body',fontName='Arial',fontSize=9,leading=12,textColor=ink)
small=ParagraphStyle('small',parent=body,fontSize=8,leading=11,textColor=gray)
title=ParagraphStyle('title',parent=body,fontName='Arial-Bold',fontSize=12,leading=15)
rate=ParagraphStyle('rate',parent=title)
specs={'zoomlion':'Грузоподъёмность до 25 т','loader2':'Фронтальный погрузчик · ковш 2 м³','loader3':'Фронтальный погрузчик · ковш 3 м³','cat330':'Гусеничный экскаватор · земляные работы','isuzu':'Высота подъёма до 14 м','mitsubishi':'Высота подъёма до 14 м','spider':'Гусеничный мини-кран с люлькой','compressor':'Компрессор + 2 отбойных молотка'}
c=canvas.Canvas(str(out),pagesize=(595.276,841.89))
c.setTitle('Коммерческое предложение с фотографиями - MBA Group');c.setAuthor('MBA Group')
def p(text,x,top,w=523,style=body):
 para=Paragraph(text,style);_,h=para.wrap(w,200);para.drawOn(c,x,top-h);return h
def text(value,x,y,size=9,color=ink,bold=False,right=False):
 c.setFillColor(color);c.setFont('Arial-Bold' if bold else 'Arial',size)
 (c.drawRightString if right else c.drawString)(x,y,value)
def photo(item,x,y,w,h):
 path=root/'dist'/item['image']
 with Image.open(path) as im: iw,ih=im.size
 c.setFillColor(colors.white);c.rect(x,y,w,h,fill=1,stroke=0)
 if item.get('realPhoto'):
  scale=max(w/iw,h/ih);dw,dh=iw*scale,ih*scale
  c.saveState();clip=c.beginPath();clip.rect(x,y,w,h);c.clipPath(clip,stroke=0,fill=0)
  c.drawImage(str(path),x+(w-dw)/2,y-(dh-h)*.76,width=dw,height=dh,mask='auto');c.restoreState()
 else:
  scale=min((w-18)/iw,(h-15)/ih);dw,dh=iw*scale,ih*scale
  c.drawImage(str(path),x+(w-dw)/2,y+(h-dh)/2,width=dw,height=dh,mask='auto')
def card(item,x,top,w=253.5,h=224):
 bottom=top-h;c.setFillColor(paper);c.setStrokeColor(line);c.setLineWidth(.6);c.rect(x,bottom,w,h,fill=1,stroke=1)
 photo(item,x+1,top-111,w-2,110)
 actual=item.get('realPhoto');label='ФОТО MBA GROUP' if actual else 'ИЛЛЮСТРАТИВНОЕ ФОТО'
 c.setFillColor(ink);c.rect(x+9,top-105,89 if actual else 124,14,fill=1,stroke=0);text(label,x+15,top-100,6.5,colors.white)
 used=p(escape(item['name']),x+12,top-125,w-24,title)
 p(escape(specs[item['id']]),x+12,top-131-used,w-24,small)
 main='По запросу' if item['price'] is None else f"{item['price']:,}".replace(',',' ')+' тг / '+{'hour':'час','day':'день','month':'месяц'}[item['period']]
 extra='Доставка включена' if item.get('deliveryIncluded') else ''
 if item.get('rates',{}).get('month',0) is None:extra='От месяца - договорная цена'
 p(escape(main),x+12,bottom+42,w-24,rate)
 if extra:p(escape(extra),x+12,bottom+23,w-24,small)
def header(page):
 c.setFillColor(ink);c.rect(0,764,596,78,fill=1,stroke=0)
 c.setFillColor(yellow);c.rect(36,785,36,35,fill=1,stroke=0);text('M',44,793,22,ink,True)
 text('MBA GROUP',86,803,20,colors.white,True)
 text('АРЕНДА СПЕЦТЕХНИКИ | АСТАНА И ОБЛАСТЬ',87,786,8,colors.HexColor('#c5cdba'))
 text(f'{page} / 2',559,803,8,colors.white,right=True)
 text('Коммерческое предложение',36,731,22,ink,True)
 text('ТОО «MBA Group» | Тарифы обновлены 15 ноября 2026',36,711,9,gray)
 text('Краны, погрузчики и экскаватор' if page==1 else 'Автовышки, мини-кран и компрессор',36,692,9,gray)
def footer(page):
 text('Условия аренды',36,188,10,ink,True)
 conditions='Техника с операторами. Работаем по договору с НДС и без. Наличие, подачу и итоговые условия подтверждает менеджер. Для заявки укажите технику, количество, срок и адрес объекта.' if page==1 else 'Компрессор: доставка включена в 60 000 тг за день. Подачу другой техники согласуем отдельно. Нагрузку и рабочую высоту люльки CS-4000 уточняйте под задачу.'
 p(conditions,36,177,523,small)
 c.setStrokeColor(line);c.line(36,132,559,132)
 text(config['phone'],36,108,14,ink,True);c.linkURL('https://wa.me/'+config['whatsapp'],(36,103,240,121),thickness=0)
 text('Телефон / WhatsApp',36,93,8,gray)
 if config.get('email'):
  text(config['email'],559,110,10,ink,right=True);c.linkURL('mailto:'+config['email'],(310,105,559,121),thickness=0)
 text('wvdyc.github.io/mba-group-vizitka',559,93,8,gray,right=True)
 c.linkURL('https://wvdyc.github.io/mba-group-vizitka/',(310,88,559,101),thickness=0)
 p('Фото CS-4000 предоставлено MBA Group. Остальные фотографии иллюстративные.',36,65,523,small)
 p('Подтвердите актуальность тарифов и комплектацию у менеджера перед заказом.',36,48,523,small)
for page in (1,2):
 header(page)
 for pos,item in enumerate(items[(page-1)*4:page*4]):card(item,36+(pos%2)*269.5,679-(pos//2)*240)
 footer(page);c.showPage()
c.save();print(out.resolve())
