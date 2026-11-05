# Olist E-Ticaret Teslimat Analizi (PySpark & KNIME)

Brezilyalı e-ticaret şirketi Olist'in açık veri seti üzerinde, sipariş durumlarını ve teslimat performansını inceleyen bir öğrenme projesi. Aynı analiz hem **PySpark** koduyla hem de **KNIME** workflow'u ile yapılmış ve sonuçların iki araçta da aynı çıktığı doğrulanmıştır.

## Öne çıkan bulgular

| Metrik | Değer |
|---|---|
| Toplam sipariş | 99.441 |
| Teslim edilen sipariş | 96.478 (~%97) |
| Tahmini tarihten geç teslim edilen | 7.826 (%8,1) |
| Ortalama teslim süresi (2017 → 2018) | 13,0 gün → 12,1 gün |
| Geç kalma oranı (2017 → 2018) | %6,6 → %9,4 |

Ortalama teslim süresi kısalmasına rağmen geç kalma oranı artmıştır. Yani müşteriye verilen tahmini teslim tarihleri, teslimattaki hızlanmadan daha fazla kısalmış olabilir.

## Proje yapısı

```
├── ders_1.py   # SparkSession oluşturma
├── ders_2.py   # CSV okuma, şema inceleme
├── ders_3.py   # Sütun seçme (select) ve filtreleme (filter)
├── ders_4.py   # Tarih işlemleri, yeni sütun (withColumn), geç teslimat oranı
├── ders_5.py   # Gruplama (groupBy / agg) ile yıllık özetler
└── knime/      # Aynı analizin KNIME workflow'u (CSV Reader → Row Filter / GroupBy)
```

## Kullanılan araçlar

- **PySpark 4.3**: `select`, `filter`, `withColumn`, `groupBy`, `agg`, `when/otherwise`, `datediff`
- **KNIME Analytics Platform 5.12**: CSV Reader, Row Filter, GroupBy

## Çalıştırma

1. Veri setini Kaggle'dan indirin: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. CSV dosyalarını `data/` klasörüne koyun. Veri, boyutu ve lisansı nedeniyle bu depoya eklenmemiştir.
3. Bağımlılıkları kurun (Java 17 gereklidir):
   ```
   pip install -r requirements.txt
   ```
4. Dosyaları çalıştırın:
   ```
   python ders_5.py
   ```

KNIME workflow'unu açmak için: KNIME'da **File → Import KNIME Workflow** ile `knime/` klasöründeki `.knwf` dosyasını içe aktarın ve CSV Reader node'undaki dosya yolunu kendi `data/` klasörünüze göre güncelleyin.
