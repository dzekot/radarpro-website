(function () {
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }

  const galleryData = [
    {
      id: 'turkiye',
      title: 'Türkiye kapsam haritası',
      desc: '2.660 radar, 802 hız koridoru ve 1.454 EDS — güncel veriyle haritada, rotanız boyunca.',
      image: 'assets/turkiye-yollari.png',
    },
    {
      id: 'harita',
      title: 'Yoğun bölgeler',
      desc: 'Şehir girişleri ve kalabalık hatlarda erken uyarı. Yoğun trafikte de kontrol sizde.',
      image: 'assets/yogun-bolgeler.png',
    },
    {
      id: 'eds',
      title: 'EDS erken uyarı',
      desc: 'Noktaya yaklaşırken ses ve görsel bildirim. Hız limitini önceden bilin.',
      image: 'assets/eds-erken-uyari.png',
    },
    {
      id: 'koridor',
      title: 'Hız koridoru takibi',
      desc: 'Giriş ve çıkış anlarında ortalama hız hesabı. Koridor boyunca sürpriz yok.',
      image: 'assets/koridor-yaklasma.png',
    },
    {
      id: 'hiz',
      title: 'Anlık hız HUD',
      desc: 'Neon gösterge ile anlık ve ortalama hız. Tek bakış, net okuma.',
      image: 'assets/anlik-hiz.png',
    },
    {
      id: 'surus',
      title: 'Kişisel sürüş HUD',
      desc: 'Sesli uyarı, sürücü ayarları ve kişisel gösterge. Deneyimi size göre ayarlayın.',
      image: 'assets/surus-hud.png',
    },
    {
      id: 'arka-plan',
      title: 'Arka planda aktif',
      desc: 'Sürüşü algılar, uyarıları sesli verir. Arka plana alın — navigasyon açıkken bile keyfinize bakın.',
      image: 'assets/hero-arka-plan.png',
    },
    {
      id: 'uzun-yol',
      title: 'Uzun yol sürüşü',
      desc: 'Otoyol ve şehirlerarası hatlarda güvenilir uyarı. Yola odaklanın.',
      image: 'assets/uzun-yol.png',
    },
  ];

  const tabs = document.querySelector('.gallery-tabs');
  const titleEl = document.querySelector('.gallery-info h3');
  const descEl = document.querySelector('.gallery-info p');
  const mainImg = document.querySelector('.gallery-phone img');
  const thumbs = document.querySelector('.gallery-thumbs');

  if (!tabs || !titleEl || !descEl || !mainImg || !thumbs) return;

  function setActive(index) {
    const item = galleryData[index];
    titleEl.textContent = item.title;
    descEl.textContent = item.desc;
    mainImg.style.opacity = '0';
    setTimeout(() => {
      mainImg.src = item.image;
      mainImg.alt = item.title;
      mainImg.style.opacity = '1';
    }, 150);

    tabs.querySelectorAll('.gallery-tab').forEach((tab, i) => {
      tab.classList.toggle('active', i === index);
    });
    thumbs.querySelectorAll('.gallery-thumb').forEach((thumb, i) => {
      thumb.classList.toggle('active', i === index);
    });
  }

  galleryData.forEach((item, index) => {
    const tab = document.createElement('button');
    tab.type = 'button';
    tab.className = 'gallery-tab' + (index === 0 ? ' active' : '');
    tab.textContent = item.title.split(' ').slice(0, 2).join(' ');
    tab.addEventListener('click', () => setActive(index));
    tabs.appendChild(tab);

    const thumb = document.createElement('button');
    thumb.type = 'button';
    thumb.className = 'gallery-thumb' + (index === 0 ? ' active' : '');
    thumb.setAttribute('aria-label', item.title);
    const img = document.createElement('img');
    img.src = item.image;
    img.alt = '';
    thumb.appendChild(img);
    thumb.addEventListener('click', () => setActive(index));
    thumbs.appendChild(thumb);
  });
})();
