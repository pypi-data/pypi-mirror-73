import re
import string
replace_list = {
    'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé', 'ỏe': 'oẻ',
    'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ', 'ụy': 'uỵ', 'uả': 'ủa',
    'ả': 'ả', 'ố': 'ố', 'u´': 'ố', 'ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ',
    'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề', 'ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ',
    'ẻ': 'ẻ', 'àk': u' à ', 'aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ', 'ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á',
    # Quy các icon về 2 loại emoj: Tích cực hoặc tiêu cực
    "👹": "negative", "👻": "positive", "💃": "positive", '🤙': ' positive ', '👍': ' positive ',
    "💄": "positive", "💎": "positive", "💩": "positive", "😕": "negative", "😱": "negative", "😸": "positive",
    "😾": "negative", "🚫": "negative", "🤬": "negative", "🧚": "positive", "🧡": "positive", '🐶': ' positive ',
    '👎': ' negative ', '😣': ' negative ', '✨': ' positive ', '❣': ' positive ', '☀': ' positive ',
    '♥': ' positive ', '🤩': ' positive ', 'like': ' positive ', '💌': ' positive ',
    '🤣': ' positive ', '🖤': ' positive ', '🤤': ' positive ', ':(': ' negative ', '😢': ' negative ',
    '❤': ' positive ', '😍': ' positive ', '😘': ' positive ', '😪': ' negative ', '😊': ' positive ',
    '?': ' ? ', '😁': ' positive ', '💖': ' positive ', '😟': ' negative ', '😭': ' negative ',
    '💯': ' positive ', '💗': ' positive ', '♡': ' positive ', '💜': ' positive ', '🤗': ' positive ',
    '^^': ' positive ', '😨': ' negative ', '☺': ' positive ', '💋': ' positive ', '👌': ' positive ',
    '😖': ' negative ', '😀': ' positive ', ':((': ' negative ', '😡': ' negative ', '😠': ' negative ',
    '😒': ' negative ', '🙂': ' positive ', '😏': ' negative ', '😝': ' positive ', '😄': ' positive ',
    '😙': ' positive ', '😤': ' negative ', '😎': ' positive ', '😆': ' positive ', '💚': ' positive ',
    '✌': ' positive ', '💕': ' positive ', '😞': ' negative ', '😓': ' negative ', '️🆗️': ' positive ',
    '😉': ' positive ', '😂': ' positive ', ':v': '  positive ', '=))': '  positive ', '😋': ' positive ',
    '💓': ' positive ', '😐': ' negative ', ':3': ' positive ', '😫': ' negative ', '😥': ' negative ',
    '😃': ' positive ', '😬': ' 😬 ', '😌': ' 😌 ', '💛': ' positive ', '🤝': ' positive ', '🎈': ' positive ',
    '😗': ' positive ', '🤔': ' negative ', '😑': ' negative ', '🔥': ' negative ', '🙏': ' negative ',
    '🆗': ' positive ', '😻': ' positive ', '💙': ' positive ', '💟': ' positive ',
    '😚': ' positive ', '❌': ' negative ', '👏': ' positive ', ';)': ' positive ', '<3': ' positive ',
    '🌝': ' positive ', '🌷': ' positive ', '🌸': ' positive ', '🌺': ' positive ',
    '🌼': ' positive ', '🍓': ' positive ', '🐅': ' positive ', '🐾': ' positive ', '👉': ' positive ',
    '💐': ' positive ', '💞': ' positive ', '💥': ' positive ', '💪': ' positive ',
    '💰': ' positive ', '😇': ' positive ', '😛': ' positive ', '😜': ' positive ',
    '🙃': ' positive ', '🤑': ' positive ', '🤪': ' positive ', '☹': ' negative ', '💀': ' negative ',
    '😔': ' negative ', '😧': ' negative ', '😩': ' negative ', '😰': ' negative ', '😳': ' negative ',
    '😵': ' negative ', '😶': ' negative ', '🙁': ' negative ',
    # Chuẩn hóa 1 số sentiment words/English words
    ':))': '  positive ', ':)': ' positive ', 'ô kêi': ' ok ', 'okie': ' ok ', ' o kê ': ' ok ',
    'okey': ' ok ', 'ôkê': ' ok ', 'oki': ' ok ', ' oke ': ' ok ', ' okay': ' ok ', 'okê': ' ok ',
    ' tks ': u' cám ơn ', 'thks': u' cám ơn ', 'thanks': u' cám ơn ', 'ths': u' cám ơn ', 'thank': u' cám ơn ',
    '⭐': 'star ', '*': 'star ', '🌟': 'star ', '🎉': u' positive ', 'roleyes': ' positive ',
    'kg ': u' không ', 'not ': u' không ', u' kg ': u' không ', '"k ': u' không ', ' kh ': u' không ', 'kô': u' không ',
    'hok': u' không ', ' kp ': u' không phải ', u' kô ': u' không ', '"ko ': u' không ', u' ko ': u' không ',
    u' k ': u' không ', 'khong': u' không ', u' hok ': u' không ',
    'he he': ' positive ', 'hehe': ' positive ', 'hihi': ' positive ', 'haha': ' positive ', 'hjhj': ' positive ',
    ' lol ': ' negative ', ' cc ': ' negative ', 'cute': u' dễ thương ', 'huhu': ' negative ', ' vs ': u' với ',
    'wa': ' quá ', 'wá': u' quá', 'j': u' gì ', '“': ' ',
    ' sz ': u' cỡ ', 'size': u' cỡ ', u' đx ': u' được ', 'dk': u' được ', 'dc': u' được ', 'đk': u' được ',
    'đc': u' được ', 'authentic': u' chuẩn chính hãng ', u' aut ': u' chuẩn chính hãng ',
    u' auth ': u' chuẩn chính hãng ', 'thick': u' positive ', 'store': u' cửa hàng ',
    'shop': u' cửa hàng ', 'sp': u' sản phẩm ', 'gud': u' tốt ', 'god': u' tốt ', 'wel done': ' tốt ', 'good': u' tốt ',
    'gút': u' tốt ',
    'sấu': u' xấu ', 'gut': u' tốt ', u' tot ': u' tốt ', u' nice ': u' tốt ', 'perfect': 'rất tốt',
    'bt': u' bình thường ',
    'time': u' thời gian ', 'qá': u' quá ', u' ship ': u' giao hàng ', u' m ': u' mình ', u' mik ': u' mình ',
    'ể': 'ể', 'product': 'sản phẩm', 'quality': 'chất lượng', 'chat': ' chất ', 'excelent': 'hoàn hảo', 'bad': 'tệ',
    'fresh': ' tươi ', 'sad': ' tệ ',
    'date': u' hạn sử dụng ', 'hsd': u' hạn sử dụng ', 'quickly': u' nhanh ', 'quick': u' nhanh ', 'fast': u' nhanh ',
    'delivery': u' giao hàng ', u' síp ': u' giao hàng ',
    'beautiful': u' đẹp tuyệt vời ', u' tl ': u' trả lời ', u' r ': u' rồi ', u' shopE ': u' cửa hàng ',
    u' order ': u' đặt hàng ',
    'chất lg': u' chất lượng ', u' sd ': u' sử dụng ', u' dt ': u' điện thoại ', u' nt ': u' nhắn tin ',
    u' tl ': u' trả lời ', u' sài ': u' xài ', u'bjo': u' bao giờ ',
    'thik': u' thích ', u' sop ': u' cửa hàng ', ' fb ': ' facebook ', ' face ': ' facebook ', ' very ': u' rất ',
    u'quả ng ': u' quảng  ',
    'dep': u' đẹp ', u' xau ': u' xấu ', 'delicious': u' ngon ', u'hàg': u' hàng ', u'qủa': u' quả ', '<': u'',
    '>': u'',
    'iu': u' yêu ', 'fake': u' giả mạo ', 'trl': 'trả lời', '><': u' positive ', 'great': u' tuyệt vời',
    ' por ': u' tệ ', ' poor ': u' tệ ', 'ib': u' nhắn tin ', 'rep': u' trả lời ', u'fback': ' feedback ',
    'fedback': ' feedback ',
    # dưới 3* quy về 1*, trên 3* quy về 5*
    '6 sao': ' 5star ', '6 star': ' 5star ', '5star': ' 5star ', '5 sao': ' 5star ', '5sao': ' 5star ',
    'starstarstarstarstar': ' 5star ', '1 sao': ' 1star ', '1sao': ' 1star ', '2 sao': ' 1star ', '2sao': ' 1star ',
    '2 starstar': ' 1star ', '1star': ' 1star ', '0 sao': ' 1star ', '0star': ' 1star ', }


