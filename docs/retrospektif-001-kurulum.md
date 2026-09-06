# Kurulum Retrospektifi — 5-6 Eylül 2026

**Kapsam:** `evalstat` ve `tr-speech-eval` projelerinin ilk iki günü. Analiz
planı 001'in taslaktan §2'si kapanmış hâle gelmesine kadar.

**Neden tutuluyor:** Bu belge bir ilerleme raporu değil. Bir ölçüm çalışması
kurulurken yapılan hataların ve onları yakalayan mekanizmaların kaydı. Çalışmanın
konusu zaten "AI çıktısı ne zaman güvenilir" olduğu için, kurulum sürecinin
kendisi ilk veri kümesi sayılır.

---

## 1. Ana bulgu

Dokuz hata kaydedildi. Kronolojik olarak bakıldığında rastgele görünüyorlar.
**Yakalayan mekanizmaya göre gruplandığında dört ayrı sınıf çıkıyor** — ve her
sınıf yalnızca kendi mekanizmasıyla yakalanabiliyor.

| Mekanizma | Yakaladığı hata sınıfı | Vaka |
|---|---|---|
| Çapraz kontrol (AI → AI) | İç tutarsızlık, matematiksel ilişki hatası | 1, 4 |
| İnsan düzeltmesi | Niyet okuma hatası, odak kayması | 2 |
| Uygulamaya geçmek | Uygulanamaz tasarım varsayımı | 6, 8 |
| Dış otoriteye sormak | Paylaşılan eskimiş bilgi | 5, 9 |
| **Hiçbiri (geç yakalandı)** | **Her iki tarafın ortak kör noktası** | **3, 7** |

Son satır en önemlisi. İki bağımsız AI'ın **aynı anda** kaçırdığı hatalar var.
Çapraz kontrol bunları çözmüyor.

---

## 2. Vakalar

### Vaka 1 — Wilcoxon = işaret testi
**Kim yaptı:** Sohbet asistanı.
Üç seviyeli tercih verisi (A/eşit/B) için "işaret testi veya Wilcoxon" önerildi.
Wilcoxon signed-rank bu veride işaret testine dejenere olur: sıfırlar atıldıktan
sonra tüm mutlak farklar 1'dir, sıralar berabere kalır. İki isim, tek hesap.
**Kim yakaladı:** Claude Code.
**Neden kendi kendine yakalanamazdı:** Aynı yanlış varsayım hem cevabı hem de
kontrolü üretiyordu. Öneri yazılırken yanlış olduğu bilinmiyordu.
**Sonuç:** Ölçek 5 seviyeye çıkarma kararı `[DECIDE]` olarak plana girdi.

