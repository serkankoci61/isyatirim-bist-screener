# İş Yatırım + BIST Analiz Sistemi Wiki

## 1. Sistem ne yapıyor?

Bu sistem, Borsa İstanbul (BIST) hisseleri için İş Yatırım şirket sayfalarını ve temettü verilerini birleştirip otomatik bir analiz çıktısı üretir.

Temel amaçlar:
- BIST hisselerini bir evren olarak taramak
- Her hisse için İş Yatırım sayfasından temel analist ve finansal verileri çekmek
- Skor bazlı bir karar üretmek: BUY / WATCH / AVOID
- Çıktıyı Excel raporu halinde oluşturmak
- İstenirse Telegram’a göndermek

Sistemin iki ana çalışma modu vardır:
- Midas temettü evreniyle çalışan klasik mod
- Tüm BIST hisselerini tarayan `--universe bist` modu

## 2. Veri kaynakları

Sistem şu dış kaynakları kullanır:

- Midas temettü takvimi
  - Yaklaşan temettü ödemeleri için ticker listesi ve temettü bilgisi sağlar
- StockAnalysis Borsa İstanbul liste sayfası
  - BIST’te listelenen şirketlerin ticker listesini çıkarır
- İş Yatırım şirket kartı sayfası
  - Analist önerisi, hedef fiyat, çarpanlar ve özet finansal veriler alınır

Not: Bu sistem resmi yatırım tavsiyesi üretmez. Ekrandaki verilerden kural tabanlı bir ön eleme çıkarır.

## 3. Çalışma mantığı

### 3.1 Ticker evreni oluşturma

İki yöntem vardır:

#### Midas modu
- Midas temettü sayfası taranır
- Yaklaşan temettü ödemesi olan hisseler alınır
- Bunlar İş Yatırım sayfası ile eşleştirilir

#### BIST modu
- Borsa İstanbul’daki tüm listelenen hisseler çekilir
- Her ticker için İş Yatırım şirket kartı alınır
- Böylece evrende temettü filtresi olmadan tam BIST taraması yapılır

### 3.2 Şirket sayfası tarama

Her ticker için şu veriler yakalanır:
- Şirket adı
- Analist önerisi
- Son öneri tarihi
- Hedef fiyat
- Getiri potansiyeli
- F/K
- FD/FAVÖK
- PD/DD
- Satışlar
- FAVÖK
- Net kâr
- Bir önceki dönem kıyasları
- Temettü verimi
- Yabancı oranı
- Sektör / faaliyet alanı / kuruluş tarihi / iletişim bilgileri

### 3.3 Skorlama

Sistem her şirket için 0–100 arası bir skor üretir.

Skor bileşenleri:
- İş Yatırım tavsiyesi
- Getiri potansiyeli
- F/K seviyesi
- FD/FAVÖK seviyesi
- PD/DD seviyesi
- Gelir büyümesi
- Net kâr büyümesi
- FAVÖK büyümesi
- Yaklaşan temettü verimi
- Yabancı oranı

Karar eşikleri:
- 65 ve üzeri: BUY
- 45–64: WATCH
- 45 altı: AVOID

## 4. Üretilen çıktılar

Sistem çalışınca iki ana çıktı üretir:

### Excel raporu
Dosya örneği:
- `bist_genel_analiz_raporu.xlsx`
- veya zaman damgalı isimler

Excel içinde şu sayfalar vardır:
- `Analysis`
- `Buy_List`
- `Raw_Companies`
- `Notes`

### JSON özet
Excel’e paralel olarak JSON dosyası da üretilir.
Bu, başka sistemlere veri beslemek için kullanışlıdır.

## 5. Excel sayfalarının amacı

### Analysis
Tüm analiz edilen şirketlerin ana listesi.

### Buy_List
BUY olarak işaretlenen şirketler.

### Raw_Companies
Ham şirket verilerinin JSON gömülü hali.
Bu sayfa debug ve iz sürme için çok önemlidir.

### Notes
Run tarihi, veri kaynakları, karar kuralı ve sistem açıklamaları.

## 6. Komut satırı kullanımı

### Klasik mod
```bash
python isyatirim_analiz.py --output rapor.xlsx
```

### Telegram’a da gönder
```bash
python isyatirim_analiz.py --telegram
```

### Sadece belirli hisseler
```bash
python isyatirim_analiz.py --tickers BIMAS,ASELS,THYAO
```

