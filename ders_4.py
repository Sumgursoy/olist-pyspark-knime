# Ders 4: İki şartla filtrelemek, tarihler ve yeni sütun eklemek

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("Ders4")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

siparisler = spark.read.csv("data/olist_orders_dataset.csv", header=True, inferSchema=True)


print("\n========== 1) TARİHTEN YIL VE AY ÇIKAR (yeni sütun) ==========")
# withColumn("yeni_sütun_adı", nasıl_hesaplanacak)
siparisler = (
    siparisler
    .withColumn("yil", F.year("order_purchase_timestamp"))
    .withColumn("ay", F.month("order_purchase_timestamp"))
)
siparisler.select("order_purchase_timestamp", "yil", "ay").show(5)


print("\n========== 2) İKİ ŞART: TESLİM EDİLMİŞ VE 2017'DE VERİLMİŞ ==========")
# &  = VE (iki şart da doğru olmalı)
# |  = VEYA (biri doğru olsa yeter)
# Her şart kendi parantezinin içinde olmalı!
teslim_2017 = siparisler.filter(
    (F.col("order_status") == "delivered") & (F.col("yil") == 2017)
)
print("2017'de verilip teslim edilen sipariş sayısı:", teslim_2017.count())


print("\n========== 3) TESLİMAT KAÇ GÜN SÜRDÜ? ==========")
# datediff(bitiş, başlangıç) = iki tarih arasındaki gün farkı
teslim_edilenler = (
    siparisler
    .filter(F.col("order_status") == "delivered")
    .withColumn("teslim_suresi_gun",
                F.datediff("order_delivered_customer_date", "order_purchase_timestamp"))
)
teslim_edilenler.select("order_purchase_timestamp",
                        "order_delivered_customer_date",
                        "teslim_suresi_gun").show(5)


print("\n========== 4) GEÇ KALAN SİPARİŞLER ==========")
# Müşteriye ulaştığı tarih > tahmini teslim tarihi ise geç kalmış demektir
gec_kalanlar = teslim_edilenler.filter(
    F.col("order_delivered_customer_date") > F.col("order_estimated_delivery_date")
)
toplam = teslim_edilenler.count()
gec = gec_kalanlar.count()
print("Teslim edilen:", toplam)
print("Geç kalan:", gec)
print("Geç kalma oranı: %", round(gec / toplam * 100, 1))


spark.stop()
