# İş Yatırım Analiz Workflow

BIST temettü takvimi ile İş Yatırım şirket sayfası verilerini birleştirip Excel raporu ve alım listesi üreten üretim odaklı workflow.

## Neler yapar?

- Midas temettü takviminden yaklaşan temettüleri çeker
- Ticker listesini tekilleştirir
- Her ticker için İş Yatırım şirket sayfasını analiz eder
- Şirket adı, sektör, öneri, hedef fiyat, çarpanlar ve özet finansalları ekler
- Temettü verimi ve büyüme analizleri üretir
- Skorlayıp alım listesi oluşturur
- Excel raporu ve JSON özet üretir
- İsteğe bağlı olarak Telegram’a gönderir

## Üretim kullanımı

En kısa komut:

```bash
make telegram
```

Dosya üretmek için:

```bash
make run
```

Belirli tickers ile çalıştırmak için:

```bash
make run TICKERS=ASUZU,BIMAS,ASELS
```

Özel dosya adı vermek için:

```bash
make run OUT=rapor.xlsx
```

## Manuel kullanım

```bash
./.venv/bin/python isyatirim_analiz.py --output isyatirim_analiz_raporu.xlsx
```

Telegram’a gönderim:

```bash
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
./.venv/bin/python isyatirim_analiz.py --telegram
```

## GitHub Actions

Bu repoda şu an hazır bir workflow dosyası yok. İstersen bir sonraki adımda cron, artifact ve Telegram gönderimi için ekleyebilirim.

Yerelde `.env.example` dosyası var.

Kopyalayıp doldurabilirsin:

```bash
cp .env.example .env
```

## Workbook sayfaları

- `Analysis`
- `Buy_List`
- `Raw_Companies`
- `Notes`

## Repo yapısı

- `isyatirim_analiz.py` — ana çalışma kodu
- `temettu_analizi_workflow.py` — geriye uyumluluk için giriş sarmalayıcısı
- `skills/temettu-analizi/SKILL.md` — Hermes skill tanımı
- `requirements.txt` — kurulum bağımlılıkları
- `Makefile` — tek komutla çalışma

## Notlar

- İş Yatırım verileri şirket sayfasından okunur.
- Temettü verimi ve finansal skor, sayfadaki mevcut verilerden türetilir.
- Bu puanlama yaklaşık bir tarama aracıdır; resmi yatırım tavsiyesi değildir.
- Tablolar değişirse parser güncellenmelidir.
