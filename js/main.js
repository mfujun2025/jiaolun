// ========== Header scroll effect ==========
const header = document.getElementById('header');
const backTop = document.getElementById('backTop');

window.addEventListener('scroll', () => {
  if (window.scrollY > 30) {
    header.classList.add('scrolled');
    backTop.classList.add('show');
  } else {
    header.classList.remove('scrolled');
    backTop.classList.remove('show');
  }
});

// ========== Mobile nav toggle ==========
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

navToggle.addEventListener('click', () => {
  navMenu.classList.toggle('open');
  // change icon
  navToggle.innerHTML = navMenu.classList.contains('open') ? '&#10005;' : '&#9776;';
});

// Close mobile nav when clicking a link
navMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navMenu.classList.remove('open');
    navToggle.innerHTML = '&#9776;';
  });
});

// ========== Back to top ==========
backTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ========== Contact form → 飞书机器人 ==========
const FEISHU_WEBHOOK = 'https://open.feishu.cn/open-apis/bot/v2/hook/da44bf55-a112-4617-b1ea-1ae5e946276b';
const contactForm = document.getElementById('contactForm');
const formMsg = document.getElementById('formMsg');

if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const company = document.getElementById('company').value.trim();
    const product = document.getElementById('product').value;
    const message = document.getElementById('message').value.trim();

    if (!name || !phone || !message) {
      alert('请填写必填项（姓名、电话、需求描述）');
      return;
    }

    // 产品选项文本映射
    const productMap = {
      industrial: '工业脚轮',
      caster: '万向轮',
      forklift: '叉车轮',
      'heat-resistant': '耐高温脚轮',
      quiet: '静音脚轮',
      'heavy-duty': '重型脚轮',
      conductive: '导电/防静电脚轮',
      pu: 'PU发泡轮',
      custom: '来图来样定制',
      other: '其他',
    };
    const productText = product ? (productMap[product] || product) : '未指定';

    // 构建飞书 post 富文本消息
    const now = new Date();
    const timeStr = now.getFullYear() + '-' +
      String(now.getMonth() + 1).padStart(2, '0') + '-' +
      String(now.getDate()).padStart(2, '0') + ' ' +
      String(now.getHours()).padStart(2, '0') + ':' +
      String(now.getMinutes()).padStart(2, '0');

    const feishuPayload = {
      msg_type: 'post',
      content: {
        post: {
          zh_cn: {
            title: '📋 脚轮.cn - 新客户咨询',
            content: [
              [{ tag: 'text', text: '👤 姓名：' + name }],
              [{ tag: 'text', text: '📞 电话：' + phone }],
              [{ tag: 'text', text: '🏢 公司：' + (company || '未填写') }],
              [{ tag: 'text', text: '🏷 产品：' + productText }],
              [{ tag: 'text', text: '📝 需求：' + message }],
              [{ tag: 'text', text: '🕐 时间：' + timeStr }],
            ],
          },
        },
      },
    };

    try {
      const resp = await fetch(FEISHU_WEBHOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feishuPayload),
      });
      const data = await resp.json();

      if (data.StatusCode === 0 || data.code === 0 || data.msg === 'success') {
        formMsg.classList.add('show');
        contactForm.reset();
        setTimeout(() => formMsg.classList.remove('show'), 5000);
      } else {
        alert('提交失败，请稍后重试或直接拨打热线 400-888-9999');
      }
    } catch (err) {
      // 网络错误时，保留表单数据并提示
      alert('网络异常，提交失败。请稍后重试，或直接拨打热线 400-888-9999');
    }
  });
}

// ========== Smooth scroll for anchor links ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
