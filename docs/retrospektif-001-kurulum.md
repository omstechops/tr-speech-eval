# Kurulum Retrospektifi — 5-6 Eylül 2026

**Kapsam:** `evalstat` ve `tr-speech-eval` projelerinin ilk iki günü. Analiz
planı 001'in taslaktan §2'si kapanmış hâle gelmesine kadar. Vaka 10, 11 ve 12
8 Eylül'de eklendi; kayıt kapatılmadı çünkü üçü de yeni bilgi taşıyordu — biri
yeni bir hata sınıfı, biri var olan bir sınıfın örüntüye dönüştüğünü, biri de bir
denetimin kendi sorusunun dışını görmediğini. Vaka 13 ve 14, 9 Eylül'de, aynı
sebeple: biri Vaka 1'in sınıfına ikinci örneği verdi ve tek vakada görünmeyen bir
kaynak örüntüsünü görünür kıldı, öteki en kalabalık sınıfın dördüncü örneği oldu
ve o sınıfın sınırını genişletti. Vaka 15 aynı sınıfın beşinci örneği ve onu
gözlem olmaktan çıkarıp çalışma kuralına dönüştürüyor (§3.5).

**Neden tutuluyor:** Bu belge bir ilerleme raporu değil. Bir ölçüm çalışması
kurulurken yapılan hataların ve onları yakalayan mekanizmaların kaydı. Çalışmanın
konusu zaten "AI çıktısı ne zaman güvenilir" olduğu için, kurulum sürecinin
kendisi ilk veri kümesi sayılır.

---

## 1. Ana bulgu

On yedi vaka kaydedildi. Kronolojik olarak bakıldığında rastgele görünüyorlar.
**Yakalayan mekanizmaya göre gruplandığında sınıflar çıkıyor** — ve her sınıf
yalnızca kendi mekanizmasıyla yakalanabiliyor.

| Mekanizma | Yakaladığı sınıf | Vaka |
|---|---|---|
| Çapraz kontrol (AI → AI) | İç tutarsızlık, matematiksel ilişki hatası | 1, 4, **13** |
| İnsan düzeltmesi | Niyet okuma hatası, odak kayması | 2 |
| **Uygulamaya geçmek** | **Uygulanamaz veya eksik tasarım varsayımı** | **6, 8, 11, 14, 15, 17** |
| Dış otoriteye sormak | Paylaşılan eskimiş bilgi | 5, 9, 11 |
| Hiçbiri (geç yakalandı) | Her iki tarafın ortak kör noktası | 3, 7 |
| **Sınıf dışı** | **Doğru kararın maliyeti** | **10** |
| **Başka soruyla yapılan tarama** | **Önceki denetimin sorusuna girmeyen hata** | **12, 16** |

Dört şey değişti.

**Birincisi: "uygulamaya geçmek" artık beş vakalı, en kalabalık sınıf ve sınırı
iki kez genişledi.** 6, 8, 11, 14 ve 15 aynı yapıya sahip: bir varsayım tasarım
turlarında yanlışlanamadı, uygulama yoluna girilince yanlışlandı. Beş örnek, tek
tek anlatılacak vaka olmaktan çıkıp **yöntem hâline geliyor**: bir varsayımı
sınamanın en ucuz yolu onu tartışmak değil, onu uygulanabilir en küçük adıma
dönüştürmek.
Vaka 11 ayrıca iki mekanizmaya birden ait — kaynağa bakmak *ve* uygulamaya
geçmek — çünkü sorulacak soruyu uygulama üretti, cevabı kaynak verdi.

Vaka 14 sınıfın sınırını taşıyor: orada yanlışlanan şey bir tasarım varsayımı
değil, **doğrulama katmanının kendisiydi.** Yazılmış, gözden geçirilmiş ve
kullanıcıya gösterilmiş bir test, kendi deposundaki bir sabitle çelişiyordu ve
çelişki ancak test koşulunca göründü. Yani "uygulamaya geçmek" yalnızca tasarımın
sınavı değil; test yazmak da bir tasarım eylemi ve aynı körlüğü miras alıyor.
Koşulmamış test, okunmuş bir varsayımdan daha güvenilir değil.

