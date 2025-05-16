from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import re 
#SON ÇALIŞAN KOD cidden açksjnşalsk
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")
chrome_options.add_argument("accept-language=tr-TR,tr;q=0.9")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 10)
products = []

import time


for sayfa_no in range(1, 21):  # 100 sayfa için
    url = f"https://www.hepsiburada.com/telefonlar-c-2147483642?sayfa={sayfa_no}"
    driver.get(url)
    print(f"{sayfa_no}. sayfa açıldı.")
    time.sleep(5)
        # Sayfanın toplam yüksekliğini al
    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_increment = 500  # Her seferinde 500 piksel kaydır
    current_position = 0

    while current_position < last_height:
        # Bir miktar kaydır
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(0.4)  # Yavaşlatmak için bekleme süresi (değeri değiştirebilirsin)
        
        # Sonraki pozisyon
        current_position += scroll_increment
        
        # Yeni yükleme olmuş mu diye kontrol et
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > last_height:
            last_height = new_height  # Yükleme olduysa total height'ı güncelle

    # Son olarak tamamen en alta kaydır
    driver.execute_script(f"window.scrollTo(0, {last_height});")
    


    product_cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[starts-with(@class, 'productListContent-')]")))

       

    for item in product_cards:
        try:
            link = item.find_element(By.CSS_SELECTOR, "a.productCardLink-module_productCardLink__GZ3eU").get_attribute("href")
            if "hepsiburada.com" not in link:
                continue  # Reklam ya da geçersiz link
        except:
            link = "Link yok"

        try:
            title = item.find_element(By.XPATH, ".//h2[contains(@class, 'title-module_titleRoot')]/span[contains(@class, 'title-module_titleText')]").text
        except:
            title = "YOK"

        try:
            price = item.find_element(By.CSS_SELECTOR, "div.price-module_finalPrice__LtjvY").text
        except:
            price = "Fiyat yok"

        try:
            rating = item.find_element(By.CSS_SELECTOR, "span.rate-module_rating__19oVu").text
        except:
            rating = "Puan yok"

        try:
            rating_count = item.find_element(By.CSS_SELECTOR, "span.rate-module_count__fjUng").text
            # Parantez içindeki sayıyı almak için regex kullanıyoruz
            rating_count = re.sub(r"[^\d]", "", rating_count)  # Sadece sayıları al
        except:
            rating_count = "Oylama yok"

        try:
            image_url = item.find_element(By.CSS_SELECTOR, "img.hbImageView-module_hbImage__Ca3xO").get_attribute("src")
        except:
            image_url = "Resim yok"

        products.append({
            "Ürün_Linki": link,
            "Ürün_Adı": title,
            "Ürün_Fiyatı": price,
            "Ürün_Puanı": rating,
            "Ürün_OySayısı": rating_count,
            "Ürün_Resmi": image_url
        })

driver.quit()

csv_file_name = "hepsiBurada_urunler.csv"
df = pd.DataFrame(products)
df.to_csv(csv_file_name, index=False, encoding="utf-8-sig")

print(f"✅ CSV dosyası başarıyla oluşturuldu: {csv_file_name}")

full_path = os.path.abspath(csv_file_name)
print("📁 Tam dosya yolu:", full_path)
