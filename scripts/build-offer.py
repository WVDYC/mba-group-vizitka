import json,shutil
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT,TA_RIGHT

root=Path(__file__).resolve().parents[1];out=root/'dist/assets/mba-group-commercial-offer.pdf'
config=json.loads((root/'dist/company.json').read_text())
items=json.loads((root/'dist/catalog.json').read_text())
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold')
ink=colors.HexColor('#20251b');gray=colors.HexColor('#626956');yellow=colors.HexColor('#e6f557');line=colors.HexColor('#e0e4d9')
style=ParagraphStyle('body',fontName='Arial',fontSize=9.5,leading=13,textColor=ink)
small=ParagraphStyle('small',parent=style,fontSize=8.5,leading=12,textColor=gray)
bold=ParagraphStyle('bold',parent=style,fontName='Arial-Bold')
white=ParagraphStyle('white',parent=style,fontName='Arial-Bold',textColor=colors.white,fontSize=8)
def para(text,kind=style):return Paragraph(text,kind)
def price(item):
 if item.get('rates'):
  vals=[]
  for period,value in item['rates'].items():
   vals.append(('От месяца - договорная' if period=='month' and value is None else 'По запросу' if value is None else f"{value:,}".replace(',',' ')+' тг / '+{'hour':'час','day':'день','month':'месяц'}[period]))
  return '<br/>'.join(vals)
 if item['price'] is None:return 'По запросу'
 return f"{item['price']:,}".replace(',',' ')+' тг / '+{'hour':'час','day':'день','month':'месяц'}[item['period']]+('<br/><font color="#626956">Доставка включена</font>' if item.get('deliveryIncluded') else '')
specs={'zoomlion':'Грузоподъёмность до 25 т','loader2':'Ковш 2 м³','loader3':'Ковш 3 м³','cat330':'Гусеничный экскаватор','isuzu':'Высота подъёма до 14 м','mitsubishi':'Высота подъёма до 14 м','spider':'Кран с люлькой','compressor':'2 отбойных молотка'}
out.parent.mkdir(exist_ok=True)
c=canvas.Canvas(str(out),pagesize=(595.276,841.89))
c.setTitle('Коммерческое предложение - MBA Group')
c.setAuthor('MBA Group')
c.setFillColor(ink);c.rect(0,736,596,106,fill=1,stroke=0)
c.setFillColor(yellow);c.rect(36,771,46,40,fill=1,stroke=0)
c.setFillColor(ink);c.setFont('Arial-Bold',26);c.drawString(46,780,'M')
c.setFillColor(colors.white);c.setFont('Arial-Bold',21);c.drawString(95,792,'MBA GROUP')
c.setFillColor(colors.HexColor('#c5cdba'));c.setFont('Arial',9);c.drawString(96,774,'АРЕНДА СПЕЦТЕХНИКИ | АСТАНА И ОБЛАСТЬ')
c.setFillColor(ink);c.setFont('Arial-Bold',23);c.drawString(36,694,'Коммерческое предложение')
c.setFillColor(gray);c.setFont('Arial',9);c.drawString(36,675,'ТОО «MBA Group»  |  Тарифы обновлены 15 ноября 2026')
p=para('Техника с операторами для строительных, монтажных, погрузочных и дорожных работ. Подберём комплект под задачу и согласуем условия аренды.')
w,h=p.wrap(523,60);p.drawOn(c,36,646-h)
rows=[[para('ТЕХНИКА',white),para('ХАРАКТЕРИСТИКА',white),para('ТАРИФ',white)]]
for item in items:
 rows.append([para(escape(item['name']),bold),para(escape(specs[item['id']]),small),para(price(item),style)])
table=Table(rows,colWidths=[202,143,178],rowHeights=[29]+[42]*8)
table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),ink),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f1f4e9'),colors.white]),('LINEBELOW',(0,1),(-1,-1),.5,line)]))
w,h=table.wrap(523,500);table.drawOn(c,36,604-h)
y=604-h-26
c.setFillColor(ink);c.setFont('Arial-Bold',11);c.drawString(36,y,'Условия аренды')
conditions=['Работаем по договору с НДС и без. Наличие и итоговые условия подтверждает менеджер.','Компрессор: 60 000 тг в день, доставка включена. Подачу другой техники согласуем отдельно.','Для расчёта сообщите технику, количество, срок аренды, адрес и вид работ.']
for text in conditions:
 p=para(text,small);w,h=p.wrap(523,45);y-=h+9;p.drawOn(c,36,y)
c.setStrokeColor(line);c.line(36,113,559,113)
c.setFillColor(ink);c.setFont('Arial-Bold',15);c.drawString(36,87,config['phone'])
c.linkURL('https://wa.me/'+config['whatsapp'],(36,83,230,103),relative=0,thickness=0)
c.setFont('Arial',9);c.drawString(36,69,'Телефон / WhatsApp')
if config.get('email'):
 c.setFillColor(ink);c.setFont('Arial',10);c.drawRightString(559,91,config['email'])
 c.linkURL('mailto:'+config['email'],(300,86,559,101),relative=0,thickness=0)
c.setFillColor(gray);c.setFont('Arial',8);c.drawRightString(559,69,'wvdyc.github.io/mba-group-vizitka')
c.linkURL('https://wvdyc.github.io/mba-group-vizitka/',(300,65,559,80),relative=0,thickness=0)
c.setFont('Arial',7.5);c.drawString(36,36,'Стоимость зависит от согласованного объёма работ. Подтвердите актуальность предложения у менеджера.')
c.showPage();c.save()
target=root/'dist/assets/mba-group-commercial-offer.pdf';shutil.copy2(out,target) if out.resolve()!=target.resolve() else None
print(out.resolve())
