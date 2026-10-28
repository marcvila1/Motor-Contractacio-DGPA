src='Motor_integrat_v063.html'; dst='Motor_integrat_v064.html'
h=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:60],h.count(a)); h=h.replace(a,b)
# ── 1. NIF: DNI, NIE i CIF d'empresa (B12345678) ───────────────────
rep('placeholder="Format: 12345678A" required="" pattern="^[0-9]{8}[A-Z]$|^[XYZ][0-9]{7}[A-Z]$"',
    'placeholder="Format: 12345678A, X1234567L o B12345678 (empresa)" required="" pattern="^[0-9]{8}[A-Za-z]$|^[XYZxyz][0-9]{7}[A-Za-z]$|^[ABCDEFGHJNPQRSUVWabcdefghjnpqrsuvw][0-9]{7}[0-9A-Ja-j]$"')
rep('placeholder="Format: 12345678A" required pattern="^[0-9]{8}[A-Z]$|^[XYZ][0-9]{7}[A-Z]$"',
    'placeholder="Format: 12345678A, X1234567L o B12345678 (empresa)" required pattern="^[0-9]{8}[A-Za-z]$|^[XYZxyz][0-9]{7}[A-Za-z]$|^[ABCDEFGHJNPQRSUVWabcdefghjnpqrsuvw][0-9]{7}[0-9A-Ja-j]$"')
rep('const nifRegex = /^[0-9]{8}[A-Z]$|^[XYZ][0-9]{7}[A-Z]$/;',
    '// DNI (12345678A), NIE (X1234567L) i CIF d\'empresa (B12345678; el dígit de control pot ser número o lletra A-J)\n    const nifRegex = /^[0-9]{8}[A-Z]$|^[XYZ][0-9]{7}[A-Z]$|^[ABCDEFGHJNPQRSUVW][0-9]{7}[0-9A-J]$/;')
# ── 2. Esborranys ──────────────────────────────────────────────────
# 2a. API de carpeta (dins de l'IIFE de la carpeta)
api='''// ── Esborranys de contractes a mig crear (subcarpeta esborranys/) ──
async function subEsb() { return arrel.getDirectoryHandle('esborranys', { create: true }); }
async function desaEsborrany(nom, dades) {
  const f = await (await subEsb()).getFileHandle(nom, { create: true });
  const w = await f.createWritable(); await w.write(JSON.stringify(dades, null, 2)); await w.close();
}
async function llistaEsborranys() {
  const dir = await subEsb(), out = [];
  for await (const [nom, h] of dir.entries()) {
    if (h.kind !== 'file' || !/\\.json$/i.test(nom)) continue;
    try { out.push({ nom, dades: JSON.parse(await (await h.getFile()).text()) }); } catch (e) {}
  }
  return out.sort((a, b) => String(b.dades?.desat || '').localeCompare(String(a.dades?.desat || '')));
}
async function eliminaEsborrany(nom) { await (await subEsb()).removeEntry(nom); }
window.carpetaContractes = {'''
rep('window.carpetaContractes = {',api)
rep("eliminar: eliminarContracteCarpeta, connectada: () => !!arrel };",
    "eliminar: eliminarContracteCarpeta, connectada: () => !!arrel, esborranys: { desa: desaEsborrany, llista: llistaEsborranys, elimina: eliminaEsborrany } };")
