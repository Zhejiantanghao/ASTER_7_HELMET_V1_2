document.body.insertBefore(document.querySelector('#case-dialog'),document.querySelector('footer'));
// Click-driven routes: home > directions > direction > case. Hash routes also work offline.
const renders=new Map();document.querySelectorAll('[data-case]').forEach(btn=>{renders.set(btn.dataset.case,btn.onclick);btn.onclick=()=>location.hash='/case/'+btn.dataset.case});
const overview=document.createElement('section');overview.id='direction-picker';overview.className='route-page';overview.innerHTML=`<p class="eyebrow">SELECT A DIRECTION</p><h1>从哪个方向开始？</h1><p class="route-intro">选择一个形态命题，查看它的设计案例与研究过程。</p><div class="case-grid">${ATLAS.branches.map(b=>`<a class="direction-choice" href="#/direction/${b.id}">${placeholder('方向代表图 · 待填充')}<span class="branch-number">${b.id}</span><h2>${b.name}</h2><p class="english">${b.en}</p><p>${b.idea}</p><strong>查看设计案例</strong></a>`).join('')}</div>`;document.querySelector('main').append(overview);
document.querySelectorAll('.brand,.summary>a,footer a').forEach(a=>a.href='#/');document.querySelectorAll('.top-link,.primary').forEach(a=>a.href='#/directions');document.querySelectorAll('.branch-nav a').forEach((a,i)=>a.href='#/direction/'+ATLAS.branches[i].id);
const trail=document.querySelector('#page-trail');
function route(){
 let path=location.hash.slice(1)||'/';if(path.startsWith('branch-'))path='/direction/'+path.slice(-2);if(path==='directions')path='/directions';
 const parts=path.split('/').filter(Boolean),kind=parts[0]||'home',id=parts[1];
 const branch=ATLAS.branches.find(b=>b.id===(kind==='case'?id?.split('-')[0]:id));
 const valid=kind==='home'||kind==='directions'||(kind==='direction'&&branch)||(kind==='case'&&renders.has(id));
 if(!valid){location.replace('#/');return}
 dialog.removeAttribute('open');document.body.dataset.page=kind;
 $('.hero').hidden=kind!=='home';$('.directions').hidden=kind!=='direction';overview.hidden=kind!=='directions';$('.process').hidden=true;$('.summary').hidden=true;
 document.querySelectorAll('.branch').forEach(el=>{el.hidden=el.id!=='branch-'+id;el.classList.add('in')});$('.section-heading').hidden=true;
 const home='<a href="#/">项目首页</a>',dirs='<a href="#/directions">设计方向</a>';
 trail.innerHTML=kind==='home'?'':`<a class="back-link" href="${kind==='directions'?'#/':kind==='direction'?'#/directions':'#/direction/'+branch.id}">返回${kind==='directions'?'首页':kind==='direction'?'方向选择':'案例列表'}</a><nav aria-label="面包屑">${home}<span>/</span>${dirs}${branch?`<span>/</span><a href="#/direction/${branch.id}">${branch.name}</a>`:''}${kind==='case'?'<span>/</span><span>案例详情</span>':''}</nav>`;
 if(kind==='case'){renders.get(id)();$('#case-title').setAttribute('tabindex','-1');$('#case-title').focus({preventScroll:true});document.querySelectorAll('#detail-nav a').forEach(a=>a.classList.remove('active'));$('#detail-nav a').classList.add('active')}
 document.title=(kind==='home'?'项目首页':kind==='directions'?'设计方向':kind==='direction'?branch.name:current.title)+' · ASTER-7';
 window.scrollTo({top:0,behavior:'instant'});
}
addEventListener('hashchange',route);route();