Vaka 15 aynı sınırı bir adım daha taşıyor ve **Vaka 14'ün alt türü** olarak
duruyor. Vaka 14'te çelişki test ile kod arasındaydı; Vaka 15'te kod tarafı yok,
**iki test birbiriyle çelişiyor.** Yanlışlanan şey ne tasarım ne de tasarımı
sınayacak araç: şartnamenin kendi iç tutarlılığı. Alt tür şöyle yazılabilir: *bir
şartname yeterince büyüdüğünde kendi içinde çelişebilir, ve bu çelişme yalnızca
yürütmeyle görünür.* Her testi tek tek okumak yetmiyor, çünkü her biri tek başına
doğru; yanlış olan yalnızca birleşimleri ve birleşimlerini hiçbir dosya yazmıyor.

Vaka 17 aynı alt türü bir ölçek küçültüyor ve sınırın nerede **olmadığını**
gösteriyor: çelişki iki test arasında bile değil, **tek bir docstring'in
içinde.** İki cümle ayrı ayrı doğru, arka arkaya yazıldıklarında yanlış bir
önerme kuruyor. Yani "birleşim" için iki dosya, hatta iki testten fazlası
gerekmiyor — bitişik iki cümle yetiyor.

**İkincisi: Vaka 10 önceki dokuzun hiçbirine benzemiyor.** Onların hepsi
"yanlıştı, düzeltildi" idi: yanlış test önerisi, kaçırılan körleme, eskimiş model
kimliği, okunmamış lisans. Vaka 10'da **yanlış bir şey yok.** Kendi kaydını
kullanma kararı hâlâ lisans açısından en iyi karar. Terk edilme sebebi hatalı
olması değil, **pahalı** olması — ve maliyeti karar verilirken görünmüyordu. Bu
yüzden ayrı satırda: "doğru ama pahalı" bir kararın terk edilmesi, bir hatanın
düzeltilmesiyle aynı şey değil ve aynı mekanizmayla yakalanmıyor.

**Üçüncüsü: Vaka 12 ve 16 hatayla değil, onu arayan mekanizmayla ilgili.**
Önceki on bir vakada yakalayan mekanizma hatayı arıyordu. Vaka 12'de hatayı bulan
tarama başka bir şey arıyordu; hatanın durduğu alan bir önceki taramada okunmuş ve
"temiz" raporlanmıştı. Rapor yanlış değildi — sorulan soruya göre temizdi. Ayrı
satırda olmasının sebebi bu: bir alanı bir sebeple denetlemek, onu başka bir
sebeple denetlemiş saymıyor.

Vaka 16 aynı satırın ikinci örneği ve sınıfı denetimden **işleme** genişletiyor.
Vaka 12'de bir *alan* iki farklı sebeple ayrı ayrı denetlenmemişti; Vaka 16'da bir
*işlem* iki hedef için ayrı ayrı doğrulanmamıştı. İkisinde de yakalayan şey,
başka bir soruyu sormak için çalıştırılan bir komut oldu. İki örnekle satır artık
tek vakalık bir merak değil: **kapsamı birden çok olan hiçbir şey — ne bir
denetim, ne bir işlem — tek bir başarılı çıktıyla kapanmıyor.**

**Dördüncüsü: Vaka 13, Vaka 1 ile aynı sınıfın ikinci örneği ve sınıf artık bir
kaynağa bağlı.** İkisinde de sohbet asistanı bir **yön veya dejenere durum**
iddiasını sezgiden kurdu ve iddia yanlış çıktı: Wilcoxon'ın üç seviyeli veride
işaret testine indiğini görmemek, ve dar aralığın gücü hangi yöne çektiğini ters
kurmak. İkisi de aynı mekanizmayla, çapraz kontrolle yakalandı. Belgenin başka
yerinde örüntü eşiği üç vaka; burada iki vaka var, ama sınıf da dar — tek kaynak,
tek iddia tipi. Bu yüzden "örüntü" değil **kaynağa özgü kural** olarak
kaydediliyor (§3.8).

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
**Vakanın kendi kaydı da aynı hataya düştü.** Bu vaka ilk yazıldığında, olayı
anlatmak için, geçmişten çıkarılan e-posta adresi metnin içine birebir konuldu.
On üç commit'ten silinen dizgi, yayınlanacak bir belgeye düz metin olarak geri
girdi. Yakalayan şey sahibinin push öncesi istediği kontrollerden biri oldu —
çalışma ağacında kişisel tanımlayıcı arayan tarama. Commit henüz push
edilmemişti; metin düzeltildi. Kural "geçmişi temizle" diye kurulduğu için
tarama geçmişe bakıyordu ve **"yeni yazılanı da kontrol et" adımı kendiliğinden
gelmedi.** Bir denetim, kendi ürettiği metni kapsamadığı sürece eksik.
**Sonuç:** Aynı ailenin iki üyesi bu bölünme sırasında zaten düzeltilmişti:
`requires-python = ">=3.10"` hiçbir testin çalıştırmadığı bir tabanı ilan
ediyordu, `license = { text = "MIT" }` ise var olmayan bir LICENSE dosyasına
dayanıyordu. Üçü de aynı biçimde: **metadata bir şey beyan ediyor ve onu
doğrulayan hiçbir şey yok.** Vaka 9'un kuralı buraya uzanıyor: dışarıdan
doğrulanabilir her alan, yayımdan önce kendi kaynağından okunur — ve bir sebeple
tarandığı için öteki sebeple de tarandı sayılmaz.

