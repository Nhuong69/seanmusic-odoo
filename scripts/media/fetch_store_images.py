"""Download product reference photos with an auditable source manifest."""
import concurrent.futures
import json
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin

import requests
from lxml import html
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "assets/products/references"
SOURCES = {
    "GUITAR-NS2NA": "https://www.tanglewoodguitars.co.uk/product/ns2na/",
    "GUITAR-NS1MC": "https://www.tanglewoodguitars.co.uk/product/ns1mc/",
    "GUITAR-NS1BL": "https://www.tanglewoodguitars.co.uk/product/ns1bl/",
    "GUITAR-DONNER-HUSHC": "https://us.donnermusic.com/products/donner-hush-c-guitar",
    "GUITAR-DONNER-HUSHIPRO": "https://us.donnermusic.com/products/donner-hush-i-pro-acoustic-electric-travel-guitar-kit",
    "GUITAR-DONNER-HUSHXPRO": "https://uk.donnermusic.com/products/donner-hush-x-pro-guitar",
    "GUITAR-DONNER-DST100": "https://store.vietthuong.vn/products/dan-guitar-dien-donner-dst-100-kem-am-ly-phu-kien",
    "GUITAR-FENDER-PLAYER2": "https://store.vietthuong.vn/products/fender-dan-guitar-dien-player-ii-strat-hss-rw-3ts-0140540500",
    "AMP-BLACKSTAR-FLY3": "https://store.vietthuong.vn/products/blackstar-fly-3-bluetooth",
    "AMP-FENDER-LT25": "https://store.vietthuong.vn/products/fender-combo-ampli-die-n-mustang-lt25-230v-25w-2311106000",
    "DRUM-ALESIS-TURBO": "https://store.vietthuong.vn/products/alesis-turbo-mesh-kit",
    "AMP-BLACKSTAR-BA102019": "https://store.vietthuong.vn/products/blackstar-fly3-bass",
    "AMP-BS-AMPLUG2": "https://store.vietthuong.vn/products/blackstar-amplug2-fly-guitar",
    "AMP-BS-DEBUT10E": "https://store.vietthuong.vn/products/blackstar-debut-10e",
    "AMP-BS-DEBUT15E": "https://store.vietthuong.vn/products/blackstar-debut-15e",
    "AMP-ROLAND-CUBE10GX": "https://store.vietthuong.vn/products/roland-cube-10gx",
    "AMP-DONNER-DA10B": "https://store.vietthuong.vn/products/donner-amply-guitar-dien-da-10b-vintage-white",
    "AMP-FISHMAN-LBMINI": "https://vietmusic.vn/products/amplifier-fishman-loudbox-mini",
    "DRUM-ALESIS-DEBUT": "https://store.vietthuong.vn/products/alesis-debut-kit-bo-trong-dien-tu",
    "DRUM-ALESIS-SURGESE": "https://store.vietthuong.vn/products/alesis-surge-se-kit-bo-trong-dien-tu",
    "DRUM-ROLAND-TD02KV": "https://store.vietthuong.vn/products/roland-td-02kv-bo-trong-dien-tu",
}


def download(entry):
    code, page = entry
    try:
        response = requests.get(page, timeout=25)
        response.raise_for_status()
        tree = html.fromstring(response.content)
        urls = tree.xpath('//meta[@property="og:image"]/@content')
        if not urls:
            raise ValueError("No product image metadata")
        url = urljoin(page, urls[0])
        photo = requests.get(url, timeout=25)
        photo.raise_for_status()
        img = Image.open(BytesIO(photo.content))
        if min(img.size) < 200:
            raise ValueError("Image too small")
        filename = DEST / (code.lower() + "." + ("png" if img.format == "PNG" else "jpg"))
        filename.write_bytes(photo.content)
        print(code, img.size, "OK", flush=True)
        return code, {"page": page, "url": url, "file": str(filename.relative_to(ROOT))}
    except Exception as error:
        print(code, type(error).__name__, str(error)[:150], flush=True)
        return code, None


if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    manifest_path = DEST / "sources.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        remaining = [(code, page) for code, page in SOURCES.items() if code not in manifest]
        for code, data in pool.map(download, remaining):
            if data:
                manifest[code] = data
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
