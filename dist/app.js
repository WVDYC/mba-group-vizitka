const money = value => new Intl.NumberFormat('ru-RU').format(value) + ' ₸';
const wa = text => 'https://wa.me/77788275160?text=' + encodeURIComponent(text);
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const select = document.querySelector('#equipment'), quantity = document.querySelector('#quantity');
let catalog = [], filter = 'all';
function renderCards() {
 document.querySelector('#cards').innerHTML = catalog.filter(item => filter === 'all' || item.category === filter).map((item) => `<article class="card"><div class="card-art"><span class="category">${escapeHTML(item.label)}</span><img loading="lazy" src="${escapeHTML(item.image)}" alt="${escapeHTML(item.name)} — иллюстративное фото"><span class="art-number">${String(catalog.indexOf(item)+1).padStart(2,'0')}</span></div><div class="card-body"><h3>${escapeHTML(item.name)}</h3><p>${escapeHTML(item.description)}</p><div class="card-bottom"><span class="card-price">${item.price == null ? 'По запросу' : money(item.price)}<small>${item.price == null ? 'Уточните условия аренды' : item.period === 'day' ? 'за день' : 'за месяц'}</small></span><a href="${wa('Здравствуйте! Интересует аренда: '+item.name+'. Подскажите наличие и условия.') }" target="_blank" rel="noopener" aria-label="Обсудить аренду: ${escapeHTML(item.name)}">↗</a></div></div></article>`).join('');
 document.querySelectorAll('.card img').forEach(img => img.addEventListener('error', () => { img.src='assets/site-work.jpg'; img.alt='Иллюстрация строительной техники'; }, {once:true}));
}
function updateCalc() {
 const item=catalog.find(i=>i.id===select.value); if(!item) return;
 const qty=Number(quantity.value), valid=Number.isInteger(qty)&&qty>=1&&qty<=120;
 document.querySelector('#quantity-label').textContent=item.period==='day'?'Количество дней':'Количество месяцев';
 document.querySelector('#total').textContent=!valid?'Укажите срок от 1 до 120':item.price==null?'По запросу':money(item.price*qty);
}
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{filter=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button));});renderCards();}));
select.addEventListener('change',updateCalc); quantity.addEventListener('input',updateCalc);
for(const [id,delta] of [['minus',-1],['plus',1]]) document.querySelector('#'+id).addEventListener('click',()=>{quantity.value=Math.max(1,Math.min(120,(Number(quantity.value)||1)+delta));updateCalc();});
document.querySelector('#calc-form').addEventListener('submit',event=>{event.preventDefault();if(!quantity.reportValidity())return;const item=catalog.find(i=>i.id===select.value);if(!item)return;const text=`Здравствуйте! Нужна аренда спецтехники:\nТехника: ${item.name}\nСрок: ${quantity.value} ${item.period==='day'?'дн.':'мес.'}\nПредварительная стоимость: ${item.price==null?'по запросу':money(item.price*Number(quantity.value))}\nПодскажите наличие, условия подачи и итоговую стоимость.`;window.open(wa(text),'_blank','noopener');});
const menu=document.querySelector('.menu');menu.addEventListener('click',()=>{const open=document.querySelector('nav').classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>{document.querySelector('nav').classList.remove('open');menu.setAttribute('aria-expanded','false');}));
fetch('catalog.json').then(response=>{if(!response.ok)throw Error('catalog');return response.json();}).then(data=>{catalog=data;renderCards();select.innerHTML=catalog.map(i=>`<option value="${escapeHTML(i.id)}">${escapeHTML(i.name)}${i.id==='zoomlion'?' · 25 т':''}</option>`).join('');updateCalc();}).catch(()=>{document.querySelector('#cards').innerHTML='<p>Каталог временно недоступен. Позвоните <a href="tel:+77788275160">+7 778 827 51 60</a> — поможем подобрать технику.</p>';document.querySelector('#calc-form button[type=submit]').disabled=true;});