### Vaka 13 — Kapsama açığının güce etkisi ters kuruldu
**Kim yaptı:** Sohbet asistanı; sahibi zinciri devraldı ve `power_analysis()`
görev tanımına yazdı.
İddia şuydu: `paired_bootstrap`'ın aralıkları k=40'ta nominal %95 yerine ~%93
kapsadığı için, nominal orana dayanan bir güç hesabı "aynı oranda **iyimser**"
olur. Yön ters. Kapsaması düşük aralık **dar**dır; dar aralık sıfırı daha sık
dışlar; prosedür hem H₀ hem H₁ altında nominalden **daha sık** reddeder. Yani ham
reddetme oranı bakımından nominal hesap iyimser değil, karamsardır. İyimserlik
başka yerde ve gerçekten var: prosedürün α=0.05'te çalıştığı iddiasında. Gerçek
hatayı %5'te tutmak aralığı genişletmeyi gerektirir, bu da aynı n'de gücü düşürür
ve MDE'yi büyütür.
**Kim yakaladı:** Claude Code, görevin ilk adımında, kod yazılmadan.
**Neden kendi kendine yakalanamazdı:** Vaka 1 ile aynı yapı. "Dar aralık = az
bilgi = az güç" zinciri sezgisel olarak akıcı ve her adımı ayrı ayrı doğru
sesleniyor; yanlış olan birleşim. İddiayı üreten sezgi, onu kontrol edecek sezgiyle
aynı sezgi.
**Sonuç:** Sıfır maliyet — yanlış yön uygulamaya geçmedi. Ama geçseydi ucuz
olmazdı: §9.1'in düzeltme seçenekleri bu yön üzerine kuruluydu ve MDE eğrisi
yanlış yöne düzeltilirdi. Doğru okuma §9.1'e yazıldı, kapsama-güç yönü orada
artık açıkça anlatılıyor.
**Sınıf notu:** Vaka 1 ile aynı sınıf, aynı kaynak, ikinci örnek. Kural §3.8'de.

### Vaka 14 — Test, kendi deposundaki sabitle çelişti ve bu ancak koşunca göründü
**Kim yaptı:** Claude Code, `power_analysis()` test süitini yazarken.
`paired_bootstrap` küme sayısı `MIN_CLUSTERS = 25`'in **altında** olduğunda
`FewClustersWarning` veriyor. Yeni süitteki üç test ise k=40 tasarımını
`pytest.warns(FewClustersWarning)` ile sarmıştı — R7 dahil, yani `paired_bootstrap`
ile tutarlılığı taşıyan test. 40 > 25 olduğu için o uyarı hiçbir zaman çıkmayacaktı;
üç test, gövde yazıldıktan sonra bile kalıcı olarak kırmızı kalırdı ve kırmızılığın
sebebi uygulama sanılırdı.
**Kim yakaladı:** Claude Code, süiti koşarken — yazarken değil, gözden geçirirken
değil, kullanıcıya diff olarak sunduktan sonra.
**Neden okumakla yakalanmadı:** Çelişki tek bir dosyada değildi. Test dosyasında
"k=40" yazıyor, `bootstrap.py`'de "25" yazıyor, ve ikisinin ilişkisi hiçbir yerde
yazmıyor — okuyucunun kafasında kuruluyor. Sarmalayıcı ayrıca **akla yatkındı**:
40 küme az sayılır, kapsama açığı tam da orada ölçülmüştü, dolayısıyla "burada bir
uyarı olmalı" sezgisi doğruya yakındı. Yanlış olan sezgi değil, sezginin kodda
karşılığı olduğu varsayımı.
**Sınıf:** Vaka 6, 8, 11 ile aynı — yalnızca yürütülünce görünen çelişki — ama
nesnesi farklı: yanlışlanan şey tasarım değil, tasarımı sınayacak olan araçtı.
**Maliyet:** Sıfıra yakın; aynı oturumda, gövde yazılmadan düzeltildi. Maliyeti
sıfırdan büyük yapan tek şey, düzeltmenin kullanıcıya gösterilen diff'ten sonra
gelmesi: gösterilen ile depoya giren aynı metin değil.
**Sonuç:** Üç sarmalayıcı kaldırıldı. Eşik ayrıca iki yönlü sınandı — k=10 uyarır,
`MIN_CLUSTERS` uyarmaz — çünkü tek yönlü eşik testi kaydığında sessiz kayar.

