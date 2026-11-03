# Bakım Rehberi / Maintenance Guide

Bu depo, CYLOGIC SOFTWARE'in resmî dijital kimlik merkezini (GitHub Pages) barındırır.
Sayfalar `scripts/build.py` ile JSON kaynaklardan üretilir; harici bağımlılık yoktur.

## Hızlı başlangıç

```bash
python3 scripts/build.py          # index.html, en/, ru/, fa/ ve sitemap.xml üretir
python3 -m http.server 8000       # http://localhost:8000 adresinde önizleme
```

`main` branch'ine yapılan her push, `.github/workflows/deploy.yml` ile sayfaları yeniden üretir ve GitHub Pages'e otomatik yayınlar.
Workflow da `build.py` çalıştırdığı için yalnızca JSON dosyalarını düzenleyip push etmek yeterlidir; yerelde üretilen HTML dosyalarını da commit etmek önerilir (depo görünümü güncel kalır).

## İçerik güncelleme

| Ne değişecek? | Dosya |
|---|---|
| Metinler, hizmetler, SEO başlık/açıklama | `locales/tr.json`, `en.json`, `ru.json`, `fa.json` |
| Sosyal medya / resmî profiller | `data/social-links.json` |
| Teknoloji listesi, logo URL'si, yayın adresi | `scripts/build.py` (`TECH`, `LOGO`, `BASE_URL`) |
| Görünüm | `assets/css/style.css` |
| Etkileşim (dil menüsü, mobil menü, animasyon) | `assets/js/main.js` |
| README | `README.md` |

Dört dil dosyası aynı anahtar yapısını korumalıdır. Yeni bir hizmet eklerken her dört dosyaya da `services.items` altında aynı `id` ile ekleyin (`id` değeri ikon seçimi için kullanılır: `ai`, `erp`, `software`, `automation`, `it`).

## Sosyal profil ekleme kuralları

1. Yalnızca CYLOGIC SOFTWARE'e ait olduğu **doğrulanmış** resmî hesapları ekleyin.
2. Tahmini veya henüz açılmamış hesap URL'si eklemeyin.
3. Kişisel hesaplar, yönetim paneli bağlantıları veya giriş bilgileri asla eklenmez.
4. Yeni platform için `assets/icons/<id>.svg` dosyası ekleyin ([Simple Icons](https://simpleicons.org/), CC0) ve `assets/css/style.css` içinde `.si-<id>` arka plan rengini tanımlayın.
5. Bir hesabı geçici olarak gizlemek için `"verified": false` yapın.

Profiller otomatik olarak sayfadaki kartlara, footer'a ve Schema.org `sameAs` alanına yansır. README tablosunu ve `llms.txt` dosyasını elle güncelleyin.

## Güvenlik kontrol listesi (public depo)

- `.env`, API anahtarı, token, parola, özel anahtar **commit etmeyin** (`.gitignore` bunları dışlar).
- Müşteri verisi, iç ağ adresleri veya dahili sistem bağlantıları eklemeyin.
- Push öncesi hızlı tarama: `git grep -nIiE "(api[_-]?key|secret|token|password|BEGIN .*PRIVATE)"`

## Dil ve RTL notları

- Farsça (`fa`) sayfa `dir="rtl"` ile üretilir ve Vazirmatn yazı tipi yüklenir.
- Teknoloji adları, e-posta ve alan adları RTL içinde `dir="ltr"` ile korunur.
- Yön bağımlı stiller için CSS mantıksal özellikleri (`inset-inline-*`, `margin-inline-*`) kullanılır.

## SEO

- Her dil kendi URL'sine sahiptir; `canonical` ve `hreflang` (`x-default` = Türkçe) otomatik üretilir.
- `sitemap.xml` hreflang alternatifleriyle birlikte üretilir.
- Schema.org `Organization` + `ProfilePage` JSON-LD her sayfada bulunur; `@id` resmî web sitesindeki kuruluşu işaret eder.
- Bu sayfa ana web sitesini tamamlayıcı bir profil merkezidir; ana sitedeki içerikleri kopyalamak yerine ona yönlendirir.
