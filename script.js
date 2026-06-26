// State
let selectedSymptoms = new Set();
let selectedDiseases = new Set();
let activeMeal = 'morning';

// Date
const days = ['อาทิตย์','จันทร์','อังคาร','พุธ','พฤหัสบดี','ศุกร์','เสาร์'];
const months = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
const now = new Date();
document.getElementById('today-date').textContent = `วัน${days[now.getDay()]} ${now.getDate()} ${months[now.getMonth()]} ${now.getFullYear()+543}`;

// Foods database (loaded from API)
let foods = {};

// Fetch food data from the API
async function loadFoods() {
  try {
    const res = await fetch('/api/foods');
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    foods = await res.json();
    renderFoods(activeMeal);
  } catch (err) {
    console.error('Failed to load foods from API:', err);
  }
}

loadFoods();

function toggleSymptom(btn) {
  const s = btn.dataset.sym;
  if (btn.classList.contains('active')) {
    btn.classList.remove('active');
    selectedSymptoms.delete(s);
  } else {
    btn.classList.add('active');
    selectedSymptoms.add(s);
  }
}

function toggleDisease(d) {
  if (d === 'ไม่มีโรค') {
    if (selectedDiseases.has('ไม่มีโรค')) {
      selectedDiseases.delete('ไม่มีโรค');
    } else {
      selectedDiseases.clear();
      selectedDiseases.add('ไม่มีโรค');
    }
  } else {
    selectedDiseases.delete('ไม่มีโรค');
    if (selectedDiseases.has(d)) {
      selectedDiseases.delete(d);
    } else {
      selectedDiseases.add(d);
    }
  }
  syncDiseaseTags();
}

function toggleDiseaseTag(el) {
  const d = el.dataset.d;
  toggleDisease(d);
}

function selectDiseaseFromDropdown(val) {
  if (!val) return;
  toggleDisease(val);
  // Reset dropdown to placeholder
  document.getElementById('disease-select').value = '';
}

function syncDiseaseTags() {
  document.querySelectorAll('.d-tag').forEach(t => {
    t.classList.toggle('active', selectedDiseases.has(t.dataset.d));
  });
}

function doSearch() {
  const panel = document.getElementById('result-panel');
  const inner = document.getElementById('result-inner');

  if (selectedDiseases.size === 0 && selectedSymptoms.size === 0) {
    inner.innerHTML = `<div style="color:#b85e00;font-weight:500">⚠️ กรุณาเลือกอาการ หรือโรคประจำตัวก่อนค้นหา</div>`;
    panel.style.display = 'block';
    return;
  }

  let msg = '<div style="font-family:\'Mitr\',sans-serif;font-size:1rem;font-weight:600;color:#7a4e00;margin-bottom:0.5rem">📋 คำแนะนำสำหรับคุณ</div><ul style="list-style:none;display:flex;flex-direction:column;gap:0.4rem">';

  const adviceMap = {
    'เบาหวาน': '🩸 เบาหวาน — หลีกเลี่ยงอาหาร GI สูง เน้นผักใยสูง โปรตีนลีน และคาร์บซับซ้อน',
    'ความดันโลหิตสูง': '❤️ ความดันสูง — ลดโซเดียม หลีกเลี่ยงอาหารเค็ม เน้นโพแทสเซียม เช่น กล้วย ผักใบเขียว',
    'ไขมันสูง': '🫀 ไขมันในเลือดสูง — เน้นโอเมก้า-3 ไขมันดี หลีกเลี่ยงอาหารทอด มันสัตว์',
    'โรคไต': '🫘 โรคไต — จำกัดโปรตีน โพแทสเซียม ฟอสฟอรัส เลือกอาหารที่ไตไม่ต้องทำงานหนัก',
    'โรคหัวใจ': '🫶 โรคหัวใจ — เน้นไขมันดี ลดคอเลสเตอรอล เลี่ยงของทอด เกลือ น้ำตาล',
    'ภูมิแพ้กลูเตน': '🌾 ภูมิแพ้กลูเตน — หลีกเลี่ยงข้าวสาลี ข้าวบาร์เลย์ ข้าวไรย์ เลือกข้าวกล้อง ข้าวโพด มันเทศ',
    'แพ้นม': '🥛 แพ้นม/แลคโตส — หลีกเลี่ยงผลิตภัณฑ์นม เลือกนมพืช เต้าหู้ หรืออาหารเสริมแคลเซียม',
    'ไม่มีโรค': '🌿 สุขภาพดี — กินอาหารหลากหลายครบ 5 หมู่ เน้นผักผลไม้สด ธัญพืชไม่ขัดสี',
  };

  const symptomAdvice = {
    'ปวดหัว': '🤕 ปวดหัว — ดื่มน้ำให้เพียงพอ กินแมกนีเซียม (ผักใบเขียว ถั่ว) หลีกเลี่ยงคาเฟอีน',
    'ลำไส้แปรปรวน': '🤢 ลำไส้แปรปรวน — กินอาหารอ่อน ๆ โยเกิร์ต โปรไบโอติก หลีกเลี่ยงของมัน เผ็ด',
    'ปวดท้อง': '😣 ปวดท้อง — กินข้าวต้ม โจ๊ก ซุป อ่อน ๆ ย่อยง่าย หลีกเลี่ยงของทอด ของแข็ง',
    'กินได้น้อย': '😔 กินได้น้อย — กินมื้อเล็ก ๆ บ่อยครั้ง เน้นอาหารที่มีโภชนาการสูงต่อมื้อ',
    'อ่อนเพลีย': '😴 อ่อนเพลีย — เพิ่มธาตุเหล็ก วิตามินบี โปรตีน และคาร์โบไฮเดรตที่ดีเพื่อพลังงาน',
    'มีอื่น ๆ': '❓ อาการอื่น ๆ — ควรปรึกษาแพทย์หรือนักโภชนาการเพื่อการดูแลที่ตรงจุด',
  };

  selectedDiseases.forEach(d => {
    if (adviceMap[d]) {
      msg += `<li style="background:rgba(245,130,31,0.1);border-left:3px solid var(--orange);padding:0.5rem 0.8rem;border-radius:0 8px 8px 0;font-size:0.88rem">${adviceMap[d]}</li>`;
    }
  });
  selectedSymptoms.forEach(s => {
    if (symptomAdvice[s]) {
      msg += `<li style="background:rgba(58,170,110,0.08);border-left:3px solid var(--green);padding:0.5rem 0.8rem;border-radius:0 8px 8px 0;font-size:0.88rem">${symptomAdvice[s]}</li>`;
    }
  });

  msg += '</ul>';
  inner.innerHTML = msg;
  panel.style.display = 'block';
  renderFoods(activeMeal);
  document.getElementById('daily').scrollIntoView({ behavior: 'smooth' });
}