### Vaka 15 — İki test birbiriyle çelişti; çelişki kodda değil şartnamenin içindeydi
**Kim yaptı:** Claude Code, `power_analysis()` test süitini yazarken — gövdeden
önce, Vaka 14'ün düzeltmesiyle aynı oturumda. Aynı dosyada iki test, birbirinden
habersiz, uyarı eşiği hakkında uyuşmaz iki şey istedi:

- `test_the_threshold_itself_does_not_warn` eşiği `MIN_CLUSTERS`'a çiviliyor —
  "MIN_CLUSTERS is the first count that is **not** warned about", yani k=25
  uyarmaz ve 25'in altı uyarır.
- R10'un tekdüzelik testi k=20 ile güç hesaplatıyor. 20 < 25 olduğu için uyarı
  çıkıyor, `pyproject`'te `filterwarnings = ["error"]` var, ve uyarı hakkında
  hiçbir iddiası olmayan bir test uyarı yüzünden düşüyor.

k=10 uyarsın, k=20 uyarmasın, k=25 uyarmasın diyen bir eşik yok. İki test tek tek
makul; birlikte tutarsızlar.

**Kim yakaladı:** Claude Code, gövdeyi yazıp süiti koşarken. Süit yazıldı, gözden
geçirildi, kullanıcıya sunuldu ve **bir kez Vaka 14 için düzeltildi** — çelişki
üç okumanın da içinden geçti.

**Sınıf:** Vaka 6, 8, 11, 14 ile aynı, ama Vaka 14'ün **alt türü.** Vaka 14'te
çelişki test ile kod arasındaydı: test dosyasında "k=40", `bootstrap.py`'de "25",
ve ikisinin ilişkisi hiçbir yerde yazılı değil. Burada kod tarafı hiç yok. İki
testin ortak sonucu — "hangi k değerleri uyarır" — tek bir yerde yazılsaydı
çelişki görünürdü, ama o cümle hiçbir dosyada durmuyor; yalnızca iki testin
birleşiminden çıkıyor.

**Neden okumakla yakalanmadı:** İki test dosyada yüzlerce satır arayla duruyor ve
hiçbiri ötekine atıf yapmıyor. Her ikisi de kendi başına doğru; yanlış olan
birleşim. Vaka 14'ün dersi ("koşulmamış test, sınanmamış varsayımdır") burada bir
katman yukarı çıkıyor: koşulmamış bir **süit**, tek tek doğru testlerden kurulu
olsa bile sınanmamış bir bütündür.

**Maliyet:** Sıfıra yakın. Gövde yazıldı, süit koşuldu, tek kırmızı buydu ve
sebebi tek satırda ayrıştı. Uygulamayı yazan taraf çelişkiyi kendiliğinden
çözmedi, kullanıcıya iki seçenekle getirdi — şartnameyi sessizce değiştirmek,
düzeltilen şeyin ne olduğunu kaydın dışında bırakırdı.

**Sonuç:** Uyarı yalnızca o üretimde `warnings.catch_warnings()` ile bastırıldı,
k=20 korundu. Az kümeyle çalışmak gerçek bir senaryo ve fonksiyonun orada da
doğru davranması gerekiyor; k'yi eşiğin üstüne çekmek süiti susturur ama test
kapsamını daraltırdı. `MIN_CLUSTERS` oynatılmadı — o `bootstrap.py`'ın ölçülmüş
sabiti ve test rahatlığı için değişmez. Bastırmanın **neden** orada olduğu testin
docstring'ine yazıldı; yazılmasaydı altı ay sonra sarmalayıcının kendisi bir soru
olurdu.