# 2b. UI + captura/restauració
js=r'''
<script>
/* ===== Esborranys: desa i recupera un contracte a mig crear al mòdul Inici (v064) ===== */
(function(){
'use strict';
var nomEsborrany = null;   // nom del fitxer de l'esborrany en curs (perquè desar de nou el sobreescrigui)
var $ = function(id){ return document.getElementById(id); };
var arrelInici = function(){ return $('module-inici'); };
var carpeta = function(){ return window.carpetaContractes && window.carpetaContractes.connectada && window.carpetaContractes.connectada() ? window.carpetaContractes.esborranys : null; };

function captura(){
  var camps={}, radios={}, checks={};
  arrelInici().querySelectorAll('input,select,textarea').forEach(function(e){
    var k=e.id||e.name; if(!k) return;
    if(['file','button','submit','reset'].indexOf(e.type)>=0) return;
    if(e.type==='radio'){ if(e.checked) radios[e.name]=e.value; return; }
    if(e.type==='checkbox'){ checks[k]=e.checked; return; }
    camps[k]=e.value;
  });
  return { tipus:'esborrany-contracte-inici', versio:1, desat:new Date().toISOString(), pas:currentStepInici,
           camps:camps, radios:radios, checks:checks,
           propostes:document.querySelectorAll('#propostesContainer .proposta-row').length,
           formData:JSON.parse(JSON.stringify(formDataInici)) };
}
function aplicaValors(d, ambEsdeveniments){
  var root=arrelInici();
  Object.keys(d.camps||{}).forEach(function(k){
    var e=$(k)||root.querySelector('[name="'+k+'"]'); if(!e||!root.contains(e)||e.type==='radio'||e.type==='checkbox') return;
    if(e.tagName==='SELECT' && ![].some.call(e.options,function(o){return o.value===d.camps[k];})) return;
    e.value=d.camps[k];
    if(ambEsdeveniments) e.dispatchEvent(new Event('input',{bubbles:true}));
  });
  Object.keys(d.checks||{}).forEach(function(k){ var e=$(k)||root.querySelector('[name="'+k+'"]'); if(e&&root.contains(e)) e.checked=!!d.checks[k]; });
}
function restaura(d){
  var root=arrelInici();
  // 1) camps que condicionen la resta (unitat, naturalesa, RAE…) amb els seus esdeveniments
  var u=$('unitatPromotora'); if(u && d.camps.unitatPromotora){ u.value=d.camps.unitatPromotora; u.dispatchEvent(new Event('change',{bubbles:true})); }
  Object.keys(d.radios||{}).forEach(function(n){
    root.querySelectorAll('input[type=radio][name="'+n+'"]').forEach(function(r){
      if(r.value===d.radios[n]){ r.checked=true; r.dispatchEvent(new Event('change',{bubbles:true})); r.dispatchEvent(new Event('click',{bubbles:true})); }
    });
  });
  // 2) propostes dinàmiques
  var cont=$('propostesContainer');
  if(cont && typeof afegirPropostaInici==='function'){ while(cont.querySelectorAll('.proposta-row').length < (d.propostes||0)) afegirPropostaInici(); }
  // 3) tots els valors (després, per no ser trepitjats per les autoomplertes)
  setTimeout(function(){
    aplicaValors(d,true);
    try{ Object.keys(d.formData||{}).forEach(function(p){ Object.assign(formDataInici[p]||(formDataInici[p]={}), d.formData[p]); }); }catch(e){}
    // 4) ens situem al pas on s'havia deixat
    var pas=d.pas||1;
    root.querySelectorAll('.paso-content').forEach(function(p){p.classList.remove('active');});
    var dest=$('paso-'+pas); if(dest) dest.classList.add('active');
    currentStepInici=pas;
    try{
      if(pas===3 && typeof initPaso3==='function') initPaso3();
      else if(pas===4 && typeof initPaso4==='function') initPaso4();
      else if(pas===5){ if(typeof renderitzarEnviamentsInici==='function') renderitzarEnviamentsInici(); if(typeof licMostraBotoPas5==='function') licMostraBotoPas5(); }
    }catch(e){ console.warn('Esborrany: init del pas',e); }
    updateProgressBarInici(); window.scrollTo(0,0);
    setTimeout(function(){ aplicaValors(d,false); },250);   // segona passada per si el pas ha tornat a pintar camps
    avis('✔ Esborrany recuperat. Continueu des del pas '+pas+'.');
  },300);
}
function avis(t){
  var a=$('avisEsborrany'); if(!a){ a=document.createElement('div'); a.id='avisEsborrany';
    a.style.cssText='position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#088074;color:#fff;padding:10px 18px;border-radius:6px;z-index:100000;font-size:14px;box-shadow:0 4px 14px rgba(0,0,0,.3);';
    document.body.appendChild(a); }
  a.textContent=t; a.style.display='block'; clearTimeout(a._t); a._t=setTimeout(function(){a.style.display='none';},4500);
}
function slug(s){ return String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^A-Za-z0-9]+/g,'_').replace(/^_+|_+$/g,'').slice(0,40); }
function nomNou(d){ var t=new Date(), p=function(n){return String(n).padStart(2,'0');};
  return 'Esborrany_'+(slug(d.camps.unitatPromotora)||'sense-unitat')+'_'+(slug(d.camps.titolContracte)||'sense-titol')+'_'+t.getFullYear()+p(t.getMonth()+1)+p(t.getDate())+'-'+p(t.getHours())+p(t.getMinutes())+'.json'; }

window.desaEsborranyInici=async function(){
  var d=captura();
  if(!d.camps.titolContracte && !d.camps.unitatPromotora){ avis('Ompliu com a mínim la unitat o el títol abans de desar.'); return; }
  if(!nomEsborrany) nomEsborrany=nomNou(d);
  var c=carpeta();
  if(c){ try{ await c.desa(nomEsborrany,d); avis('💾 Esborrany desat a la carpeta (esborranys/).'); return; }catch(e){ console.warn('Esborrany: carpeta',e); } }
  var blob=new Blob([JSON.stringify(d,null,2)],{type:'application/json'}), a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=nomEsborrany; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){URL.revokeObjectURL(a.href);},2000);
  avis('💾 Esborrany descarregat. Per recuperar-lo, useu «Recupera un esborrany».');
};
function carrega(d,nom){
  if(!d||d.tipus!=='esborrany-contracte-inici'){ alert('Aquest fitxer no és un esborrany de contracte del Motor.'); return; }
  var hiHaDades=($('titolContracte')&&$('titolContracte').value.trim())||($('descripcio')&&$('descripcio').value.trim());
  if(hiHaDades && !confirm('Recuperar l\'esborrany substituirà les dades que teniu ara al formulari. Voleu continuar?')) return;
  nomEsborrany=nom||null; var m=$('modalEsborranys'); if(m) m.style.display='none'; restaura(d);
}
window.recuperaEsborranyInici=async function(){
  var m=$('modalEsborranys');
  if(!m){ m=document.createElement('div'); m.id='modalEsborranys';
    m.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px;';
    m.innerHTML='<div style="background:#fff;border-radius:10px;max-width:700px;width:100%;max-height:88vh;overflow:auto;padding:22px;box-shadow:0 10px 40px rgba(0,0,0,.35);">'
      +'<h3 style="margin:0 0 10px;color:#088074;">📂 Recupera un esborrany</h3><div id="llistaEsborranys" style="margin-bottom:14px;font-size:14px;"></div>'
      +'<input type="file" id="fitxerEsborrany" accept=".json,application/json" style="display:none">'
      +'<div style="display:flex;gap:8px;justify-content:flex-end;"><button type="button" class="btn btn-secondary" id="btnObreFitxerEsb">Obre un fitxer…</button><button type="button" class="btn btn-secondary" onclick="document.getElementById(\'modalEsborranys\').style.display=\'none\'">Tanca</button></div></div>';
    document.body.appendChild(m);
    m.addEventListener('click',function(e){ if(e.target===m) m.style.display='none'; });
    $('btnObreFitxerEsb').onclick=function(){ $('fitxerEsborrany').click(); };
    $('fitxerEsborrany').onchange=function(ev){ var f=ev.target.files[0]; if(!f) return; var r=new FileReader();
      r.onload=function(){ try{ carrega(JSON.parse(r.result), f.name); }catch(e){ alert('No s\'ha pogut llegir el fitxer.'); } }; r.readAsText(f); ev.target.value=''; };
  }
  m.style.display='flex';
  var ll=$('llistaEsborranys'); ll.textContent='';
  var c=carpeta();
  if(!c){ ll.textContent='La carpeta de contractes no està connectada: trieu el fitxer d\'esborrany que heu descarregat.'; return; }
  ll.textContent='Carregant…';
  try{
    var llista=await c.llista(); ll.textContent='';
    if(!llista.length){ ll.textContent='No hi ha cap esborrany a la carpeta.'; return; }
    llista.forEach(function(it){
      var d=it.dades||{}, fila=document.createElement('div');
      fila.style.cssText='display:flex;gap:8px;align-items:center;padding:8px 0;border-bottom:1px solid #eee;';
      var t=document.createElement('div'); t.style.flex='1';
      var data=d.desat?new Date(d.desat).toLocaleString('ca-ES'):'';
      t.innerHTML='<strong></strong><br><span style="color:#666;font-size:12px;"></span>';
      t.children[0].textContent=(d.camps&&d.camps.titolContracte)||'(sense títol)';
      t.children[2].textContent=((d.camps&&d.camps.unitatPromotora)||'sense unitat')+' · pas '+(d.pas||1)+' · '+data;
      var b1=document.createElement('button'); b1.type='button'; b1.className='btn btn-primary'; b1.textContent='Obre'; b1.onclick=function(){ carrega(d,it.nom); };
      var b2=document.createElement('button'); b2.type='button'; b2.className='btn btn-secondary'; b2.textContent='🗑';
      b2.onclick=async function(){ if(confirm('Voleu eliminar aquest esborrany?')){ await c.elimina(it.nom); fila.remove(); } };
      fila.appendChild(t); fila.appendChild(b1); fila.appendChild(b2); ll.appendChild(fila);
    });
  }catch(e){ ll.textContent='No s\'ha pogut llegir la carpeta d\'esborranys.'; }
};

function munta(){
  var r=arrelInici(); if(!r) return;
  // barra superior
  var h1=r.querySelector('#module-content h1');
  if(h1 && !$('barraEsborranys')){
    var b=document.createElement('div'); b.id='barraEsborranys'; b.style.cssText='display:flex;gap:8px;flex-wrap:wrap;margin:-10px 0 18px;';
    b.innerHTML='<button type="button" class="btn btn-secondary" onclick="recuperaEsborranyInici()">📂 Recupera un esborrany</button><button type="button" class="btn btn-secondary" onclick="desaEsborranyInici()">💾 Desa l\'esborrany</button>';
    h1.nextElementSibling.insertAdjacentElement('afterend',b);
  }
  // botó de desar a cada pas
  r.querySelectorAll('.paso-buttons').forEach(function(pb){
    if(pb.querySelector('.btn-desa-esb')) return;
    var btn=document.createElement('button'); btn.type='button'; btn.className='btn btn-secondary btn-desa-esb'; btn.textContent='💾 Desa l\'esborrany';
    btn.onclick=function(){ desaEsborranyInici(); }; pb.insertBefore(btn, pb.children[1]||null);
  });
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',munta); else munta();
})();
</script>
'''
i=h.rindex('</body>'); h=h[:i]+js+h[i:]
open(dst,'w',encoding='utf-8').write(h); print('ok')
