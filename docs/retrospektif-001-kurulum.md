# Kurulum Retrospektifi — 5-6 Eylül 2026

**Kapsam:** `evalstat` ve `tr-speech-eval` projelerinin ilk iki günü. Analiz
planı 001'in taslaktan §2'si kapanmış hâle gelmesine kadar. Vaka 10, 11 ve 12
8 Eylül'de eklendi; kayıt kapatılmadı çünkü üçü de yeni bilgi taşıyordu — biri
yeni bir hata sınıfı, biri var olan bir sınıfın örüntüye dönüştüğünü, biri de bir
denetimin kendi sorusunun dışını görmediğini.

**Neden tutuluyor:** Bu belge bir ilerleme raporu değil. Bir ölçüm çalışması
kurulurken yapılan hataların ve onları yakalayan mekanizmaların kaydı. Çalışmanın
konusu zaten "AI çıktısı ne zaman güvenilir" olduğu için, kurulum sürecinin
kendisi ilk veri kümesi sayılır.

---

## 1. Ana bulgu

On iki vaka kaydedildi. Kronolojik olarak bakıldığında rastgele görünüyorlar.
**Yakalayan mekanizmaya göre gruplandığında sınıflar çıkıyor** — ve her sınıf
yalnızca kendi mekanizmasıyla yakalanabiliyor.

| Mekanizma | Yakaladığı sınıf | Vaka |
|---|---|---|
| Çapraz kontrol (AI → AI) | İç tutarsızlık, matematiksel ilişki hatası | 1, 4 |
| İnsan düzeltmesi | Niyet okuma hatası, odak kayması | 2 |
| **Uygulamaya geçmek** | **Uygulanamaz veya eksik tasarım varsayımı** | **6, 8, 11** |
| Dış otoriteye sormak | Paylaşılan eskimiş bilgi | 5, 9, 11 |
| Hiçbiri (geç yakalandı) | Her iki tarafın ortak kör noktası | 3, 7 |
| **Sınıf dışı** | **Doğru kararın maliyeti** | **10** |
| **Başka soruyla yapılan tarama** | **Önceki denetimin sorusuna girmeyen hata** | **12** |

Üç şey değişti.

**Birincisi: "uygulamaya geçmek" artık üç vakalı ve örüntü sayılır.** 6, 8 ve 11
aynı yapıya sahip: bir tasarım varsayımı tasarım turlarında yanlışlanamadı,
uygulama yoluna girilince yanlışlandı. Üç örnek, tek tek anlatılacak vaka
olmaktan çıkıp **yöntem hâline geliyor**: bir varsayımı sınamanın en ucuz yolu
onu tartışmak değil, onu uygulanabilir en küçük adıma dönüştürmek. Vaka 11 ayrıca
iki mekanizmaya birden ait — kaynağa bakmak *ve* uygulamaya geçmek — çünkü
sorulacak soruyu uygulama üretti, cevabı kaynak verdi.

**İkincisi: Vaka 10 önceki dokuzun hiçbirine benzemiyor.** Onların hepsi
"yanlıştı, düzeltildi" idi: yanlış test önerisi, kaçırılan körleme, eskimiş model
kimliği, okunmamış lisans. Vaka 10'da **yanlış bir şey yok.** Kendi kaydını
kullanma kararı hâlâ lisans açısından en iyi karar. Terk edilme sebebi hatalı
olması değil, **pahalı** olması — ve maliyeti karar verilirken görünmüyordu. Bu
yüzden ayrı satırda: "doğru ama pahalı" bir kararın terk edilmesi, bir hatanın
düzeltilmesiyle aynı şey değil ve aynı mekanizmayla yakalanmıyor.

**Üçüncüsü: Vaka 12 hatayla değil, onu arayan mekanizmayla ilgili.** Önceki on
bir vakada yakalayan mekanizma hatayı arıyordu. Vaka 12'de hatayı bulan tarama
başka bir şey arıyordu; hatanın durduğu alan bir önceki taramada okunmuş ve
"temiz" raporlanmıştı. Rapor yanlış değildi — sorulan soruya göre temizdi. Ayrı
satırda olmasının sebebi bu: bir alanı bir sebeple denetlemek, onu başka bir
sebeple denetlemiş saymıyor.

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