### Vaka 16 — İki depoya push edildiği varsayıldı, yalnızca biri doğrulandı
**Kim yaptı:** Claude Code ve sahibi birlikte, 8 Eylül bölünmesinde. Tek depo üçe
ayrıldı, ikisine remote eklendi ve ikisine push edildi. `evalstat`'ın push'u
başarılı döndü. `tr-speech-eval` tarafında **uzak depo hiç var olmadı** — remote
URL'si `git remote add` ile yerel yapılandırmaya yazıldı, ama GitHub tarafında o
adres hiçbir zaman çözülmedi. `git remote -v` doğru URL'yi gösterdiği için
yapılandırma bakıldığında sağlam görünüyor; `remote -v` yalnızca yazılmış olanı
okuyor, karşılığının var olduğunu sınamıyor.

**Asıl hata varsayımın kendisi değil, kanıtın devredilmesi.** İki hedefli bir
işlem yapıldı, bir hedefin başarılı çıktısı görüldü, ve o çıktı **ikisinin de**
gittiğinin kanıtı sayıldı. Ortada yanlış bir gözlem yok — `evalstat` gerçekten
push edildi. Yanlış olan, tek gözlemin kapsamının iki katına çıkarılması.

**Kim yakaladı:** Sahibi, push öncesi "kaç commit bekliyor" diye sorunca. Cevap
için `git fetch` atıldı ve fetch `Repository not found` döndü. Yani hatayı bulan
komut hatayı aramıyordu; commit sayısı sayıyordu.

**Sınıf:** Vaka 12'nin akrabası — başka bir soruyla yapılan tarama. Orada bir alan
iki farklı sebeple denetlenmemişti, burada bir işlem iki hedef için ayrı ayrı
doğrulanmamıştı.

**Neden aradaki sürede yakalanmadı:** Hiçbir şey kırmızıya dönmedi. Yerel depo
tamamen sağlıklı: `git status` temiz, `git log` 22 commit gösteriyor, `git commit`
çalışıyor, `git remote -v` beklenen adresi yazıyor. Uzak tarafın yokluğu ancak
uzak tarafa gerçekten dokunan bir komutla — `fetch`, `ls-remote`, `push` — ortaya
çıkıyor, ve bölünmeden sonra o komutlardan hiçbiri bu depoda çalıştırılmadı.
Ayrıca `origin/main` diye bir ref hiç oluşmadığı için `log origin/main..HEAD`
"0 commit" değil **hata** veriyor; bu ayrımın kendisi de fark edilmeyi bekliyordu,
çünkü "0 commit bekliyor" ile "kıyaslanacak taraf yok" aynı ekranda benzer duruyor.

**İkincil zarar: yanlış olgu belleğe yazıldı.** Arada geçen sürede kalıcı nota
"depolar public oldu" diye bir cümle girdi. O cümle hiçbir kaynaktan okunmamıştı;
push'un başarılı olduğu varsayımından türetilmişti. Yani doğrulanmamış bir varsayım
yalnızca kaydedilmedi, **olgu diye kaydedildi** ve sonraki oturumlara olgu olarak
taşındı. Bu, belgenin başka yerinde zaten yazılı olan kuralın ihlali: bir artefakta
veya dışarıya verilen bir beyana girecek olgu, kaynağından okunur.

**Maliyet:** Şimdilik düşük — hiçbir iş kaybolmadı, 22 commit yerelde duruyor ve
push edilebilir durumda. Maliyeti sıfırdan büyük yapan iki şey var: bölünmeden
bu yana yapılan bütün çalışma tek kopya hâlinde tek diskte durdu, ve bellekteki
yanlış olgu düzeltilene kadar sonraki her oturumun başlangıç bilgisi yanlıştı.

**Sonuç:** `evalstat`'ın `ls-remote`'u kontrol grubu olarak koşuldu ve gerçek hash
döndürdü, yani sorun kimlik doğrulama veya ağ değil, adresin kendisi. Uzak deponun
durumu sahibine soruldu; `remote set-url` sahibinin cevabı gelmeden yapılmadı,
çünkü doğru adresi tahmin etmek bu vakanın kendisini tekrarlamak olurdu.

Sahibinin cevabı teşhisi doğruladı: **depo GitHub'da hiç yoktu ve aynı adla yeni
oluşturuldu.** Yerel remote URL'si baştan beri doğruydu, `set-url` hiç gerekmedi —
eksik olan yapılandırma değil, yapılandırmanın işaret ettiği şeydi. Aynı komut
şimdi farklı bir sonuç veriyor ve fark tam da §3.7'nin üçüncü maddesinin konusu:

