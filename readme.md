# Tokenizer Benchmark

Bu çalışma, dil modellerinin performansını dilbilimsel temellere dayalı standartlar aracılığıyla artırmayı hedefleyen bir **tokenizer benchmark** yaklaşımı sunmaktadır. Türkçe gibi zengin morfolojik yapıya sahip dillerde tokenizasyon, yalnızca metnin belirli parçalara ayrılması değildir; aynı zamanda dilin anlamlı, tutarlı ve verimli şekilde modellenmesini sağlayacak temel bir adımdır.

---

## Tokenizer Benchmark Kriterleri ve Amaçları

Aşağıda belirtilen kriterler, dil modellerinde hem dilbilimsel doğruluğu hem de hesaplama verimliliğini artırmaya yönelik olarak belirlenmiştir. Bu kriterlerin detaylı olarak anlaşılması, tokenizer seçimi ve geliştirilmesinde yol gösterici olacaktır.

### Kriterler

1. **Token Sayısı**: Verilen bir metnin kaç parçaya (token) bölündüğünü ifade eder.  
2. **Hız**: Tokenleştirme işleminin ne kadar sürede tamamlandığı.  
3. **Anlamlı Token Oranı**: Tokenlerin kaçının dil açısından anlamlı olduğu, yani kendi başına bir anlam veya işlev taşıyan birimlere denk geldiği.  
4. **Token Saflığı (Purity)**: Tokenlerin kaçının anlam kaybı olmadan, yapay alt parçalara ayrılmadan kullanılabildiği. Bu, özellikle Türkçe gibi eklemeli (aglütinatif) dillerde önemlidir.  
5. **Sözlük Boyutu**: Tokenizer'ın sözlük boyutunun büyüklüğü, kullanılan token sayısını ifade eder.

---

### Kriterlerin Amaçları (Detaylandırılmış Açıklamalar ve Örnekler)

Aşağıdaki bölümlerde her bir kriterin model eğitimi, çıkarım (inference) süreci ve dilbilimsel bütünlük açısından neden önemli olduğu ayrıntılı örneklerle açıklanmaktadır.

#### 1. Token Sayısı

**Amaç**: Modelin eğitimi sırasında veri işleme hızını ve bellek kullanımını optimize etmektir. Fewer, but more semantically rich tokens may help models learn patterns more effectively.

**Detay**:  
Çok fazla sayıda tokena bölünmüş bir metin, modelin daha büyük embedding matrisleri oluşturmasına, daha yavaş eğitilmesine ve daha çok bellek tüketmesine neden olur. Öte yandan, metni çok az sayıda ancak anlamlı tokenlere bölmek, modelin her tokeni daha anlaşılır bir bilgi birimi olarak işlemesine yardımcı olabilir.

**Örnek**:  
- Cümle: "Akademisyenlerle aileleri aktif çalışıyor."  
  - **Daha az ve anlamlı token örneği**: ["akademisyen", "ler", "le", "aile", "leri", "aktif", "çalış", "ıyor"]  
    Bu ayrım, kelimelerin kök ve ek yapısını korur ve kelime anlamlarını net ortaya koyar. Böylece model, "akademisyen" kavramını, çoğul ekini ("ler"), bağlacı ("le"), "aile" kavramını, çoğul ekini ("leri"), sıfat ("aktif") ve fiilin çekimli formunu ("çalışıyor") ayrı ayrı öğrenir. Sonuçta, toplam token sayısı makul bir seviyede tutulmuş, ama anlam bütünlüğü korunmuştur.

#### 2. Hız

**Amaç**: Eğitim ve çıkarım aşamasında tokenleştirme süresini kısaltarak gerçek zamanlı uygulamalara uygun bir iş akışı sağlamak.

**Detay**:  
Özellikle büyük veri setleri üzerinde çalışan modellerde, tokenizasyon süresinin uzun olması eğitim süresini uzatır. Gerçek zamanlı metin işleme, sohbet robotları veya anlık geri bildirim gereken uygulamalarda tokenizasyon hızı kritik hale gelir. Daha hızlı tokenizasyon, daha düşük gecikme (latency) ve daha yüksek işlem hacmi (throughput) anlamına gelir.

