# İŞ YATIRIM BIST Screener

Borsa İstanbul hisseleri için İş Yatırım şirket sayfalarını tarayan, finansal verileri birleştiren ve skorlayarak Excel/JSON raporu üreten otomasyon projesi.

## Proje özeti

Bu proje şunları yapar:
- BIST evrenini veya temettü odaklı evreni tarar
- İş Yatırım şirket kartlarından analist önerisi, hedef fiyat, çarpanlar ve finansal özetleri çeker
- Her hisse için 0–100 arası bir skor hesaplar
- Hisseleri BUY / WATCH / AVOID olarak sınıflandırır
- Excel raporu ve JSON özet üretir
- İsteğe bağlı olarak Telegram’a gönderir
- GitHub Actions ile zamanlanmış olarak çalışabilir

## Çıktılar

Ana çıktı dosyaları:
- `bist_genel_analiz_raporu.xlsx`
- `bist_genel_analiz_raporu.json`

Excel çalışma kitabı şu sayfaları içerir:
- `Analysis`
- `Buy_List`
- `Raw_Companies`
- `Notes`

## Hızlı başlangıç

Kurulum sonrası tüm BIST için çalıştırmak için:

```bash
python isyatirim_analiz.py --universe bist --output bist_genel_analiz_raporu.xlsx
```

Telegram’a da göndermek için:

```bash
python isyatirim_analiz.py --universe bist --telegram
```

Belirli hisselerle çalıştırmak için:

```bash
python isyatirim_analiz.py --tickers BIMAS,ASELS,THYAO
```

## GitHub Actions

Depoya bir workflow eklendi. Varsayılan davranış:
- manuel tetikleme (`workflow_dispatch`)
- hafta içi planlı çalışma (`schedule`)
- çıktı artifact olarak yüklenir
- Telegram secret’ları tanımlıysa rapor Telegram’a da gönderilir

## Repo yapısı

- `isyatirim_analiz.py` — ana analiz motoru
- `temettu_analizi_workflow.py` — geriye uyumluluk sarmalayıcısı
- `details1.md` — ayrıntılı wiki
- `skills/temettu-analizi/SKILL.md` — Hermes skill dokümantasyonu
- `requirements.txt` — bağımlılıklar
- `Makefile` — yardımcı komutlar

## Notlar

- Bu araç yatırım tavsiyesi değildir.
- Veriler üçüncü taraf web sayfalarından çekilir; sayfa yapısı değişirse parser güncellenmelidir.
- BIST evreni geniş olduğu için tam tarama birkaç dakika sürebilir.