### Vaka 10 — Korpus yolunun gerçek maliyeti uygulamada göründü
**Kim yaptı:** Tasarım (ikisi de onayladı).
Vaka 9'dan sonra korpus "kendi kayıtlarım" oldu ve bu, lisans açısından
kusursuz bir karardı: hakları tutuyorsun, ND yok, yeniden dağıtım serbest,
konuşmacı üstverisi tanımlı. Karar, **kendi seçim kriteri içinde** doğruydu ve o
kriter lisanstı.
Görünmeyen şey maliyetin ikinci bileşeniydi: insan denekli kayıt etik kurul
onayı gerektiriyor ve o onay haftalar sürüyor, tarihi de belirsiz. Yani karar
lisans riskini sıfırladı ve yerine bir **takvim riski** koydu — ama takvim riski
karar verilirken hiç tartılmadı, çünkü lisans tartışmasının içinde böyle bir
terim yoktu.
**Kim yakaladı:** Uygulama yoluna girmek. Tasarım turunda değil, 57 konuşmacılık
toplama planı gerçek bir takvime oturtulmaya çalışılırken.
**Neden tasarım turunda yakalanamazdı:** Seçenekler bir eksende karşılaştırıldı
(lisans güvenliği), kararın maliyeti başka bir eksende çıktı (onay süresi).
Doğru eksende doğru cevap verildi. Yanlış olan cevap değil, karşılaştırmanın tek
eksenli olmasıydı — ve bir eksenin eksik olduğu, ancak o eksen bağlayıcı hâle
gelince görülüyor.
**Sonuç:** Çalışma iki kola ayrıldı (§3.0). Kol 1 sentetik bozulmayla açık
lisanslı Türkçe metinden, Kol 2 gerçek ASR çıktısıyla kendi kayıtlarından. Kol 2
iptal değil ertelendi ve tasarımı **şimdi donduruluyor** — onay geldiğinde
yazılacak bir tasarım, Kol 1'in sonuçlarını görmüş bir tasarım olurdu ve ön kayıt
diye bir şey kalmazdı. `segmentation.py`, Whisper kararı, kayıt uzunluğu ve VAD
kararları rafa kalktı, silinmedi.
**Sınıf: önceki dokuzun hiçbiri değil.** Vaka 1-9'un hepsi "yanlıştı,
düzeltildi" biçimindeydi — yanlış test, kaçırılan körleme, eskimiş model kimliği,
okunmamış lisans. Burada düzeltilen bir yanlış yok. Kendi kaydını kullanma kararı
hâlâ lisans ekseninde en iyi karar ve o eksende hâlâ savunulabilir; Kol 2 olarak
planda duruyor ve onay gelince aynen uygulanacak. Terk edilme sebebi hatalı
olması değil, **pahalı** olması.
Vaka 6 ve 8'e benzeyen tek yanı yakalanma anı: ikisinde de uygulama yoluna
girmek gerekti. Ama orada yanlışlanan **varsayımdı**, burada yanlışlanan
**maliyet tahmini**. Bir tasarım kararının doğruluğu ile uygulanabilirliği ayrı
şeyler, ve ikisi ayrı anlarda ortaya çıkıyor.
**Kaydedilmeye değer olan:** çalışmayı durduran şey bir hata değildi. Hata
avlayan bir retrospektif, bunu hiç görmezdi.