**Örnek**:  
- Aynı uzunluktaki iki metinden biri 2 saniyede, diğeri 10 saniyede tokenleşiyorsa, büyük hacimli metinleri işlemek isteyen bir uygulamada 10 saniyelik gecikme kabul edilemez hale gelebilir. Özellikle binlerce metni ardışık olarak işlemek gerektiğinde hız farkı büyük bir etki yaratır.

#### 3. Anlamlı Token Oranı

**Amaç**: Tokenlerin dilin anlamsal yapısını yansıtacak şekilde oluşturulmasını sağlamak. Anlamlı tokenlerin yüksek olması, modelin embedding uzayında daha tutarlı ve doğru temsil oluşturmasını kolaylaştırır.

**Detay**:  
Anlamsız veya gereksiz yere bölünmüş tokenler, modelin bu parçaları bir bütün halinde anlamlandırmasını zorlaştırır. Anlamlı tokenler, dilin temel yapı taşlarını (kökler, ekler, sıfatlar, fiil çekimleri) modelin doğrudan tanımasını sağlar. Bu sayede model, "aile" ve "leri" ekini ayrı ayrı öğrenerek "aileleri" kavramını kolayca inşa edebilir.

**Örnek**:  
- "aileleri" kelimesi:  
  - **Doğru Tokenizasyon**: ["aile", "leri"]  
    Burada "aile" kök kelimeyi, "leri" ek de çoğulluğu temsil eder. Model bu iki anlamlı parçayı birleştirerek “aileleri” kavramını kavrayabilir.  
  - **Yanlış Tokenizasyon**: ["a", "i", "le", "leri"]  
    Bu şekilde bölündüğünde "a" ve "i" anlamsız hale gelir, model bu parçaları birleştirerek özgün anlamı kavramakta zorlanır.

#### 4. Token Saflığı (Purity)

**Amaç**: Kelimelerin morfolojik yapısını bozmadan anlam bütünlüğünü koruyacak şekilde tokenlere ayrılması. Bu sayede model, dilin doğal yapısını daha iyi öğrenerek daha yüksek performans gösterebilir.

**Detay**:  
Türkçe gibi eklemeli dillerde, kelime kökü ve ekler arasındaki ilişki kritiktir. Saf tokenler, anlamlı alt birimlere dayanır; gereksiz ve anlamsız bölünmeler, modelin dilbilgisel yapıları kavramasını zorlaştırır. Token saflığı, hem eğitim süresinde hem de sonrasında modelin cevap kalitesinde belirleyici olur.

**Örnek**:  
- "çalışıyorlar" kelimesi:  
  - **Anlamlı Ayrıştırma**: ["çalış", "ıyor", "lar"]  
    "çalış" fiil kökü, "ıyor" geniş zaman çekimi, "lar" çoğul ekidir. Model bu yapıyı öğrendiğinde benzer kalıplara rahatça genelleme yapabilir.  
  - **Anlamsız Ayrıştırma**: ["ça", "lı", "şı", "yor", "lar"]  
    Bu durumda "ça", "lı", "şı" gibi parçalar anlam taşımadığı için model dilin yapısal mantığını çözmede zorlanır.

#### 5. Sözlük Boyutu

**Amaç**: Optimum bir sözlük boyutu belirleyerek modeli gereksiz yere büyütmemek ve performansı artırmak. Sözlük boyutu, hem bellek kullanımını hem de tahmin süresini etkiler.

**Detay**:  
Aşırı büyük bir sözlük, modelin hesaplama yükünü artırır. Tokenizer, çok sayıda nadir veya anlamsız token içeriyorsa, model bu tokenlerin temsilini anlamlı hale getirmekte zorlanır. Orta boyutta, sık kullanılan kelime kökleri ve ekleri içeren bir sözlük, hem eğitimde hem de çıkarımda daha etkilidir.

**Örnek**:  
- İki farklı sözlük boyutu:  
  - 256 bin token içeren bir sözlük, nadir kelimeleri ve gereksiz parçaları içeriyor olabilir. Bu durum, embedding matrisini büyütür ve eğitimi zorlaştırır.  
  - 30 bin civarında sık kullanılan, anlamlı kök ve eklerden oluşan bir sözlük, dilin önemli kısımlarını kapsar. Model bu sayede bellek kullanımını optimize eder ve anlamlı genellemeler yapar.