class Text:
    def __init__(self, text):
        self.text = text
        self.to_string()
        self.lowercase()

    def to_string(self):
        self.text = str(self.text)

    def lowercase(self):
        self.text = self.text.lower()

    def normalize(self):
        self.punctuate()
        self.regex_normalize()
        return self.text

    def punctuate(self):
        for k, v in replace_list.items():
            self.text = self.text.replace(k, v)

    def regex_normalize(self):
        patterns = ['\[([^\]=]+)(?:=[^\]]+)?\].*?\[\/\\1\\n]', r'\b(?:(?:https?|ftp)://)?\w[\w-]*(?:\.[\w-]+)+\S*',
                    "[\(\[].*?[\)\]]"]
        for pattern in patterns:
            self.text = re.sub(pattern, '', self.text)
        # chuyen punctuation thành space
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        self.text = self.text.translate(translator)

        # remove nốt những ký tự thừa
        self.text = self.text.replace(u'"', u' ')
        self.text = self.text.replace(u'️', u'')
        self.text = self.text.replace('🏻', '')

        self.text = re.sub(r'(\D)\1+', r'\1', self.text)
        self.text = self.text.replace('\r', '')
        # Remove numbers
        self.text = re.sub(r'\d+', ' ', self.text)
        # Removing multiple spaces
        self.text = re.sub(r'\s+', ' ', self.text)
        # Remove các ký tự kéo dài: vd: đẹppppppp
        self.text = re.sub(r'([A-Z])\1+', lambda m: m.group(1), self.text, flags=re.IGNORECASE)

        self.text = self.text.strip()
