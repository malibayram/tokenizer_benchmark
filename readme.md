# Tokenizer Benchmark

### Tokenizer benchmarkı oluşturma ve bu yolla tokenizer standartları oluşturma amaçlı çalışmaları içerir.

---

## Benchmark Kriterleri 

1. **Token Sayısı**: Verilen bir metnin kaç tokene bölündüğü.
2. **Hız**: Tokenleştirme işleminin ne kadar sürede tamamlandığı.
3. **Anlamlı Token Oranı**: Tokenlerin kaçının dil açısından anlamlı olduğu.
4. **Token Saflığı (Özlük)**: Tokenlerin kaçının anlam kaybı olmadan daha küçük parçalara bölünmeden kullanılabildiği.
5. **Sözlük Boyutu**: Tokenizer'ın sözlük boyutunun büyüklüğü.

---

## Kriterlerin Amaçları 

- **Token Sayısı**: 
  Train aşamasında kullanılacak bir metnin daha az tokene bölünmesi, hem kelimelerin daha kapsamlı tokenleştirildiğini hem de işlemlerin daha hızlı tamamlanacağını gösterir.

- **Anlamlı Token Oranı**: 
  Anlamlı tokenlerin yüksek olması, embedding matrisinde bu tokenlerin temsil ettiği anlamların daha tutarlı ve doğru şekilde modellenmesini sağlar.

- **Token Saflığı (Özlük Oranı)**: 
  Bir tokenin daha küçük parçalara ayrılmadan aynı anlamı koruyabiliyor olması, dilin anlam desenlerini daha iyi yakalayan bir tokenizer için kritik öneme sahiptir. Tokenlerin özlü olması, corpus değerini artırır ve modelin eğitimi sırasında anlam kaybını en aza indirir.

- **Sözlük Boyutu**: 
  Daha küçük bir sözlük, hem eğitim sırasında hem de tahmin aşamasında daha hızlı ve verimli çalışmayı sağlar. Bununla birlikte, sözlük boyutunun gereksiz yere büyük olması modelin boyutunu artırabilir ve performansı olumsuz etkileyebilir.

- **Hız**: 
  Hem train sürecinde corpusun tokenleştirilmesi sırasında hem de kullanıcıların büyük metinleri işlerken karşılaşacağı gecikmeleri en aza indirmek için önemlidir.

---

## Maddelerin Uygulanması

*İlgili maddelerin uygulanması ile ilgili fikirler:*

- Tokenlerin anlamlı olup olmadığı `isTurkish()` fonksiyonu ile kontrol edilebilir. 
- Eğer token bir `predefined_word` ise `isTurkish()` fonksiyonunu çalıştırmaya gerek yok.

## İlk Sonuçlar

1605376 karakter ve 198193 boşluklarla ayrılmış kelime içeren bir metin üzerinde 14 farklı tokenizer çalıştırıldı. Tokenizer'ların performansı aşağıdaki kriterlere göre değerlendirildi:

1. **Toplam Token Sayısı**: Metnin kaç tokene ayrıldığı.
2. **Tokenleştirme Süresi**: Tokenleştirme işleminin ne kadar sürede tamamlandığı.
3. **Anlamlı Token Sayısı ve Oranı**: Tokenlerin kaçının anlamlı olduğu ve bunun toplam token sayısına oranı.
4. **Saf Token Sayısı ve Oranı (Özlük)**: Tokenlerin kaçının daha küçük parçalara ayrılmadan aynı anlamı koruduğu ve bunun toplam token sayısına oranı.
5. **Benzersiz Token Sayısı**: Tokenizer'ın oluşturduğu benzersiz tokenlerin sayısı.
6. **Sözlük Boyutu (Vocab Size)**: Her bir tokenizer'ın sözlük kapasitesi.

Bu analiz, Türkçe metinlerin tokenleştirilmesinde dilin morfolojik yapısına uygun ve verimli tokenizer geliştirmek için önemli sonuçlar sağlamaktadır.

| Tokenizer                                | Vocab Size | Token Count | Time   | Unique Token Count | Turkish Token Count | Turkish Token % | Pure Token Count | Pure Token % |
|------------------------------------------|------------|-------------|--------|---------------------|---------------------|-----------------|------------------|--------------|
| google/gemma-2-9b                        | 256,000    | 497,015     | 2.95   | 6,383               | 3,104               | 0.4863          | 2,365            | 0.3705       |
| alibayram/tr_tokenizer                   | 30,158     | 476,556     | 2.4231 | 11,531              | 11,342              | 0.9836          | 11,055           | 0.9587       |
| AhmetSemih/tr_tokenizer                  | 59,572     | 451,883     | 2.4849 | 13,370              | 13,253              | 0.9912          | 13,357           | 0.999        |
| aliarda/turkish_tokenizer_256k           | 256,000    | 488,267     | 2.5124 | 13,631              | 13,351              | 0.9795          | 12,981           | 0.9523       |
| aliarda/turkish_tokenizer                | 58,526     | 451,936     | 2.3406 | 13,268              | 13,170              | 0.9926          | 13,256           | 0.9991       |
| meta-llama/Llama-3.2-3B                  | 128,256    | 488,535     | 3.1249 | 6,823               | 3,125               | 0.458           | 2,109            | 0.3091       |
| utter-project/EuroLLM-9B-Instruct        | 128,000    | 497,173     | 3.2019 | 5,226               | 2,457               | 0.4701          | 1,838            | 0.3517       |
| Qwen/Qwen2.5-7B-Instruct                 | 151,665    | 561,866     | 3.315  | 5,752               | 2,320               | 0.4033          | 1,734            | 0.3015       |
| CohereForAI/aya-expanse-8b               | 255,029    | 434,526     | 2.7651 | 8,562               | 4,338               | 0.5067          | 2,822            | 0.3296       |
| openai-community/gpt2                    | 50,257     | 821,139     | 4.3765 | 3,454               | 1,582               | 0.458           | 1,119            | 0.324        |
| mistralai/Mistral-Nemo-Instruct-2407     | 131,072    | 534,930     | 3.1405 | 4,354               | 1,971               | 0.4527          | 1,571            | 0.3608       |
| microsoft/Phi-3.5-mini-instruct          | 32,011     | 803,971     | 4.5526 | 3,640               | 1,599               | 0.4393          | 1,253            | 0.3442       |
| Trendyol/Trendyol-LLM-8b-chat-v2.0       | 128,256    | 488,535     | 3.0438 | 6,823               | 3,125               | 0.458           | 2,109            | 0.3091       |
| ytu-ce-cosmos/turkish-gpt2-large-750m-v0 | 50,258     | 339,852     | 2.4044 | 22,746              | 17,529              | 0.7706          | 6,291            | 0.2766       |