// Plinth V2, header, reveal, counters, testimonials, FAQ, to-top, forms
document.addEventListener('DOMContentLoaded',()=>{
  const header=document.querySelector('.site-header');
  const toTop=document.getElementById('toTop');
  let pastFooter=false;
  const onScroll=()=>{
    const y=window.scrollY||0;
    if(header) header.classList.toggle('scrolled',y>10);
    if(toTop) toTop.classList.toggle('show',y>700&&!pastFooter);
  };
  const foot=document.querySelector('footer');
  if(foot&&'IntersectionObserver' in window){
    new IntersectionObserver(es=>{es.forEach(en=>{pastFooter=en.isIntersecting;onScroll();});},{threshold:.06}).observe(foot);
  }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  if(toTop) toTop.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));

  const t=document.querySelector('.mobile-toggle');
  const n=document.querySelector('nav.main');
  const hr=document.querySelector('.head-right');
  if(t&&n){t.addEventListener('click',()=>{n.classList.toggle('open');if(hr)hr.classList.toggle('open',n.classList.contains('open'));t.textContent=n.classList.contains('open')?'✕':'☰';t.setAttribute('aria-label',n.classList.contains('open')?'Close menu':'Open menu');});
    n.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{n.classList.remove('open');if(hr)hr.classList.remove('open');t.textContent='☰';}));
    window.addEventListener('resize',()=>{if(window.innerWidth>1120){n.classList.remove('open');if(hr)hr.classList.remove('open');t.textContent='☰';}});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&n.classList.contains('open')){n.classList.remove('open');if(hr)hr.classList.remove('open');t.textContent='☰';}});}

  // active nav
  try{
    const path=(location.pathname.split('/').pop()||'index.html').toLowerCase();
    document.querySelectorAll('nav.main a').forEach(a=>{
      const href=(a.getAttribute('href')||'').toLowerCase();
      if(href===path||(path===''&&href==='index.html')) a.classList.add('active');
    });
  }catch(e){}

  // hero video: pause offscreen to save battery/data
  const hv=document.querySelector('.hero-bg');
  if(hv && 'IntersectionObserver' in window){
    new IntersectionObserver((es)=>{es.forEach(en=>{
      if(en.isIntersecting){hv.play().catch(()=>{});}else{hv.pause();}
    });},{threshold:.05}).observe(hv);
  }

  // drifting thumbnails: only animate while visible
  const movers=document.querySelectorAll('.card, .guide');
  if(movers.length && 'IntersectionObserver' in window){
    const mio=new IntersectionObserver((entries)=>{
      entries.forEach(en=>{en.target.classList.toggle('inview',en.isIntersecting);});
    },{threshold:.15});
    movers.forEach(m=>mio.observe(m));
  } else { movers.forEach(m=>m.classList.add('inview')); }

  // Foster-style auto slideshow (gallery page)
  const show=document.getElementById('show');
  if(show){
    const slides=[...show.querySelectorAll('.slide')];
    const count=document.getElementById('shCount');
    const fill=document.getElementById('shFill');
    const bar=fill?fill.closest('.sh-bar'):null;
    const dotsBox=document.getElementById('shDots');
    const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let cur=0, timer=null;
    const pad=n=>String(n).padStart(2,'0');
    slides.forEach((_,i)=>{
      const d=document.createElement('button');
      d.setAttribute('aria-label','Show project '+(i+1));
      d.addEventListener('click',()=>{go(i);restart();});
      if(dotsBox)dotsBox.appendChild(d);
    });
    const dots=dotsBox?[...dotsBox.children]:[];
    const paint=()=>{
      slides.forEach((s,i)=>s.classList.toggle('on',i===cur));
      dots.forEach((d,i)=>d.classList.toggle('on',i===cur));
      if(count)count.textContent=pad(cur+1)+' / '+pad(slides.length);
      if(bar){bar.classList.remove('playing');void bar.offsetWidth;if(!reduce)bar.classList.add('playing');}
    };
    const go=i=>{cur=(i+slides.length)%slides.length;paint();};
    const restart=()=>{if(timer)clearInterval(timer);if(!reduce)timer=setInterval(()=>go(cur+1),4000);};
    const prev=document.getElementById('shPrev'), next=document.getElementById('shNext');
    if(prev)prev.addEventListener('click',()=>{go(cur-1);restart();});
    if(next)next.addEventListener('click',()=>{go(cur+1);restart();});
    document.addEventListener('keydown',e=>{
      if(!show)return;
      if(e.key==='ArrowLeft'){go(cur-1);restart();}
      if(e.key==='ArrowRight'){go(cur+1);restart();}
    });
    show.addEventListener('mouseenter',()=>{if(timer)clearInterval(timer);if(bar)bar.classList.remove('playing');});
    show.addEventListener('mouseleave',()=>{paint();restart();});
    // grid thumbnails jump the show to the matching slide
    document.querySelectorAll('.gallery-grid figure img').forEach(img=>{
      img.style.cursor='pointer';
      img.addEventListener('click',()=>{
        const f=(img.getAttribute('src')||'').split('/').pop();
        const hit=slides.findIndex(s=>(s.querySelector('img').getAttribute('src')||'').split('/').pop()===f);
        if(hit>-1){go(hit);restart();show.scrollIntoView({behavior:'smooth'});}
      });
    });
    paint();restart();
  }

  // reveal on scroll
  const els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window && els.length){
    const io=new IntersectionObserver((entries)=>{
      entries.forEach(en=>{if(en.isIntersecting){en.target.classList.add('visible');io.unobserve(en.target);}});
    },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    els.forEach(el=>io.observe(el));
  } else { els.forEach(el=>el.classList.add('visible')); }

  // animated counters
  const counters=document.querySelectorAll('[data-count]');
  if(counters.length && 'IntersectionObserver' in window){
    const cio=new IntersectionObserver((entries)=>{
      entries.forEach(en=>{
        if(!en.isIntersecting) return;
        const el=en.target; cio.unobserve(el);
        const target=parseFloat(el.getAttribute('data-count')||'0');
        const suffix=el.getAttribute('data-suffix')||'';
        const dur=1400, t0=performance.now();
        const tick=(now)=>{
          const p=Math.min(1,(now-t0)/dur);
          const eased=1-Math.pow(1-p,3);
          el.textContent=Math.round(target*eased)+suffix;
          if(p<1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    },{threshold:.4});
    counters.forEach(c=>cio.observe(c));
  }

  // testimonials rotator
  const quotes=[
    {q:'“Plinth fixed our Goodwood parapet leaks two winters ago, still bone dry. Written quote, fixed price, tidy site every day.”',w:'Homeowner · Richmond Estate, Goodwood*'},
    {q:'“Bathroom strip-out to re-tile in seven days. Dust sheets, daily photos, zero surprises on the invoice.”',w:'Client · Bellville*'},
    {q:'“They prepped our DB and trunking for solar before our installer arrived. Saved us a full day on site.”',w:'Homeowner · Century City*'}
  ];
  const bq=document.getElementById('tQuote'), who=document.getElementById('tWho'), dots=document.getElementById('tDots');
  let ti=0, timer=null;
  const render=(i)=>{
    ti=i;
    if(bq) bq.textContent=quotes[i].q;
    if(who) who.textContent=quotes[i].w;
    if(dots) [...dots.children].forEach((d,di)=>d.classList.toggle('on',di===i));
  };
  if(bq&&dots){
    quotes.forEach((_,i)=>{const d=document.createElement('button');d.setAttribute('aria-label','Show review '+(i+1));d.addEventListener('click',()=>{render(i);restart();});dots.appendChild(d);});
    render(0);
    const restart=()=>{if(timer)clearInterval(timer);timer=setInterval(()=>render((ti+1)%quotes.length),5200);};
    restart();
  }

  // FAQ: single-open accordion + smooth
  const items=[...document.querySelectorAll('details.faq-item')];
  items.forEach(d=>{
    d.addEventListener('toggle',()=>{
      if(d.open) items.forEach(o=>{if(o!==d&&o.open)o.open=false;});
    });
  });

  // year + estimate form
  const y=document.getElementById('yr'); if(y) y.textContent=new Date().getFullYear();
  const f=document.getElementById('estimate-form');
  if(f){
    f.addEventListener('submit',(e)=>{
      e.preventDefault();
      const d=new FormData(f);
      const name=String(d.get('name')||'there').slice(0,60);
      const box=document.getElementById('form-ok');
      if(box){box.style.display='block';box.innerHTML='<strong>Thank you, '+name+'.</strong><br>We received your request and will contact you within 1 business day on '+String(d.get('phone')||'your number')+'. For urgent jobs call <a href="tel:+27661505770">066 150 5770</a>.';box.scrollIntoView({behavior:'smooth',block:'center'});}
      f.reset();
    });
  }
});