---

## Maddelerin Uygulanması

Bu kriterlerin hayata geçirilmesinde çeşitli fonksiyonlar ve metodolojiler kullanılabilir:

- `isTurkish()` fonksiyonu: Her tokenin gerçekten Türkçe bir kök ya da geçerli bir ek içerip içermediğini kontrol edebilir.  
- `predefined_word` listeleri: Önceden belirlenen sözcük veya kelime köklerini doğrulanmış anlamlı birim kabul ederek ek kontrolleri atlayabilir, bu da hız ve verimlilik kazandırır.

Bu tür metodolojiler, dilbilimsel farkındalığı artırarak tokenizasyon sürecini geliştirmeyi amaçlar.

---

# Tokenizer Benchmark ve MMLU Benchmark Sonuçlarının İlişkisi

Tokenizer benchmarkı, MMLU (Massive Multitask Language Understanding) benchmarkında kullanılan 6200 sorunun metinleştirilmiş verisi üzerinde uygulanmıştır. Böylece dil modelinin soruları anlama ve yanıt üretme başarısıyla, tokenizer kriterlerindeki başarının korelasyonu incelenebilir.

## İlk Sonuçlar

1605376 karakter ve 198193 boşlukla ayrılmış kelime içeren bir metin üzerinde 14 farklı tokenizer test edilmiştir. MMLU verisinin kullanılması, tokenizasyonun gerçek dünyadaki sınav soru tipleriyle ne kadar uyumlu olduğunu göstermeye yardımcı olur.

---

## Tokenizer Benchmark Sonuçlarının Değerlendirilmesi

Tokenizer benchmarkı, ölçülen kriterlerin her birinin model performansına farklı yönlerden etki ettiğini ortaya koymaktadır. Örneğin, yüksek anlamlı token oranına sahip bir tokenizer, MMLU performansını artırabilir. Benzer şekilde, saf tokenlerin yoğunluğu, modelin dilin yapısal ve semantik kurallarını daha iyi kavramasını sağlayarak doğruluğunu yükseltebilir.

Ayrıca, sözlük boyutunun optimizasyonu ve hızlı tokenleştirme, büyük modellerin gerçek zamanlı uygulamalarda daha verimli kullanılmasını mümkün kılar.

Aşağıdaki tablo, farklı tokenizerların performansını detaylı bir şekilde karşılaştırmaktadır. Bu tabloda her bir tokenizer için sözlük boyutu (Vocab Size), toplam token sayısı (Token Count), işleme süresi (Time), benzersiz token sayısı (Unique Token Count), anlamlı Türkçe tokenlerin sayısı (Turkish Token Count) ve oranı (Turkish Token %), ayrıca saf token sayısı (Pure Token Count) ve oranı (Pure Token %) gibi ölçütler verilmiştir. Bu sayede, hangi tokenizer’ın dilin yapısını daha iyi yansıttığı, hangi oranda anlamlı ve saf token ürettiği, ne kadar hızlı çalıştığı ve ne kadar geniş bir sözlüğe sahip olduğu daha net bir şekilde değerlendirilebilir.