### Vaka 2 — Örtük hedef müdahalesi
**Kim yaptı:** Sohbet asistanı.
Kullanıcının merak sorularının ("kendini kontrol etsen kusursuz olur muydun",
"bu projeyi tek başına yapabilir misin") altında bir endişe olduğu çıkarımı
yapıldı ve cevaba istenmemiş bir moral bölümü eklendi. Cevabın yaklaşık üçte
biri kullanıcının sormadığı bir soruyu cevaplıyordu.
**Kim yakaladı:** Kullanıcı.
**Hatanın yapısı:** Tek hipotez desteklendi, rakip hipotez ("bu kişi sadece
merak ediyor") hiç yoklanmadı. İkinci hata: çıkarım açık edilmedi, doğruymuş
gibi kullanıldı.
**Sonuç:** `docs/ideas/fikir-002-ortuk-hedef-mudahalesi.md` — bu vaka ikinci
çalışmanın araştırma sorusuna dönüştü.

### Vaka 3 — Körleme eksikliği
**Kim yaptı:** İkisi de.
İlk tasarımda çalışmayı kuran, birincil ölçümü yapan ve belirli bir sonucu
bekleyen aynı kişiydi. Model kimliği puanlayana açıktı.
**Kim yakaladı:** Claude Code — ama ilk turda değil, tasarım bir kez yazıldıktan
sonra.
**Neden önemli:** Sohbet asistanı bu hatayı hiç görmedi, oysa çalışmanın
geçerliliğini tek başına yok edecek türden. **Ortak kör nokta örneği.**
**Sonuç:** Zorunlu körleme §4.3'e girdi; `blinding.py` bunu uyguluyor.

### Vaka 4 — Bloke sıralaması
**Kim yaptı:** Sohbet asistanı.
"Sıradaki adım 30 örneğin kör okunması" denildi. Oysa o adımın kendisi bloke:
kör okuma için önce korpus, ASR çıktısı ve iki modelin post-edit çıktısı
gerekiyor. Rubrik boru hattını, boru hattı rubriği bekliyordu.
**Kim yakaladı:** Sohbet asistanı (kendi hatasını, bir tur sonra).
**Neden geç fark edildi:** Özetin özetine yorum yapılıyordu; bağımlılık sırası
özette görünmüyor.
**Sonuç:** Döngü kırıldı — boru hattının rubrikten bağımsız yarısı yazıldı.

### Vaka 5 — Model kimliği çelişkisi
**Kim yaptı:** İkisi de.
Claude Code tarihsiz kimliğin doğru olduğunu söyledi, sohbet asistanının bilgisi
tarihli formu gösteriyordu. İkisi de emindi.
**Kim yakaladı:** Kimse — çelişki görünür oldu, doğrusu ikisinde de yoktu.
**Sınıf farkı:** Bu, çapraz kontrolle **çözülemeyen** hata sınıfı. İki tarafın
bilgisi aynı kaynaktan geliyor ve ikisi de eskimiş olabilir. Yanlış olan
cevaplardan biri değil, ikisinin de dış doğrulama yapmadan konuşmuş olması.
**Sonuç:** Model kimlikleri koşu anında Models API'den okunup manifest'e
yazılacak. Hiçbir ezber manifest'e girmiyor.

### Vaka 6 — Uygulanamaz tasarım satırı
**Kim yaptı:** Tasarım (ikisi de onayladı).
Plan §2 "her iki sistem için aynı temperature, tüm item'lar için sabit"
diyordu. Sonnet 5 sampling parametrelerini reddediyor (400) ve adaptif düşünme
varsayılan olarak açık. Yani "aynı ayar" fiziksel olarak kurulamaz; varsayılan
karşılaştırması aslında "akıl yürüten sistem vs yürütmeyen sistem".
**Kim yakaladı:** Claude Code — tasarım tartışırken değil, **üretim adımını
yazmaya çalışırken.**
**Sonuç:** Tahmin hedefi (estimand) yeniden tanımlandı: model karşılaştırması
değil, **sistem karşılaştırması**. Hiçbir modelde sıcaklık gönderilmiyor.
Yapılandırma farkı gizlenmiyor, ilan ediliyor. Tekrar-koşu varyans kontrolü
koşullu olmaktan çıkıp iki kollu ve zorunlu oldu. Başlık "System A (Haiku 4.5)
vs System B (Sonnet 5), default configurations" olarak değişti — "Sonnet daha
iyi çünkü daha büyük" cümlesini yapısal olarak kapatmak için.

### Vaka 7 — İki gün süren bloke
**Kim yaptı:** Süreç.
Korpus ve ASR kaynağı kararı 5 Eylül'den beri açık. Bu iki gün boyunca
yapılan her iş — ortam kurulumu, paket iskeleti, körleme modülü, 15 test,
plan revizyonu — asıl darboğazın etrafından dolaştı. Hepsi meşru işti; hiçbiri
bloke edicileri çözmedi.
**Kim yakaladı:** Sohbet asistanı, gün sonunda.
**Ders:** Devredilemez kararlar, devredilebilir işlerin arkasına saklanır. İkisi
de "ilerleme" gibi görünür ve ikisi de commit üretir. AI yardımı bu eğilimi
artırıyor, çünkü devredilebilir işin maliyetini düşürüyor.

### Vaka 8 — Plan uygulamada çözüldü
**Kim yaptı:** —
§2, iki tur tasarım tartışmasıyla kapanmadı. Kod yazılırken çıkan bir API
kısıtıyla kapandı (Vaka 6).
**Ders:** Tasarımı mükemmelleştirmek için uygulamayı geciktirmek, tasarım
hatalarını gizler. Bazı varsayımlar ancak koda dönüştürülünce yanlışlanabilir.

### Vaka 9 — TEDx önerisi kaynağa bakılmadan verildi
**Kim yaptı:** İkisi de.
Korpus seçenekleri karşılaştırılırken TEDx "doğal konuşma, iyi ses kalitesi,
nötr içerik; lisansı tek tek kontrol etmeniz gerekir" diye sunuldu ve kaynak
kararına girdi. Lisans, kontrol edilmesi gereken bir ayrıntı olarak
**işaretlendi ama kontrol edilmedi.** Oysa TED'in kendi kullanım politikası
CC BY-NC-ND ve ND kısıtı çalışmanın merkezindeki işlemi doğrudan yasaklıyor:
"kısaltılmış sürüm veya klip paylaşılamaz", "transkriptlerin telifi TED'e ait".
Yani TEDx baştan elenmesi gereken bir seçenekti ve bir gün boyunca planda karar
verilmiş kaynak olarak durdu.
**Kim yakaladı:** Dış doğrulama — politika metni okunduğunda.
**Neden çapraz kontrol yakalamadı:** İki taraf da TEDx'i makul buldu. Vaka 5'te
en azından bir çelişki vardı ve çelişki dikkat çekti; burada çelişki bile yoktu.
**Tam mutabakat, ortak hata** — ve mutabakat, doğruluğun kanıtı gibi göründüğü
için daha da sinsi.
**Sınıf:** Vaka 5 ile aynı. Paylaşılan eksik bilgi; yalnızca dış otoriteye
sorarak yakalanabilir.
**Maliyet:** Bir gün. Fark edilmeseydi ya yayınlanamayan bir veri seti ya da
lisans ihlali üretecekti.
**Sonuç:** Korpus kendi kayıtlarına döndü (§3), ve kural genelleşti: dışarıdan
doğrulanabilir her karar, karara girmeden önce kaynağından okunur. "Sonra
kontrol edersin" diye işaretlenen şey kontrol edilmiyor.

---

## 3. Çıkarımlar

**1. Çapraz kontrol çalışıyor ama sınırlı.**
İki bağımsız AI bağlamı arasında çıktı taşımak gerçek hata yakaladı (Vaka 1, 4).
Ama ortak kör nokta (Vaka 3, 7) ve paylaşılan eskimiş bilgi (Vaka 5) bu yöntemle
yakalanmıyor. Çapraz kontrol, dış doğrulamanın ve insan yargısının yerine
geçmiyor.

**2. En pahalı hata sınıfı: ikisinin de kaçırdığı.**
Körleme eksikliği çalışmanın geçerliliğini tek başına yok ederdi ve iki AI'dan
biri tarafından, geç yakalandı. Bu sınıf için tek savunma, **kontrol listesi
gibi mekanik araçlar** — akıl yürütme değil.

**3. Aktarım kaybı gerçek.**
Sohbet asistanı iki gün boyunca 302 satırlık planın kendisini değil, özetini
gördü. Vaka 4 doğrudan bunun sonucu. Kritik dosyaların ham metni taşınmalı.

**4. Hız devredilebilir işte, yavaşlık devredilemez işte.**
İki günde ortam, iki paket, 17 test, körleme modülü ve bir plan revizyonu
tamamlandı. Aynı iki günde tek bir devredilemez karar (korpus) ilerlemedi.
Oran bozuk ve bozukluğun yönü sistematik.

---

## 4. Somut durum (6 Eylül sonu)

**Tamamlanan:** Ortam (Python 3.14.5, iki venv, pytest+ruff+mypy temiz).
`evalstat` iskeleti. `tr-speech-eval`: `blinding.py`, `burned.py`, 15 test.
Plan §2 kapandı.

**Açık `[DECIDE]`:** 26.

> **Bu bölüm 6 Eylül akşamının kaydıdır ve kasten güncellenmemiştir.** 7 Eylül'de
> 1-3 kapandı ve buradaki korpus önerisi Vaka 9 olarak geri döndü — TEDx lisans
> gerekçesiyle elendi, kaynak kendi kayıtları oldu.

**Bloke ediciler — hepsi devredilemez:**
1. Korpus kaynağı (öneri: TEDx/podcast ile başla, kendi kaydını paralel biriktir)
2. ASR seçimi (tek ASR sabitlenip manifest'e yazılacak; hangisi olduğu çalışmanın
   sorusu değil, ama sabit olmalı)
3. 300 örnek kaç ayrı kayıttan gelecek (kümelenme kararı buna bağlı)
4. Rubrik çapaları (1-3 çözülmeden başlanamaz)

**Commit durumu:** Üç ayrı commit önerildi, plan revizyonu sona bırakılacak —
`analysis-plan-001-frozen` etiketinin neyi dondurduğu belirsizleşmesin diye.
