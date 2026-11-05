# Ders 5: Gruplama (groupBy) - Excel'deki Pivot Tablo

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("Ders5")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

siparisler = spark.read.csv("data/olist_orders_dataset.csv", header=True, inferSchema=True)
siparisler = siparisler.withColumn("yil", F.year("order_purchase_timestamp"))


print("\n========== 1) HER DURUMDAN KAÇ SİPARİŞ VAR? ==========")
# groupBy: aynı değere sahip satırları bir grupta topla
# count: her grupta kaç satır var say
(
    siparisler
    .groupBy("order_status")
    .count()
    .orderBy(F.desc("count"))    # çoktan aza sırala
    .show()
)


print("\n========== 2) HER YIL KAÇ SİPARİŞ VERİLMİŞ? ==========")
(
    siparisler
    .groupBy("yil")
    .count()
    .orderBy("yil")              # küçükten büyüğe sırala
    .show()
)


print("\n========== 3) HER YIL İÇİN BİRDEN FAZLA HESAP (agg) ==========")
# Önce sadece teslim edilenleri al, teslim süresini ve geç kalıp kalmadığını hesapla
teslim_edilenler = (
    siparisler
    .filter(F.col("order_status") == "delivered")
    .withColumn("teslim_suresi_gun",
                F.datediff("order_delivered_customer_date", "order_purchase_timestamp"))
    # geç kaldıysa 1, kalmadıysa 0
    .withColumn("gec_mi",
                F.when(F.col("order_delivered_customer_date") > F.col("order_estimated_delivery_date"), 1)
                 .otherwise(0))
)

# agg: her grup için birden fazla hesap yap
(
    teslim_edilenler
    .groupBy("yil")
    .agg(
        F.count("*").alias("siparis_sayisi"),                          # kaç sipariş
        F.round(F.avg("teslim_suresi_gun"), 1).alias("ort_teslim_gun"),  # ortalama kaç gün
        F.max("teslim_suresi_gun").alias("en_uzun_teslim_gun"),          # en uzun kaç gün
        F.sum("gec_mi").alias("gec_kalan"),                              # kaç tanesi geç kaldı
    )
    .orderBy("yil")
    .show()
)


spark.stop()
