# Hamburger Oyunu v2

Skor kaydı, olay günlüğü ve istatistik grafikleri içeren üç kişilik proje yapısı.

## Klasör Yapısı

- `backend/logic.py`: Oyun kuralları, süreler, puanlama ve olay günlüğü (Kişi A)
- `frontend/ui.py`: Ekranlar, 1000x500 Canvas çizimleri, sürükle-bırak ve istatistik penceresi (Kişi B)
- `data/data_store.py`: Dosya yolları, sütun tanımları ve güvenli CSV kayıt/okuma (Kişi C)
- `data/analytics.py`: `pandas` ve `numpy` ile istatistik ve liderlik tablosu hesaplamaları (Kişi C)
- `data/charts.py`: `matplotlib` (`Figure`) ile 5 grafik üretimi (Kişi C)
- `data/sample_data.py`: Testler için sahte veri üretici (Kişi C)
- `test_data/`: Sahte test verilerinin yazıldığı dizin

## Kurulum ve Çalıştırma

```bash
pip install pandas numpy matplotlib
python main.py
```