function switchMeal(meal, btn) {
  activeMeal = meal;
  document.querySelectorAll('.meal-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  renderFoods(meal);
}

const tagColors = { 'GI ต่ำ':'green','โปรตีนสูง':'blue','ไขมันต่ำ':'green','ย่อยง่าย':'green','โซเดียมต่ำ':'blue','วิตามินสูง':'green','ใยอาหารสูง':'green','โอเมก้า-3':'blue','คาร์บต่ำ':'orange','เบตาแคโรทีน':'orange','โปรตีนพืช':'green','โปรไบโอติก':'blue','พลังงานเร็ว':'orange','ไขมันดี':'green','สุขภาพหัวใจ':'red','คาร์บสูง':'orange' };

function renderFoods(meal) {
  const grid = document.getElementById('food-grid');
  const list = foods[meal] || [];

  grid.innerHTML = list.map(f => {
    const avoided = [...selectedDiseases].some(d => f.avoid.includes(d));
    const relevantToSymptom = [...selectedSymptoms].some(s => f.good.includes(s));

    const highlight = (!avoided && relevantToSymptom) ? 'box-shadow:0 0 0 3px var(--green),0 8px 24px rgba(58,170,110,0.2);' : '';
    const opacity = avoided ? 'opacity:0.4;filter:grayscale(0.6);' : '';

    const tagsHtml = f.tags.map(t => {
      const c = tagColors[t] || 'green';
      return `<span class="ftag ${c}">${t}</span>`;
    }).join('') + (avoided ? '<span class="ftag red">⚠ ควรหลีกเลี่ยง</span>' : '') + (relevantToSymptom && !avoided ? '<span class="ftag green">✓ แนะนำสำหรับคุณ</span>' : '');

    const imgHtml = f.image ? `<img src="${f.image}" alt="${f.name}" style="width:100%;height:100%;object-fit:cover;display:block;">` : f.emoji;

    return `
    <div class="food-card" style="${opacity}${highlight}">
      <div class="food-img" style="background:${f.image ? 'none' : 'linear-gradient(135deg, var(--green-light), #d4f0e2)'}">
        ${imgHtml}
        <span class="kcal-badge">${f.kcal}</span>
      </div>
      <div class="food-body">
        <div class="food-name">${f.name}</div>
        <div class="food-desc">${f.desc}</div>
        <div class="food-tags">${tagsHtml}</div>
        <div class="nutrient-row" style="margin-top:0.7rem;padding-top:0.6rem;border-top:1px solid var(--border)">
          <div class="ntr"><span class="nval">${f.p}g</span>โปรตีน</div>
          <div class="ntr"><span class="nval">${f.c}g</span>คาร์บ</div>
          <div class="ntr"><span class="nval">${f.f}g</span>ไขมัน</div>
          <div class="ntr"><span class="nval">${f.sugar}g</span>น้ำตาล</div>
        </div>
      </div>
    </div>`;
  }).join('');
}

// Scroll observer
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-up').forEach(el => obs.observe(el));