| Tokenizer                                | Vocab Size | Token Count | Time    | Unique Token Count | Turkish Token Count | Turkish Token % | Pure Token Count | Pure Token % |
|------------------------------------------|------------|-------------|---------|---------------------|---------------------|-----------------|------------------|--------------|
| google/gemma-2-9b                        | 256,000    | 497,015     | 2.95    | 6,383               | 3,104               | 48.63           | 2,365            | 37.05        |
| alibayram/tr_tokenizer                   | 30,158     | 476,556     | 2.4231  | 11,531              | 11,342              | 98.36           | 11,055           | 95.87        |
| AhmetSemih/tr_tokenizer                  | 59,572     | 451,883     | 2.4849  | 13,370              | 13,253              | 99.12           | 13,357           | 99.90        |
| aliarda/turkish_tokenizer_256k           | 256,000    | 488,267     | 2.5124  | 13,631              | 13,351              | 97.95           | 12,981           | 95.23        |
| aliarda/turkish_tokenizer                | 58,526     | 451,936     | 2.3406  | 13,268              | 13,170              | 99.26           | 13,256           | 99.91        |
| meta-llama/Llama-3.2                     | 128,256    | 488,535     | 3.1249  | 6,823               | 3,125               | 45.8            | 2,109            | 30.91        |
| utter-project/EuroLLM                    | 128,000    | 497,173     | 3.2019  | 5,226               | 2,457               | 47.01           | 1,838            | 35.17        |
| Qwen/Qwen2.5                             | 151,665    | 561,866     | 3.315   | 5,752               | 2,320               | 40.33           | 1,734            | 30.15        |
| CohereForAI/aya-expanse                  | 255,029    | 434,526     | 2.7651  | 8,562               | 4,338               | 50.67           | 2,822            | 32.96        |
| openai-community/gpt2                    | 50,257     | 821,139     | 4.3765  | 3,454               | 1,582               | 45.8            | 1,119            | 32.4         |
| mistralai/Mistral-Nemo-Instruct-2407     | 131,072    | 534,930     | 3.1405  | 4,354               | 1,971               | 45.27           | 1,571            | 36.08        |
| microsoft/Phi-3.5-mini-instruct          | 32,011     | 803,971     | 4.5526  | 3,640               | 1,599               | 43.93           | 1,253            | 34.42        |
| Trendyol/Trendyol-LLM-8b-chat-v2.0       | 128,256    | 488,535     | 3.0438  | 6,823               | 3,125               | 45.8            | 2,109            | 30.91        |
| ytu-ce-cosmos/turkish-gpt2-large-750m-v0 | 50,258     | 339,852     | 2.4044  | 22,746              | 17,529              | 77.06           | 6,291            | 27.66        |

Bu tabloda farklı tokenizerların başarım ölçütlerini karşılaştırarak, hangi yaklaşımın Türkçe dilinin morfolojik yapısına daha uygun, hangi yaklaşımın daha hızlı, hangi yaklaşımın daha anlamlı token ürettiği gibi sorulara yanıt aramak mümkündür. Böylece hem dilbilimsel bütünlüğü koruyan, hem de pratik kullanımda avantaj sağlayan tokenizasyon stratejilerine ulaşmak hedeflenir.

---

## MMLU Benchmark Sonuçlarından Örnekler

Aşağıdaki tablo, [**`alibayram/yapay_zeka_turkce_mmlu_liderlik_tablosu`**](https://huggingface.co/datasets/alibayram/yapay_zeka_turkce_mmlu_liderlik_tablosu) üzerinden elde edilen bazı modellerin başarı ve süre değerlerini gösterir. Bu sayede, belirli tokenizasyon stratejilerinin model performansı üzerindeki etkisi daha somut hale gelir.

| Model Name                               | Parametre Sayısı | Başarı (%) | Toplam Süre (s) |
|------------------------------------------|------------------|------------|-----------------|
| google/gemma-2-9b                        | 9.2B             | 69.26      | 2,276.631       |
| utter-project/EuroLLM-9B-Instruct        | 9.2B             | 51.29      | 2,114.299       |
| meta-llama/Llama-3.2-3B                  | 3.2B             | 44.95      | 1,008.758       |
| Qwen/Qwen2.5-7B-Instruct                 | 7.6B             | 61.68      | 1,808.736       |
| CohereForAI/aya-expanse-8b               | 8.0B             | 62.06      | 1,725.916       |
| phi3.5                                   | 3.8B             | 29.37      | 3,244.336       |
| mistralai/Mistral-Nemo-Instruct-2407     | 12.2B            | 46.89      | 2,421.859       |

---

## Sonuç

Bu çalışma, dilbilimsel kriterler ve MMLU gibi kapsamlı testler üzerinden tokenizer performansını değerlendirerek, dil modellerinin eğitiminde daha anlamlı, saf, hızlı ve verimli bir yapı oluşturmayı amaçlar. Dilbilim temelli tokenizasyon standartları, büyük modellerin yalnızca veri hacmine bel bağlamadan, dilin içsel yapısal ve anlamsal özelliklerine dayalı bir şekilde öğrenme gerçekleştirmesini mümkün kılar. Bu yaklaşım, hem araştırmacıların hem de uygulayıcıların, büyük dil modellerini daha akılcı, hesaplı ve etkin bir biçimde geliştirmelerine yardımcı olacaktır.