| | Depo yokken | Depo boş oluşturulduktan sonra |
|---|---|---|
| `ls-remote origin` | exit 128, `Repository not found` | exit 0, çıktı boş |
| `fetch origin` | exit 128 | exit 0 |
| `remote -v` | aynı satır | aynı satır |

`remote -v` iki durumda da değişmedi, çünkü yerel yapılandırmayı okuyor; değişen
uzak tarafın kendisiydi. `log origin/main..HEAD` hâlâ hata veriyor, ama artık
başka bir sebeple — depo var, içi boş, `origin/main` diye bir ref henüz yok. "Yok"
ile "boş"un aynı ekranda benzer görünmesi bu vakada iki kez işe karıştı.

Uzak taraf sıfır ref taşıdığı için bölünmeden bu yana biriken **22 commit'in
tamamı** push bekliyor. Kural §3.7'ye eklendi.

### Vaka 17 — Tek docstring'in içinde iki doğru cümle, yanlış bir önerme
**Kim yaptı:** Claude Code, `power_analysis()` test süitini yazarken (Vaka 14 ve
15 ile aynı dosya). R7'nin docstring'i şunu diyordu:

> *"the 0.03 tolerance below is a tolerance on Monte Carlo noise, not a threshold
> that decides anything. Both seeds are fixed, so a failure is reproducible and
> is never bad luck."*

İki yarısı da doğru. Tolerans gerçekten bir karar eşiği değil, gürültü payı. Ve
tohumlar gerçekten sabit, dolayısıyla hata gerçekten yeniden üretilebilir.
Birleşimleri ise yanlış: **sabit tohum gürültüyü kaldırmıyor, donduruyor.**
Yeniden üretilebilir bir hata pekâlâ şanssızlık olabilir — hep aynı şanssızlık
olur, o kadar. Cümle "reproducible" ile "not noise"u eşitliyor; ikisi eşit değil.

**Kim yakaladı:** Simülasyon yolu yazılıp süit koşulunca. R7 tam sınırda düştü:
ampirik 0.77, sapma `0.030000000000000027`. Docstring'in iddiasına göre bunun
tek sebebi uygulamanın yanlış olması olabilirdi.

**Yakalayan şey testi koşmak değil, iddiayı ölçmek oldu.** Önce yanlılık
sınandı: `n_sim=20000` ile çözülen MDE, 5000 denemelik bağımsız kontrolde 0.7994
verdi — kestirici yansız, kod doğru. Sonra yayılım ölçüldü: `n_sim=600`'de,
testin sabitlediği ayarda, 14 tohum üzerinden ampirik SD 0.0133 ve aralık
0.760–0.805. Tolerans birleşik gürültünün ~1.3 katıymış ve 14 tohumun 2'si
düşüyormuş. Sabitlenen tohum yanlış tarafa düşmüş.

**Sınıf:** Vaka 15'in alt türü, bir ölçek küçüğü. Vaka 15'te çelişki iki test
arasındaydı ve "birleşimi hiçbir dosya yazmıyor" demek anlamlıydı. Burada
birleşim tek bir docstring'in iki bitişik cümlesi. Tek tek okumak yine yetmiyor,
ama bu kez "tek tek okumak" bir paragrafı okumak demek.

**Neden okumakla yakalanmadı:** Cümle akıcı ve kendinden emin. "Sabit tohum →
tekrarlanabilir → şans değil" zinciri sezgisel olarak doğru duruyor ve ilk iki
halkası gerçekten doğru. Yanlış olan üçüncü halka, ve o halka yazılmamış;
okuyucunun kafasında kuruluyor. Vaka 15'te de böyleydi, Vaka 14'te de.

**Maliyet:** Sıfıra yakın, ama sıfır değil. Cümleye inanılsaydı doğru bir
uygulama yanlış sanılır, hata kodda aranır ve kestirici "düzeltilmeye"
çalışılırdı. Ölçüm iki deney ve birkaç dakika sürdü; onu yapmama kararı da
alınabilirdi.

