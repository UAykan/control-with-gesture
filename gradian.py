import cv2

# Görüntüyü oku
goruntu = cv2.imread('ornek.jpg')

# Görüntünün genişliğini ve yüksekliğini al
genislik, yukseklik, renk_kanal = goruntu.shape

# Görüntüyü gri tonlamaya çevir
goruntu_gri = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)

# Görüntüyü ekrana göster
cv2.imshow('Görüntü', goruntu)
cv2.imshow('Gri Tonlama', goruntu_gri)

# Beklet ve çık
cv2.waitKey(0)
cv2.destroyAllWindows()