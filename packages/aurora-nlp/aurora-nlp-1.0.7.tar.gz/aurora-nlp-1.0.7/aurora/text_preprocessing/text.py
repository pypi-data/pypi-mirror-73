import re
import string
from flashtext import KeywordProcessor
replace_list = {
        'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé','ỏe': 'oẻ',
        'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ','ụy': 'uỵ', 'uả': 'ủa',
        'ả': 'ả', 'ố': 'ố', 'u´': 'ú','ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ', '?': ' ', ',': ' ', '.': ' ',
        'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề','ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ', ' r ': ' rồi ',
        'ẻ': 'ẻ', 'ak': 'à', 'àk': 'à','aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ','ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á', ' k ': ' không ', 'kh ': 'không ',
        #dưới 3* quy về 1*, trên 3* quy về 5*
        '6 sao': ' 5star ','6 star': ' 5star ', '5star': ' 5star ','5 sao': ' 5star ','5sao': ' 5star ',
        'starstarstarstarstar': ' 5star ', '1 sao': ' 1star ', '1sao': ' 1star ','2 sao':' 1star ','2sao':' 1star ',
        '2 starstar':' 1star ','1star': ' 1star ', '0 sao': ' 1star ', '0star': ' 1star ',}

keyword_dict = {
    ' ': ["👹", "👻", "💃", '🤙', '👍', "💄", "💎", "💩", "😕", "😱", "😸", "😾", "🚫", "🤬", "🧚", "🧡", '🐶', '👎',
          '😣', '✨', '❣', '☀', '♥', '🤩', '💌', '🤣', '🖤', '🤤', ':(', '😢', '❤', '😍', '😘', '😪', '😊', '😁',
          '💖', '😟', '😭', '💯', '💗', '♡', '💜', '🤗', '^^', '😨', '☺', '💋', '👌', '😖', '😀', ':((', '😡', '😠',
          '😒', '🙂', '😏', '😝', '😄', '😙', '😤', '😎', '😆', '💚', '✌', '💕', '😞', '😓', '️🆗️', '😉', '😂', ':v',
          '=))',
          '😋', '💓', '😐', ':3', '😫', '😥', '😃', '😬', ' 😬 ', '😌', ' 😌 ', '💛', '🤝', '🎈', '😗', '🤔', '😑',
          '🔥', '🙏',
          '🆗', '😻', '💙', '💟', '😚', '❌', '👏', ';)', '<3', '🌝', '🌷', '🌸', '🌺', '🌼', '🍓', '🐅', '🐾', '👉',
          '💐', '💞',
          '💥', '💪', '💰', '😇', '😛', '😜', '🙃', '🤑', '🤪', '☹', '💀', '😔', '😧', '😩', '😰', '😳', '😵', '😶',
          '🙁', ':))',
          ':)', ':d', ':]]', ':]', 'roleyes', 'he he', 'hehe', 'hihi', 'haha', 'hjhj', 'lol', '“', '><', 'haizzz',
          'vl'],
    'ok': ['ok', 'ô kêi', 'okie', 'o kê', 'okey', 'ôkê', 'okay', 'oki', 'oke', 'okê'], 'điện thoại thông minh': ['smp'],
    'cảm ơn': ['cảm ơn', 'cám ơn', 'tks', 'thks', 'thanks', 'ths', 'thank you', 'thank u'],
    'không': ['không', 'hông', 'hem', 'kô', 'hok', 'ko', 'khong', 'k0'],
    'giống': ['giống', 'simili', 'similar', 'giốg'], 'không phải': ['kp'],
    'đéo': ['đéo', 'del', 'dél', 'éo'], 'dễ thương': ['cute', 'dễ thg', 'dthg'], 'với': ['vs', 'zới'],
    'vậy': ['zỵ', 'zị', 'dẹ', 'dỵ', 'zậy'], 'được': ['đươc', 'đc', 'đk', 'dk', 'dc', 'đx'],
    'quá': ['wa', 'wá', 'qá'], 'đường dẫn': ['link'], 'kích cỡ': ['sz', 'size'],
    'chuẩn chính hãng': ['authentic', 'auth'], 'xóa': ['delete', 'del'], 'xấu': ['sấu', 'xau'],
    'thích': ['thick', 'thk', 'thich', 'thch', 'thik', 'like'],
    'tốt': ['good', 'god', 'gút', 'gut', 'tot', 'tôt', 'nice', 'gud', 'wel done'], 'perfect': ['rất tốt'],
    'cửa hàng': ['store', 'shop', 'shopE', 'sop'], 'sản phẩm': ['sp', 'product'], 'cảm nhận': ['review'],
    'chiết khấu': ['comision'], 'bình thường': ['bt', 'bthg', 'btg', 'bình thg', 'bình tg'],
    'thời gian': ['time', 'tgian', 'thgian'], 'giao hàng': ['ship', 'síp', 'delivery'],
    'mình': ['mik', 'mh', 'mih', 'mìh'], 'tôi cũng vậy': ['me too'],
    'chất lượng': ['quality', 'chat lượng', 'chất lg'], 'hoàn hảo': ['excelent'], 'tệ': ['bad', 'sad', 'por', 'poor'],
    'tươi': ['fresh'], 'hạn sử dụng': ['date', 'exp', 'expiry date', 'hsd'],
    'nhanh': ['quickly', 'quick', 'fast'], 'phóng to': ['zoom'], 'đẹp': ['beautiful', 'đep', 'dep'],
    'trả lời': ['tl', 'trl', 'rep', 'repply'], 'rồi': ['rồi', 'roài', 'rùi'],
    'đặt hàng': ['order'], 'sử dụng': ['sd', 'sử dg', 'sử dụg'], 'điện thoại': ['đt', 'đthoai'],
    'nhắn tin': ['nt', 'inbox', 'inbx', 'ib'], 'xài': ['sài'], 'có': ['coá'],
    'bây giờ': ['bi h', 'bi giờ', 'bây h', 'bjo', 'bi jờ'], 'facebook': ['fb', 'fbook'], 'rất': ['rất', 'very'],
    'ngon': ['delicious'], 'hàng': ['hàg'], 'giả mạo': ['fake'],
    'quả': ['qủa'], 'yêu': ['love', 'iu', 'iêu'], 'bạn': ['you'], 'phản hồi': ['fback', 'fedback'], 'gì': ['gì', 'ji'],
    'gì ': ['j '], 'chú trọng': ['grace', 'chú trọng', 'chú chọng', 'trú trọng', 'trú chọng'],
    'anh em': ['ae'], 'miễn phí': ['free', 'fre'], 'đáng yêu': ['lovely', 'đáng iu', 'đáng iêu'], 'vui': ['zui'],
    'vẻ': ['zẻ'], 'tuyệt vời': ['toẹt vời', 'tuyệt zời', 'toẹt zời', 'great']
}

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
        keyword_processor = KeywordProcessor(case_sensitive=False)
        keyword_processor.add_keywords_from_dict(keyword_dict)
        self.text = keyword_processor.replace_keywords(text)

        # chuyen punctuation thành space
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        self.text = self.text.translate(translator)

        remove = regex.compile(r'[\p{C}|\p{M}|\p{P}|\p{S}|\p{Z}]+', regex.UNICODE)
        self.text = remove.sub(u" ", text).strip()
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