### Vaka 11 — Whisper zaten noktalama üretiyor, Kol 1 tasarımı buna göre değişti
**Kim yaptı:** Tasarım (ikisi de onayladı).
Kol 1 kurgusu şuydu: temiz metinden noktalama silinir, büyük harfler düşürülür,
sayılar sözlü forma çevrilir; post-edit görevi bunu geri kurmaktır. Kurgu kendi
içinde tutarlıydı ve iki taraf da makul buldu.
Doğrulama sırasında Whisper `large-v3`'ün **zaten noktalamalı, büyük harfli,
rakamlı çıktı verdiği** görüldü — bilinen zaafı yokluk değil *tutarsızlık*, ve
davranış dile göre değişiyor. Yani Kol 1 noktalamayı tamamen silseydi iki kol
**farklı görev** sunacaktı: Kol 1 sıfırdan restorasyon, Kol 2 onarım. S3
(eşdeğerlik sorusu) iki farklı görevi karşılaştırıp farkı yanlış nedene yazacaktı
— ve fark bulunsaydı "sentetik bozulma gerçeği temsil etmiyor" diye okunacaktı,
oysa sebep tasarımın kendisi olacaktı.
**Kim yakaladı:** Claude Code — ama tasarım tartışırken değil, **bozulma
protokolü seçenekleri yazılmaya çalışılırken.** "Hangi bozulmayı uygulayacağız"
sorusu, "girdi zaten neye benziyor" sorusunu zorunlu kıldı. Cevap kaynaktan
okununca çıktı.
**Neden tasarım turunda yakalanamazdı:** Varsayım hiç dile getirilmedi. "ASR
çıktısı ham ve noktalamasızdır" cümlesi planın hiçbir yerinde yazmıyordu; o
kadar temel görülüyordu ki tartışılacak bir şey sayılmadı. Yazılmayan varsayım
kontrol edilmez.
**Sonuç:** İki katmanlı. (1) Çıktı biçimi artık **doğrulama kalemi**: rubrik
dondurulmadan önce seçilen checkpoint'in gerçek çıktısı incelenip manifest'e
yazılıyor. (2) Bozulma protokolü D4'e (TTS → ASR turu) döndü — o kurguda her iki
kolun girdisi de aynı tanıyıcının çıktısı olduğu için biçim eşleşmesi taklit
edilmiyor, **yapıdan geliyor.**
**Sınıf:** Vaka 6 ve 8 ile aynı — uygulamaya geçince yanlışlanan tasarım
varsayımı. Ama bu **üçüncü örnek**, yani artık tekil vaka değil örüntü; §1'deki
çıkarım bu yüzden yeniden yazıldı.

### Vaka 12 — Kırık proje adresi gizlilik taramasının içinden geçti
**Kim yaptı:** Claude Code, ilk commit'te.
`evalstat/pyproject.toml`'un `[project.urls]` bölümü `Homepage` ve `Issues`
alanlarını var olmayan bir depoya yönlendirdi: adresin hesap kısmına GitHub
hesabı değil **yerel makinenin kullanıcı adı** yazılmıştı ve o adreste hiçbir
zaman bir depo olmadı. Değer bir kaynaktan okunmadı, elde duran isimden
üretildi — üstelik depo henüz yaratılmamıştı, yani okunacak bir kaynak da yoktu.
İki alan da paket metadata'sına giriyor: PyPI'a yayımlansaydı paket
sayfasındaki "Homepage" ve "Issues" bağlantıları 404 verecekti.
**Kim yakaladı:** Claude Code — ama **gizlilik taraması sırasında değil**, ondan
sonra gelen isim eşitlemesi sırasında.
**Neden gizlilik taraması yakalamadı:** Yakalayamazdı. O tarama tüm geçmişte
yazar alanındaki kişisel e-posta adresini arıyordu; tam da bu dosyayı okudu,
adresi on üç commit'ten çıkardı ve **"temiz" raporladı.** Rapor doğruydu —
sorulan soruya göre temizdi. Kırık adres o sorunun içinde değildi. Bir tarama
yalnızca kendi sorusunu cevaplar, ve cevabı "temiz" olduğunda alan denetlenmiş
görünür.
**Sınıf:** Yeni. Aynı alan iki ayrı sebeple denetlenmeliydi — **gizlilik**
(içinde kişisel bir tanımlayıcı var mı) ve **doğruluk** (yazdığı şey gerçek mi).
Biri için tarandığında öteki görünmüyor, üstelik ilk taramanın temiz raporu
ikincinin gereksiz olduğu izlenimini veriyor.
**Maliyet:** Bu kez sıfır; push'tan önce yakalandı.
**Sonuç:** Aynı ailenin iki üyesi bu bölünme sırasında zaten düzeltilmişti:
`requires-python = ">=3.10"` hiçbir testin çalıştırmadığı bir tabanı ilan
ediyordu, `license = { text = "MIT" }` ise var olmayan bir LICENSE dosyasına
dayanıyordu. Üçü de aynı biçimde: **metadata bir şey beyan ediyor ve onu
doğrulayan hiçbir şey yok.** Vaka 9'un kuralı buraya uzanıyor: dışarıdan
doğrulanabilir her alan, yayımdan önce kendi kaynağından okunur — ve bir sebeple
tarandığı için öteki sebeple de tarandı sayılmaz.

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

**4. Bir kararın maliyeti, kendi seçim ekseninde görünmeyebilir.**
Vaka 9 ve 10 aynı kararın iki yarısı. Korpus lisans ekseninde tartışıldı ve o
eksende en güvenli seçenek kazandı; kaybettiren şey hiç tartılmayan takvim
ekseni oldu. Ders, "kendi kaydını seçme" değil: **bir seçenek elenmeden önce,
elenme gerekçesinin hangi eksende olduğunu ve o eksenin tek eksen olup
olmadığını sormak.** Vaka 9'un kuralı (kaynağından doğrula) buna eşlik ediyor
ama yerini tutmuyor — TED'in politikası okunsaydı da etik kurul takvimi
görünmezdi.

