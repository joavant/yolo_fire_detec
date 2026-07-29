import time
import urllib.parse
import urllib.request
from maix import app, camera, display, image, nn

# ==========================================
# ⚙️ CONFIGURATION (Modifie ici facilement)
# ==========================================
MODEL_PATH = "/root/models/best.cvimodel"
CONF_THRESHOLD = 0.50
IOU_THRESHOLD = 0.45

# --- Alerte Telegram ---
TELEGRAM_ENABLED = False
BOT_TOKEN = "TON_BOT_TOKEN_ICI"
CHAT_ID = "TON_CHAT_ID_ICI"
COOLDOWN_ALERT = 10  # Secondes entre deux alertes pour éviter le spam

# ==========================================
# 🚀 INITIALISATION
# ==========================================
print("⏳ Chargement du modèle sur le NPU...")
detector = nn.YOLOv8(model=MODEL_PATH)

print("📷 Démarrage de la caméra...")
cam = camera.Camera(
    detector.input_width(), detector.input_height(), detector.input_format()
)
disp = display.Display()

last_alert_time = 0


def send_telegram_alert(label, confidence):
  """Envoie une alerte rapide sur Telegram."""
  try:
    text = (
        f"🔥 **ALERTE FEU** 🔥\nObjet : {label.upper()}\nConfiance :"
        f" {confidence * 100:.1f}%"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=3):
      pass
    print(f"📲 Alerte envoyée pour : {label}")
  except Exception as e:
    print(f"❌ Erreur Telegram : {e}")


# ==========================================
# 🔄 BOUCLE PRINCIPALE
# ==========================================
print("✅ C'est parti ! Appuie sur Ctrl+C pour stopper.")

while not app.need_exit():
  # 1. Capture de l'image
  img = cam.read()

  # 2. Détection IA
  objs = detector.detect(img, conf=CONF_THRESHOLD, iou=IOU_THRESHOLD)

  detected = False
  top_label = ""
  top_conf = 0.0

  # 3. Dessin des boîtes de détection
  for obj in objs:
    label = (
        detector.labels[obj.class_id]
        if detector.labels
        else f"Class {obj.class_id}"
    )
    conf = obj.score

    # Dessine le rectangle et le texte sur l'image
    img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED, thickness=2)
    img.draw_string(
        obj.x,
        max(0, obj.y - 20),
        f"{label} {conf * 100:.0f}%",
        color=image.COLOR_RED,
        scale=1.5,
    )

    if conf > top_conf:
      top_conf = conf
      top_label = label
      detected = True

  # 4. Gestion du cooldown Telegram
  now = time.time()
  if TELEGRAM_ENABLED and detected and (now - last_alert_time > COOLDOWN_ALERT):
    send_telegram_alert(top_label, top_conf)
    last_alert_time = now

  # 5. Affichage sur l'écran de la MaixCAM
  disp.show(img)
