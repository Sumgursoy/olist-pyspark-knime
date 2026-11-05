# Ders 3: Sütun seçmek ve satır filtrelemek

from pyspark.sql import SparkSession
from pyspark.sql import functions as F   # Spark'ın hazır fonksiyonları (kısaca F diyoruz)

spark = (
    SparkSession.builder
    .appName("Ders3")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

siparisler = spark.read.csv("data/olist_orders_dataset.csv", header=True, inferSchema=True)


print("\n========== 1) SADECE 2 SÜTUNU SEÇ ==========")
# select: istediğin sütunları al, gerisini gösterme
siparisler.select("order_id", "order_status").show(5)


print("\n========== 2) SİPARİŞ DURUMLARI NELER? ==========")
# distinct: tekrar edenleri at, her değeri bir kere göster
siparisler.select("order_status").distinct().show()


print("\n========== 3) SADECE TESLİM EDİLENLER ==========")
# filter: şarta uyan satırları tut, uymayanları at
teslim_edilenler = siparisler.filter(F.col("order_status") == "delivered")
print("Teslim edilen sipariş sayısı:", teslim_edilenler.count())


print("\n========== 4) STOKTA OLMAYANLAR (seç + filtrele birlikte) ==========")
stokta_yok = (
    siparisler
    .filter(F.col("order_status") == "unavailable")
    .select("order_id", "order_purchase_timestamp")
)
print("Stokta olmayan sipariş sayısı:", stokta_yok.count())
stokta_yok.show(5)


spark.stop()