### Tüm BIST evreni
```bash
python isyatirim_analiz.py --universe bist --output bist_genel_analiz_raporu.xlsx
```

### Daha yüksek paralellik
```bash
python isyatirim_analiz.py --universe bist --max-workers 8
```

## 7. Telegram entegrasyonu

Telegram gönderimi için ortam değişkenleri gerekir:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Sistem çıktı dosyasını Telegram’da doküman olarak gönderir.
Bu özellik hem klasör düzeyinde rapor almak hem de sonuçları anında telefona düşürmek için uygundur.

## 8. Performans ve ölçek

BIST modu geniş evren taradığı için daha yoğundur.
Bu nedenle:
- Ağ hataları olabilir
- İş Yatırım sayfaları tek tek fetch edilir
- Bazı tickers boş veya hatalı veri döndürebilir
- Yönetim amacıyla çoklu iş parçacığı (ThreadPoolExecutor) kullanılır

Bu yapı küçük veri setlerinde hızlıdır, ancak BIST genel taraması için birkaç dakika sürebilir.

## 9. Hata dayanıklılığı

Sistem şu tür sorunlara karşı toleranslıdır:
- Bir hissenin sayfası erişilemezse tüm iş durmaz
- Hatalı tekil şirket verisi diğerlerini engellemez
- Fetch başarısızlıkları uyarı olarak yazdırılır
- Excel ve JSON ayrı ayrı üretildiği için biri bozulsa diğeri yine alınabilir

## 10. Kod yapısı

Ana dosyalar:
- `isyatirim_analiz.py`
  - ana veri toplama, parse, skor, export
- `temettu_analizi_workflow.py`
  - geriye uyumluluk için giriş sarmalayıcısı
- `README.md`
  - kısa kullanım özeti
- `details1.md`
  - bu wiki dokümanı

## 11. Teknik akış

1. Argümanlar okunur
2. Evren seçilir: Midas veya BIST
3. Ticker listesi oluşturulur
4. Her ticker için İş Yatırım sayfası çekilir
5. HTML içindeki tablolar parse edilir
6. Finansal ve analist verileri normalize edilir
7. Skor hesaplanır
8. Excel ve JSON üretilir
9. İsteğe bağlı olarak Telegram’a gönderilir

## 12. Kullanım senaryoları

### Hızlı tarama
Bir yatırımcı “hangi hisseler öne çıkıyor?” sorusuna cevap almak istiyorsa BUY listesine bakabilir.

### Araştırma çalışma kitabı
Excel dosyası, manuel yatırım araştırması için başlangıç noktası olarak kullanılabilir.

### Telegram otomasyonu
Raporun direkt Telegram’a gelmesi, günlük kontrolü kolaylaştırır.

### Toplu BIST taraması
Yeni sürümde tüm BIST hisseleri için çalışan mod sayesinde evren daralmadan tarama yapılabilir.

## 13. Sonuçların nasıl yorumlanacağı

- BUY: Görece güçlü adaylar, ama yine de kesin alım anlamına gelmez
- WATCH: Takip listesi; veri veya değerleme karmaşık olabilir
- AVOID: Sistem puanına göre daha zayıf görünen hisseler

Önemli: Bu puanlama mekanik bir filtreleme aracıdır. Temel analiz, haber akışı, bilanço kalitesi, sektör dinamikleri ve risk iştahı ayrıca değerlendirilmelidir.

## 14. Yayınlama / GitHub

Repo yeni isimle GitHub’a yüklenebilir.
Önerilen repo adı formatı:
- `bist-isyatirim-analiz`
- `bist-genel-analiz`
- `isyatirim-bist-screener`

Bu doküman, repo ilk açılışında kullanıcıya sistemin ne yaptığını anlamak için tasarlanmıştır.

## 15. Genişletme fikirleri

Gelecekte eklenebilecekler:
- GitHub Actions ile zamanlanmış çalıştırma
- Telegram’a sadece BUY listesini gönderme
- Sektör bazlı filtreleme
- Fiyat geçmişi ile teknik analiz entegrasyonu
- Sonuçları CSV/Parquet olarak da dışa aktarma
- Web arayüzü veya dashboard

## 16. Kısa özet

Bu sistem:
- BIST veya Midas evrenini tarar
- İş Yatırım verilerini toplar
- Kural bazlı skor üretir
- Excel ve JSON çıktısı oluşturur
- İstenirse Telegram’a yollar
- Analiz sürecini tek komutla otomatikleştirir
