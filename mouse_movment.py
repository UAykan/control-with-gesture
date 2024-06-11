import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import pyautogui

# Önceki fare konumu
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Mediapipe kütüphanesini kullanarak el algılama modelini yükler
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Kamerayı başlat
wCap, hCap = 1920, 1080 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCap)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCap)

# Ekran genişliği ve yüksekliği
wScr, hScr = pyautogui.size()

# Pycaw kütüphanesi ile ses kontrolü için gerekli ayarlar
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# El algılama modelini başlat
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Görüntüyü el algılama modeline geçirme
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Eğer el algılama başarılı olursa
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # İşaret parmağı ve başparmak uç noktalarının koordinatlarını al
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                
                # Ekran boyutlarına göre koordinatları yeniden ölçeklendir
                cx, cy = int(index_finger_tip.x * wCap), int(index_finger_tip.y * hCap)
                tx, ty = int(thumb_tip.x * wCap), int(thumb_tip.y * hCap)
                
                # Fare pozisyonunu bul ve yatay hareketi tersine çevir
                x = np.interp(cx, [0, wCap], [wScr, 0])
                y = np.interp(cy, [0, hCap], [0, hScr])
                
                # Yumuşatma olmadan fareyi hareket ettir
                pyautogui.moveTo(x, y)
                plocX, plocY = x, y

                # İşaret parmağı ve başparmak arasındaki mesafeyi hesapla
                length = hypot(tx - cx, ty - cy)
                
                # Eğer bu mesafe belirli bir eşiğin altına inerse tıklama yap
                if length < 50:
                    pyautogui.click()

        # Görüntüyü ekrana çizdirme
        cv2.imshow('Hand Tracking', frame)

        # Çıkış için 'q' tuşuna basıldığında döngüyü kır
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Kamerayı ve pencereyi kapat
cap.release()
cv2.destroyAllWindows()