**5. Bir varsayımı sınamanın en ucuz yolu, onu tartışmak değil.**
Vaka 6, 8 ve 11 aynı yapıda ve üçü birlikte artık örüntü sayılır: tasarım
turlarında kapanmayan şey, uygulamanın en küçük adımı yazılırken kapandı. Vaka
11'de mekanizma daha da özel — yanlışlayan şey kodun kendisi değil, **kod
yazmaya çalışmanın ürettiği soru** oldu ("girdi zaten neye benziyor?"). Sonuç:
bir tasarım turu, uygulanabilir bir adım üretmeden kapatılmıyor.

**6. Hız devredilebilir işte, yavaşlık devredilemez işte.**
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

---

## 5. 8 Eylül eki — korpus yolu ve bozulma protokolü

Yukarıdaki §4, 6 Eylül akşamının kaydıdır ve kasten güncellenmiyor. Bu ek,
sonrasında ne olduğunu ayrı bir katman olarak yazar.

- **7 Eylül:** Bloke edici 1-3 kapandı. TEDx lisans gerekçesiyle elendi (Vaka 9),
  kaynak kendi kayıtları oldu.
- **8 Eylül (sabah):** Kendi kayıtları yolunun etik kurul onayı gerektirdiği ve
  bunun haftalar sürebileceği ortaya çıktı (Vaka 10). Çalışma iki kola ayrıldı.
  Kol 1 aktif, Kol 2 ertelendi ve tasarımı planda donduruldu.
- **8 Eylül (akşam):** Whisper'ın zaten noktalamalı çıktı verdiği doğrulandı
  (Vaka 11) ve bozulma protokolü **D4**'e karar bağlandı: metin → tereddüt
  enjeksiyonu → TTS → akustik bozulma → 30 sn pencere → Whisper. Kol 1'de ses
  var, insan yok.
- **Değişmeyenler:** körleme, ön kayıt, iki tiyerli ölçüm, kümelenmiş çıkarım,
  hakem doğrulaması, sistem karşılaştırması tahmin hedefi, iki başlık kuralı.
  `blinding.py` ve `burned.py` aynen kullanılıyor.
- **Rafa kalkmadı:** `segmentation.py`, Whisper `large-v3-turbo` kararı, VAD
  eşiği ve kenar kuralı — D4 kararı bunları Kol 1'de **hemen** kullanıma soktu.
  Yalnızca 7 dakikalık kayıt alt sınırı ve konuşmacı toplama Kol 2'ye kaldı.
  Ertelenen şey ses değil, insan denek.
- **Kapanan kararlar:** bozulma protokolü (D4 + D2), kümeleme birimi (makale),
  parça uzunluğu (saniye cinsinden, iki kolda aynı — L1/L2/L3 tartışması
  gereksizleşti), model sürümü kontrolü (X2 köprü seti), rubrik aktarımı
  (kollar arası aynen, revize yok), S3 testi (TOST), mutlak tiyer alt kümesi
  (40, keşifsel etiketli), yayın lisansı (her şey CC BY-SA 4.0).
- **Yeni açık `[DECIDE]`:** TTS seçimi, Kol 1'de konuşmacı çeşitliliği, akustik
  bozulma parametreleri (SNR / bant / RT60), tereddüt oranları, eşdeğerlik marjı,
  köprü seti boyutu.
- **Doğrulanacak, ezberden yazılmayacak:** Common Voice dağıtımı Ekim 2025'te
  Mozilla Data Collective'e taşındı; §3.3'ün ısınma malzemesi olarak dayandığı
  lisans yeniden kaynağından okunmalı. Klonlama elendiği için soru daraldı:
  yalnızca boru hattı ısınması için kullanılabilir mi.

**Sayaç:** Bugün `[DECIDE]` 26'dan 38'e çıktı — kapanandan çok açıldı ve net yön
ilk kez **açma** yönünde. Ders: bir tasarım kararı (D4) sadece iş eklemez,
**bilinmeyen** ekler — ve plan büyürken kod durursa bu görünmez, çünkü büyüyen
belge ilerleme gibi okunur.
