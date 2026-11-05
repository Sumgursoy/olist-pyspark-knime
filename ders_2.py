# Ders 2: CSV okumak ve veriyi tanımak

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Ders2")
    .master("local[*]")
    .getOrCreate()
)

# Uyarı (WARN) mesajlarını gizle, sadece hataları göster
spark.sparkContext.setLogLevel("ERROR")

# 1) CSV dosyasını oku
urunler = spark.read.csv(
    "data/olist_products_dataset.csv",
    header=True,        # ilk satır sütun adları
    inferSchema=True    # her sütunun tipini (sayı, tarih, yazı) Spark tahmin etsin
)

# 2) İlk 5 satırı göster
urunler.show(5)

# 3) Şemayı göster: hangi sütunlar var, tipleri ne
urunler.printSchema()

# 4) Kaç satır var
print("Satır sayısı:", urunler.count())

# 5) Sütun adlarının listesi
print("Sütunlar:", urunler.columns)

spark.stop()
