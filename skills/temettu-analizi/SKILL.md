---
name: temettu-analizi
summary: Run the BIST dividend workflow that combines Midas dividend calendar data with Fintables company analysis, exports an Excel report, and can send it to Telegram.
---

# Temettü Analizi

## Ne zaman kullanılır

- Kullanıcı güncel BIST temettü analizi isterse
- Midas temettü takvimi ile Fintables şirket verileri birleştirilecekse
- Excel raporu üretilecekse
- Sonuç Telegram’a gönderilecekse

## Workflow

1. Midas temettü takvimini çek.
2. Bugünden itibaren gelen temettüleri al.
3. Aynı ticker için birden fazla kayıt varsa en erken onaylı ödeme tarihini tut.
4. Ticker listesini tekilleştir.
5. Her ticker için Fintables şirket sayfasına git.
6. Şu alanları al:
   - şirket adı
   - sektör
   - satışlar
   - FAVÖK
   - net dönem karı
   - F/K
   - PD/DD
   - free float
   - piyasa değeri
   - ödenmiş sermaye
7. Fintables market cap / sermaye ile yaklaşık fiyat hesapla.
8. Net temettü / yaklaşık fiyat ile temettü verimini hesapla.
9. Excel üret:
   - Dividend_Analysis
   - Top10_Yield
   - Midas_Raw
   - Notes
10. `--telegram` verilmişse Telegram botu ile dosyayı gönder.

## Tek komutla çalışma

Repo kökünde:

```bash
make run
make telegram
```

İstersen Python scriptini doğrudan da çalıştırabilirsin:

```bash
python3 -m pip install -r requirements.txt
python3 temettu_analizi_workflow.py --output temettu_analiz_raporu.xlsx
python3 temettu_analizi_workflow.py --telegram
```

## GitHub Actions ve secrets

Repo’daki workflow `workflow_dispatch` ve cron ile çalışır.
Gerekli secrets:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Bunlar yoksa workflow dosyayı üretir ama Telegram’a gönderemez.

## Pitfalls

- Fintables sayfalarında tablo yapısı değişebilir.
- Piyasa değeri ve sermaye ile hesaplanan fiyat yaklaşık değerdir.
- Telegram gönderimi için bot yetkileri gerekir.
