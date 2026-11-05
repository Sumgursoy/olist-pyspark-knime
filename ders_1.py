# Ders 1: Spark'ı başlatmak

# 1) pyspark.sql modülünden SparkSession sınıfını al
from pyspark.sql import SparkSession

# 2) Oturumu (SparkSession) oluştur ve "spark" değişkenine ata
spark = (
    SparkSession.builder
    .appName("Ders1")        # uygulamanın adı (istediğin isim olabilir)
    .master("local[*]")      # kendi bilgisayarımda, tüm çekirdeklerle çalış
    .getOrCreate()           # varsa var olanı ver, yoksa yenisini oluştur
)

# 3) Spark'ın sürümünü ekrana yazdır
print("Spark sürümü:", spark.version)

# 4) İşimiz bitti, oturumu kapat
spark.stop()
