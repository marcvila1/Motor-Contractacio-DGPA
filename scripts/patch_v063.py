import re,sys
src='Motor_integrat_v062.html'; dst='Motor_integrat_v063.html'
h=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a,h.count(a)); h=h.replace(a,b)
# 1. termini RAE 15/12 -> 30/12
rep('no posterior a 15 de desembre, any en curs','no posterior a 30 de desembre, any en curs')
rep('i no posterior a 15 de desembre</p>','i no posterior a 30 de desembre</p>')
rep('// Validar que la data de RAE no sigui posterior a 15 de desembre','// Validar que la data de RAE no sigui posterior a 30 de desembre')
rep('// Validació 2: Data no pot ser posterior a 15 de desembre','// Validació 2: Data no pot ser posterior a 30 de desembre')
rep('new Date(yearNum, 11, 15);','new Date(yearNum, 11, 30);')
rep("'❌ La data no pot ser posterior a 15 de desembre'","'❌ La data no pot ser posterior a 30 de desembre'")
rep('≤ 15 de desembre (ja ho fa','≤ 30 de desembre (ja ho fa')
rep('futura i ≤ 15/12','futura i ≤ 30/12')
rep("includes('posterior a 15')","includes('posterior a 30')")
# 3. botó prompt CPV
btn='''          <div style="margin:0 0 10px 0;">
            <button type="button" class="btn btn-secondary" onclick="obrirPromptCPV()" style="padding:6px 12px;">🤖 No sé quin CPV triar: genera un prompt per al Copilot</button>
          </div>
          <select id="cpv" name="cpv" required="">'''
rep('          <select id="cpv" name="cpv" required="">',btn)
js='''
<script>
/* ===== Prompt per al Copilot: ajuda per triar el CPV (v063) ===== */
function construeixPromptCPV(){
  var g=function(id){var e=document.getElementById(id);return e?(e.value||'').trim():'';};
  var nat=(document.querySelector('input[name="naturalesa"]:checked')||{}).value||'';
  var natTxt={SERVEI:'Servei',OBRA:'Obra',SUBMINISTRAMENT:'Subministrament'}[nat]||'(no indicada)';
  var titol=g('titolContracte')||'[escriviu aquí el títol del contracte]';
  var desc=g('descripcio')||'[escriviu aquí una descripció del que cal contractar]';
  return 'Actua com a expert en contractació pública a Catalunya. Necessito que m\\'indiquis el codi CPV (Common Procurement Vocabulary, Reglament (CE) 213/2008, versió oficial vigent) més adequat per a aquest contracte.\\n\\n'
  +'DADES DEL CONTRACTE\\n- Naturalesa: '+natTxt+'\\n- Títol: '+titol+'\\n- Descripció: '+desc+'\\n\\n'
  +'INSTRUCCIONS\\n'
  +'1. Proposa un codi CPV principal i, com a màxim, dos d\\'alternatius, tots amb el format oficial de 8 dígits + dígit de control (exemple: 77310000-6).\\n'
  +'2. Tria el codi més específic possible (nivell de grup, classe o categoria) que descrigui l\\'objecte principal del contracte, no el més genèric.\\n'
  +'3. Que el CPV sigui coherent amb la naturalesa indicada: els codis 45xxxxxx són d\\'obres, els 03–44 acostumen a ser subministraments i els 50–98 serveis.\\n'
  +'4. Si el contracte barreja prestacions, tria el CPV de la prestació que representi la part principal del valor.\\n'
  +'5. Per a cada codi indica: el codi, la descripció oficial en català i, en una frase, per què hi encaixa.\\n'
  +'6. No t\\'inventis codis: si no n\\'estàs segur, indica-ho i demana\\'m més detalls.\\n'
  +'7. Respon en català, de manera breu, amb aquest format:\\n   CPV principal: [codi] — [descripció]\\n   Alternatius: [codi] — [descripció]\\n   Motiu: [una frase]';
}
function obrirPromptCPV(){
  var m=document.getElementById('modalPromptCPV');
  if(!m){
    m=document.createElement('div'); m.id='modalPromptCPV';
    m.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px;';
    m.innerHTML='<div style="background:#fff;border-radius:10px;max-width:720px;width:100%;max-height:90vh;overflow:auto;padding:22px;box-shadow:0 10px 40px rgba(0,0,0,.35);font-family:inherit;">'
     +'<h3 style="margin:0 0 8px 0;color:#088074;">🤖 Ajuda per trobar el CPV amb el Copilot</h3>'
     +'<ol style="margin:0 0 12px 18px;padding:0;line-height:1.5;font-size:14px;"><li>Reviseu el text següent (s\\'ha omplert amb el títol, la descripció i la naturalesa que heu escrit; podeu editar-lo).</li><li>Premeu <b>Copia el prompt</b> i enganxeu-lo al Copilot.</li><li>Torneu aquí, escriviu el codi que us proposi al cercador de CPV i trieu-lo a la llista.</li></ol>'
     +'<textarea id="textPromptCPV" rows="16" style="width:100%;box-sizing:border-box;padding:10px;border:1px solid #ccc;border-radius:6px;font-size:13px;"></textarea>'
     +'<p style="font-size:12px;color:#666;margin:6px 0 12px 0;">Consell: com més detallada sigui la descripció, més encertat serà el CPV. Verifiqueu sempre el codi a la llista del Motor abans de continuar.</p>'
     +'<div style="display:flex;gap:8px;justify-content:flex-end;"><span id="avisCopiatCPV" style="align-self:center;color:#2e7d32;font-size:13px;"></span>'
     +'<button type="button" class="btn btn-secondary" onclick="document.getElementById(\\'modalPromptCPV\\').style.display=\\'none\\'">Tanca</button>'
     +'<button type="button" class="btn btn-primary" onclick="copiaPromptCPV()">📋 Copia el prompt</button></div></div>';
    document.body.appendChild(m);
    m.addEventListener('click',function(e){if(e.target===m)m.style.display='none';});
  }
  document.getElementById('textPromptCPV').value=construeixPromptCPV();
  document.getElementById('avisCopiatCPV').textContent='';
  m.style.display='flex';
}
function copiaPromptCPV(){
  var t=document.getElementById('textPromptCPV'), av=document.getElementById('avisCopiatCPV');
  var ok=function(){av.textContent='✔ Copiat';};
  var fallback=function(){t.focus();t.select();try{document.execCommand('copy');ok();}catch(e){av.textContent='Seleccioneu el text i premeu Ctrl+C';}};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t.value).then(ok,fallback);}else{fallback();}
}
</script>
'''
i=h.rindex('</body>'); h=h[:i]+js+h[i:]
open(dst,'w',encoding='utf-8').write(h)
print('ok')