**Bu vakayı testi koşmak yakalayamazdı, ve sebebi kaydedilmeye değer.** Vaka 14
ve 15'te yakalayan mekanizma yürütmenin kendisiydi: süit koşuldu, kırmızılık
çıktı, kırmızılığın sebebi tek bir okumayla ayrıştı. Burada süit yine koşuldu ve
yine kırmızı verdi — ama kırmızılık **iki hipotezi ayırt etmiyordu.** "Uygulama
yanlış" ve "gürültü sınırda" aynı ekranı üretiyor; ikisinin de gözlemi tek bir
başarısız `assert`. Testi tekrar koşmak aynı ekranı tekrar üretirdi, çünkü
tohumlar sabit. Ayıran şey **testin dışında koşulan bir deney** oldu:
`n_sim=20000` ile çözüp bağımsız kontrol etmek, yani testin sabitlediği ayarı
kasten terk etmek. Süit bu deneyi barındıramaz — 20 saniyelik bir süitin içinde
duramayacak kadar pahalı, ve zaten testin değil testin *toleransının* sınanması.

Bu, §3.5'in beşinci kuralının kendi örneği: bir testin kırmızılığı, testin kendi
açıklamasına göre yorumlanmıyor. Kural §3.7'nin `remote -v` örneğini taşıması
gibi kendi örneğini taşıyor — ve iki örnek aynı şeyi söylüyor: bir gözlemin ne
anlama geldiği, o gözlemi üreten aracın ne ölçtüğüne bağlı. `remote -v` yerel
yapılandırmayı okuyor, uzak tarafı değil; kırmızı bir `assert` toleransın
aşıldığını söylüyor, sebebini değil.

**Sonuç:** Tolerans `0.05`'e çıkarıldı, ama asıl düzeltme sayı değil, sayının
**neye bağlandığı**. Docstring artık ölçülen SD'yi (0.0133, 14 tohum), aralığı
ve yansızlık kontrolünü (`n_sim=20000` → 0.7994) taşıyor, ve `n_sim` ya da
deneme sayısı değişirse toleransın yeniden ölçülmesi gerektiğini açıkça
söylüyor. Yanlış cümle şununla değişti: *tohumlar sabit olduğu için hata yeniden
üretilebilir, ama gürültü kaldırılmış değil; tolerans ölçülen Monte Carlo
yayılımını kapsayacak şekilde seçildi.* `n_sim`'i büyütmek de düşünüldü ve
reddedildi — süit 20 saniyeden ~5 dakikaya çıkardı, ve atlanacak kadar yavaş bir
test koşulmayan bir testtir (§3.5.2).

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

**5. Bir varsayımı sınamanın en ucuz yolu, onu tartışmak değil. Artık gözlem
değil, çalışma kuralı.**
Vaka 6, 8, 11, 14 ve 15 aynı yapıda ve beşi birlikte belgenin en kalabalık
sınıfı: tasarım turlarında kapanmayan şey, uygulamanın en küçük adımı yazılırken
kapandı. Vaka 11'de mekanizma daha da özel — yanlışlayan şey kodun kendisi değil,
**kod yazmaya çalışmanın ürettiği soru** oldu ("girdi zaten neye benziyor?").
Beş örnek eşiği geçtiği için madde artık bir gözlemin anlatımı değil, uyulacak
bir kural:

1. **Bir tasarım turu, uygulanabilir bir adım üretmeden kapatılmaz.** Kapandı
   sayılan tur, en küçük yürütülebilir adımı yazılana kadar açık sayılır.
2. **Bir şartname, koşulmadan gözden geçirilmiş sayılmaz.** Test yazmak bir
   tasarım eylemidir ve tasarımın körlüğünü miras alır; koşulmamış bir test,
   gerekçesi ne kadar iyi yazılmış olursa olsun sınanmamış bir varsayımdır.
   Kırmızı kalması beklenen bir süit bile, kırmızılığının **beklenen sebeple**
   olduğunu görmek için koşulur. Vaka 14'te süit baştan sona kırmızıydı; hatayı
   gösteren şey kırmızılık değil, üç testin yanlış istisna tipiyle kırmızı
   olmasıydı.
3. **Süit bir bütün olarak da sınanır, tek tek testler olarak da.** Vaka 15'in
   alt türü budur: bir şartname yeterince büyüdüğünde kendi içinde çelişebilir,
   ve bu çelişme yalnızca yürütmeyle görünür. Testleri tek tek okumak yetmez,
   çünkü her biri tek başına doğru olabilir ve yanlış olan yalnızca birleşimleri
   olabilir — birleşimi ise hiçbir dosya yazmaz. Vaka 17 bunun alt sınırını
   veriyor: birleşim iki dosya değil, **bitişik iki cümle** olabilir. Doğru
   cümlelerin ardarda dizilmesi yanlış bir önerme üretebilir, ve bu, cümleleri
   tek tek okuyarak bulunamaz.
4. **Şartname ile kod çeliştiğinde, çelişki uygulamayı yazan tarafça sessizce
   çözülmez.** Hangi tarafın yanlış olduğu bir karardır; kaydı tutulur ve sahibi
   verir. Vaka 15'te iki seçenek getirildi, seçim yapıldı ve seçimin gerekçesi
   koda girdi.
5. **Bir testin kırmızılığı, testin kendi açıklamasına göre yorumlanmaz.**
   R7'nin docstring'i düşmenin tek sebebinin uygulama hatası olabileceğini
   söylüyordu; ölçüm bunun yanlış olduğunu gösterdi. Bir tolerans savunulacaksa
   ölçülür, ve bu sırayla: önce kestirici yanlı mı (yüksek hassasiyetle çöz,
   bağımsız kontrol et), sonra testin sabitlediği ayarda yayılım ne (çok
   tohumla). İkinci ölçüm ancak birincisi temizse anlamlıdır, çünkü yanlı bir
   kestiricinin yayılımı toleransı değil kodu ilgilendirir.

**6. Hız devredilebilir işte, yavaşlık devredilemez işte.**
İki günde ortam, iki paket, 17 test, körleme modülü ve bir plan revizyonu
tamamlandı. Aynı iki günde tek bir devredilemez karar (korpus) ilerlemedi.
Oran bozuk ve bozukluğun yönü sistematik.

**7. Bir denetim yalnızca sorduğu soruyu yanıtlar; bir işlem yalnızca
doğrulanan hedefinde gerçekleşmiş sayılır.**
Kişisel bilgi taraması işlevsel hatayı, geçmiş taraması yeni yazılan metni
bulmuyor — Vaka 12 ikisini de gösteriyor. Aynı alan farklı sebeplerle ayrı ayrı
denetlenmeli, ve denetim kendi çıktısını da kapsamalı.

Vaka 16 aynı kuralı işlemlere taşıyor: **çoklu hedefli bir işlemin başarısı hedef
başına doğrulanır; birinin çıktısı diğerinin kanıtı değildir.** Pratik karşılığı
mekanik ve dar:

1. İki depoya push, iki dosyaya yazma, iki ortama dağıtım — kaç hedef varsa o
   kadar doğrulama. "Komut hata vermedi" hedef sayısından bağımsız tek bir
   gözlemdir.
2. Doğrulama, işlemin gerçekten dokunduğu tarafa dokunmalı. `git remote -v`
   yalnızca yerel yapılandırmayı okur ve uzak tarafın var olduğunu sınamaz;
   bunu `ls-remote`, `fetch` veya `push` yapar. Yapılandırmayı okumak,
   yapılandırmanın işe yaradığını göstermez.
3. Bir doğrulama başarısız olduğunda, "yok" ile "boş"u ayırt et. `origin/main`
   yoksa `log origin/main..HEAD` sıfır değil hata döndürür; ikisi ekranda
   benzer görünür ve anlamları zıttır.
4. Doğrulanmamış bir varsayım kalıcı nota olgu olarak yazılmaz. Vaka 16'da
   yazıldı ve sonraki oturumlara olgu olarak taşındı; §1'in kendi kuralı zaten
   bunu yasaklıyordu.

**8. Sohbet asistanının yön ve dejenere durum iddiaları doğrulanmadan
alınmıyor.**
Vaka 1 ve 13 aynı sınıf: bir istatistiksel ilişkinin **yönü** ("hangi hata hangi
tarafa çeker") veya bir testin **dejenere durumu** ("bu veride bu test neye
iner") sezgiden kuruldu ve ikisi de yanlış çıktı. İkisi de çapraz kontrolle
yakalandı, ikisinin de maliyeti sıfır kaldı — ama ikisi de yakalanmasaydı
tasarıma girecekti. Bu sınıf, o kaynağın en zayıf yeri olarak kaydediliyor:
akıcı, tek tek doğru duran adımlardan kurulu ve yanlış olan yalnızca birleşim.
**Kural:** o kaynaktan gelen bir yön iddiası ya küçük bir sayısal örnekle ya da
formülün kendisiyle doğrulanmadan plana, koda veya göreve girmez. Kaynağın
tamamını değil, bu iki iddia tipini hedefleyen bir kontrol; geri kalanı (kavram
açıklama, karşılaştırma, redaksiyon) bu kaydın konusu değil.

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
