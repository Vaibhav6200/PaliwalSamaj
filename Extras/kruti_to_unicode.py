import re
import pandas as pd

k2u = [
    (u'\xf1', u'\u0970'),  # ñ  ->  ॰
    (u'Q+Z', u'QZ+'),  # Q+Z  ->  QZ+
    (u'sas', u'sa'),  # sas  ->  sa
    (u'aa', u'a'),  # aa  ->  a
    (u')Z', u'\u0930\u094d\u0926\u094d\u0927'),  # )Z  ->  र्द्ध
    (u'ZZ', u'Z'),  # ZZ  ->  Z
    (u'\u2018', u'"'),  # ‘  ->  "
    (u'\u2019', u'"'),  # ’  ->  "
    (u'\u201c', u"'"),  # “  ->  '
    (u'\u201d', u"'"),  # ”  ->  '
    (u'\xe5', u'\u0966'),  # å  ->  ०
    (u'\u0192', u'\u0967'),  # ƒ  ->  १
    (u'\u201e', u'\u0968'),  # „  ->  २
    (u'\u2026', u'\u0969'),  # …  ->  ३
    (u'\u2020', u'\u096a'),  # †  ->  ४
    (u'\u2021', u'\u096b'),  # ‡  ->  ५
    (u'\u02c6', u'\u096c'),  # ˆ  ->  ६
    (u'\u2030', u'\u096d'),  # ‰  ->  ७
    (u'\u0160', u'\u096e'),  # Š  ->  ८
    (u'\u2039', u'\u096f'),  # ‹  ->  ९
    (u'\xb6+', u'\u095e\u094d'),  # ¶+  ->  फ़्
    (u'd+', u'\u0958'),  # d+  ->  क़
    (u'[+k', u'\u0959'),  # [+k  ->  ख़
    (u'[+', u'\u0959\u094d'),  # [+  ->  ख़्
    (u'x+', u'\u095a'),  # x+  ->  ग़
    (u'T+', u'\u091c\u093c\u094d'),  # T+  ->  ज़्
    (u't+', u'\u095b'),  # t+  ->  ज़
    (u'M+', u'\u095c'),  # M+  ->  ड़
    (u'<+', u'\u095d'),  # <+  ->  ढ़
    (u'Q+', u'\u095e'),  # Q+  ->  फ़
    (u';+', u'\u095f'),  # ;+  ->  य़
    (u'j+', u'\u0931'),  # j+  ->  ऱ
    (u'u+', u'\u0929'),  # u+  ->  ऩ
    (u'\xd9k', u'\u0924\u094d\u0924'),  # Ùk  ->  त्त
    (u'\xd9', u'\u0924\u094d\u0924\u094d'),  # Ù  ->  त्त्
    (u'\xe4', u'\u0915\u094d\u0924'),  # ä  ->  क्त
    (u'\u2013', u'\u0926\u0943'),  # –  ->  दृ
    (u'\u2014', u'\u0915\u0943'),  # —  ->  कृ
    (u'\xe9', u'\u0928\u094d\u0928'),  # é  ->  न्न
    (u'\u2122', u'\u0928\u094d\u0928\u094d'),  # ™  ->  न्न्
    (u'=kk', u'=k'),  # =kk  ->  =k
    (u'f=k', u'f='),  # f=k  ->  f=
    (u'\xe0', u'\u0939\u094d\u0928'),  # à  ->  ह्न
    (u'\xe1', u'\u0939\u094d\u092f'),  # á  ->  ह्य
    (u'\xe2', u'\u0939\u0943'),  # â  ->  हृ
    (u'\xe3', u'\u0939\u094d\u092e'),  # ã  ->  ह्म
    (u'\xbaz', u'\u0939\u094d\u0930'),  # ºz  ->  ह्र
    (u'\xba', u'\u0939\u094d'),  # º  ->  ह्
    (u'\xed', u'\u0926\u094d\u0926'),  # í  ->  द्द
    (u'{k', u'\u0915\u094d\u0937'),  # {k  ->  क्ष
    (u'{', u'\u0915\u094d\u0937\u094d'),  # {  ->  क्ष्
    (u'=', u'\u0924\u094d\u0930'),  # =  ->  त्र
    (u'\xab', u'\u0924\u094d\u0930\u094d'),  # «  ->  त्र्
    (u'N\xee', u'\u091b\u094d\u092f'),  # Nî  ->  छ्य
    (u'V\xee', u'\u091f\u094d\u092f'),  # Vî  ->  ट्य
    (u'B\xee', u'\u0920\u094d\u092f'),  # Bî  ->  ठ्य
    (u'M\xee', u'\u0921\u094d\u092f'),  # Mî  ->  ड्य
    (u'<\xee', u'\u0922\u094d\u092f'),  # <î  ->  ढ्य
    (u'|', u'\u0926\u094d\u092f'),  # |  ->  द्य
    (u'K', u'\u091c\u094d\u091e'),  # K  ->  ज्ञ
    (u'}', u'\u0926\u094d\u0935'),  # }  ->  द्व
    (u'J', u'\u0936\u094d\u0930'),  # J  ->  श्र
    (u'V\xaa', u'\u091f\u094d\u0930'),  # Vª  ->  ट्र
    (u'M\xaa', u'\u0921\u094d\u0930'),  # Mª  ->  ड्र
    (u'<\xaa\xaa', u'\u0922\u094d\u0930'),  # <ªª  ->  ढ्र
    (u'N\xaa', u'\u091b\u094d\u0930'),  # Nª  ->  छ्र
    (u'\xd8', u'\u0915\u094d\u0930'),  # Ø  ->  क्र
    (u'\xdd', u'\u092b\u094d\u0930'),  # Ý  ->  फ्र
    (u'nzZ', u'\u0930\u094d\u0926\u094d\u0930'),  # nzZ  ->  र्द्र
    (u'\xe6', u'\u0926\u094d\u0930'),  # æ  ->  द्र
    (u'\xe7', u'\u092a\u094d\u0930'),  # ç  ->  प्र
    (u'\xc1', u'\u092a\u094d\u0930'),  # Á  ->  प्र
    (u'xz', u'\u0917\u094d\u0930'),  # xz  ->  ग्र
    (u'#', u'\u0930\u0941'),  # #  ->  रु
    (u':', u'\u0930\u0942'),  # :  ->  रू
    (u'v\u201a', u'\u0911'),  # v‚  ->  ऑ
    (u'vks', u'\u0913'),  # vks  ->  ओ
    (u'vkS', u'\u0914'),  # vkS  ->  औ
    (u'vk', u'\u0906'),  # vk  ->  आ
    (u'v', u'\u0905'),  # v  ->  अ
    (u'b\xb1', u'\u0908\u0902'),  # b±  ->  ईं
    (u'\xc3', u'\u0908'),  # Ã  ->  ई
    (u'bZ', u'\u0908'),  # bZ  ->  ई
    (u'b', u'\u0907'),  # b  ->  इ
    (u'm', u'\u0909'),  # m  ->  उ
    (u'\xc5', u'\u090a'),  # Å  ->  ऊ
    (u',s', u'\u0910'),  # ,s  ->  ऐ
    (u',', u'\u090f'),  # ,  ->  ए
    (u'_', u'\u090b'),  # _  ->  ऋ
    (u'\xf4', u'\u0915\u094d\u0915'),  # ô  ->  क्क
    (u'd', u'\u0915'),  # d  ->  क
    (u'Dk', u'\u0915'),  # Dk  ->  क
    (u'D', u'\u0915\u094d'),  # D  ->  क्
    (u'[k', u'\u0916'),  # [k  ->  ख
    (u'[', u'\u0916\u094d'),  # [  ->  ख्
    (u'x', u'\u0917'),  # x  ->  ग
    (u'Xk', u'\u0917'),  # Xk  ->  ग
    (u'X', u'\u0917\u094d'),  # X  ->  ग्
    (u'\xc4', u'\u0918'),  # Ä  ->  घ
    (u'?k', u'\u0918'),  # ?k  ->  घ
    (u'?', u'\u0918\u094d'),  # ?  ->  घ्
    (u'\xb3', u'\u0919'),  # ³  ->  ङ
    (u'pkS', u'\u091a\u0948'),  # pkS  ->  चै
    (u'p', u'\u091a'),  # p  ->  च
    (u'Pk', u'\u091a'),  # Pk  ->  च
    (u'P', u'\u091a\u094d'),  # P  ->  च्
    (u'N', u'\u091b'),  # N  ->  छ
    (u't', u'\u091c'),  # t  ->  ज
    (u'Tk', u'\u091c'),  # Tk  ->  ज
    (u'T', u'\u091c\u094d'),  # T  ->  ज्
    (u'>', u'\u091d'),  # >  ->  झ
    (u'\xf7', u'\u091d\u094d'),  # ÷  ->  झ्
    (u'\xa5', u'\u091e'),  # ¥  ->  ञ
    (u'\xea', u'\u091f\u094d\u091f'),  # ê  ->  ट्ट
    (u'\xeb', u'\u091f\u094d\u0920'),  # ë  ->  ट्ठ
    (u'V', u'\u091f'),  # V  ->  ट
    (u'B', u'\u0920'),  # B  ->  ठ
    (u'\xec', u'\u0921\u094d\u0921'),  # ì  ->  ड्ड
    (u'\xef', u'\u0921\u094d\u0922'),  # ï  ->  ड्ढ
    (u'M+', u'\u0921\u093c'),  # M+  ->  ड़
    (u'<+', u'\u0922\u093c'),  # <+  ->  ढ़
    (u'M', u'\u0921'),  # M  ->  ड
    (u'<', u'\u0922'),  # <  ->  ढ
    (u'.k', u'\u0923'),  # .k  ->  ण
    (u'.', u'\u0923\u094d'),  # .  ->  ण्
    (u'r', u'\u0924'),  # r  ->  त
    (u'Rk', u'\u0924'),  # Rk  ->  त
    (u'R', u'\u0924\u094d'),  # R  ->  त्
    (u'Fk', u'\u0925'),  # Fk  ->  थ
    (u'F', u'\u0925\u094d'),  # F  ->  थ्
    (u')', u'\u0926\u094d\u0927'),  # )  ->  द्ध
    (u'n', u'\u0926'),  # n  ->  द
    (u'/k', u'\u0927'),  # /k  ->  ध
    #   (u'\xe8k', u'\u0927'),  #  èk  ->  ध
    (u'/', u'\u0927\u094d'),  # /  ->  ध्
    (u'\xcb', u'\u0927\u094d'),  # Ë  ->  ध्
    #   (u'\xe8', u'\u0927\u094d'),  #  è  ->  ध्
    (u'\xe8', u'\u0927'),  # è  ->  ध
    (u'u', u'\u0928'),  # u  ->  न
    (u'Uk', u'\u0928'),  # Uk  ->  न
    (u'U', u'\u0928\u094d'),  # U  ->  न्
    (u'i', u'\u092a'),  # i  ->  प
    (u'Ik', u'\u092a'),  # Ik  ->  प
    (u'I', u'\u092a\u094d'),  # I  ->  प्
    (u'Q', u'\u092b'),  # Q  ->  फ
    (u'\xb6', u'\u092b\u094d'),  # ¶  ->  फ्
    (u'c', u'\u092c'),  # c  ->  ब
    (u'Ck', u'\u092c'),  # Ck  ->  ब
    (u'C', u'\u092c\u094d'),  # C  ->  ब्
    (u'Hk', u'\u092d'),  # Hk  ->  भ
    (u'H', u'\u092d\u094d'),  # H  ->  भ्
    (u'e', u'\u092e'),  # e  ->  म
    (u'Ek', u'\u092e'),  # Ek  ->  म
    (u'E', u'\u092e\u094d'),  # E  ->  म्
    (u';', u'\u092f'),  # ;  ->  य
    (u'\xb8', u'\u092f\u094d'),  # ¸  ->  य्
    (u'j', u'\u0930'),  # j  ->  र
    (u'y', u'\u0932'),  # y  ->  ल
    (u'Yk', u'\u0932'),  # Yk  ->  ल
    (u'Y', u'\u0932\u094d'),  # Y  ->  ल्
    (u'G', u'\u0933'),  # G  ->  ळ
    (u'o', u'\u0935'),  # o  ->  व
    (u'Ok', u'\u0935'),  # Ok  ->  व
    (u'O', u'\u0935\u094d'),  # O  ->  व्
    (u"'k", u'\u0936'),  # 'k  ->  श
    (u"'", u'\u0936\u094d'),  # '  ->  श्
    (u'"k', u'\u0937'),  # "k  ->  ष
    (u'"', u'\u0937\u094d'),  # "  ->  ष्
    (u'l', u'\u0938'),  # l  ->  स
    (u'Lk', u'\u0938'),  # Lk  ->  स
    (u'L', u'\u0938\u094d'),  # L  ->  स्
    (u'g', u'\u0939'),  # g  ->  ह
    (u'\xc8', u'\u0940\u0902'),  # È  ->  ीं
    (u'saz', u'\u094d\u0930\u0947\u0902'),  # saz  ->  ्रें
    (u'z', u'\u094d\u0930'),  # z  ->  ्र
    (u'\xcc', u'\u0926\u094d\u0926'),  # Ì  ->  द्द
    (u'\xcd', u'\u091f\u094d\u091f'),  # Í  ->  ट्ट
    (u'\xce', u'\u091f\u094d\u0920'),  # Î  ->  ट्ठ
    (u'\xcf', u'\u0921\u094d\u0921'),  # Ï  ->  ड्ड
    (u'\xd1', u'\u0915\u0943'),  # Ñ  ->  कृ
    (u'\xd2', u'\u092d'),  # Ò  ->  भ
    (u'\xd3', u'\u094d\u092f'),  # Ó  ->  ्य
    (u'\xd4', u'\u0921\u094d\u0922'),  # Ô  ->  ड्ढ
    (u'\xd6', u'\u091d\u094d'),  # Ö  ->  झ्
    (u'\xd8', u'\u0915\u094d\u0930'),  # Ø  ->  क्र
    (u'\xd9', u'\u0924\u094d\u0924\u094d'),  # Ù  ->  त्त्
    (u'\xdck', u'\u0936'),  # Ük  ->  श
    (u'\xdc', u'\u0936\u094d'),  # Ü  ->  श्
    (u'\u201a', u'\u0949'),  # ‚  ->  ॉ
    (u'kas', u'\u094b\u0902'),  # kas  ->  ों
    (u'ks', u'\u094b'),  # ks  ->  ो
    (u'kS', u'\u094c'),  # kS  ->  ौ
    (u'\xa1k', u'\u093e\u0901'),  # ¡k  ->  ाँ'
    (u'ak', u'k\u0902'),  # ak  ->  k +  ं
    (u'k', u'\u093e'),  # k  ->  ा
    (u'ah', u'\u0940\u0902'),  # ah  ->  ीं
    (u'h', u'\u0940'),  # h  ->  ी
    (u'aq', u'\u0941\u0902'),  # aq  ->   ुं
    (u'q', u'\u0941'),  # q  ->  ु
    (u'aw', u'\u0942\u0902'),  # aw  ->  ूं
    (u'\xa1w', u'\u0942\u0901'),  # ¡w  ->  ूँ
    (u'w', u'\u0942'),  # w  ->  ू
    (u'`', u'\u0943'),  # `  ->  ृ
    (u'\u0300', u'\u0943'),  # ̀  ->  ृ
    (u'as', u'\u0947\u0902'),  # as  ->  ें
    (u'\xb1s', u's\xb1'),  # ±s  ->  s±
    (u's', u'\u0947'),  # s  ->  े
    (u'aS', u'\u0948\u0902'),  # aS  ->  ैं
    (u'S', u'\u0948'),  # S  ->  ै
    (u'a\xaa', u'\u094d\u0930\u0902'),  # aª  ->  ्र + ं
    (u'\xaa', u'\u094d\u0930'),  # ª  ->  ्र
    (u'fa', u'\u0902f'),  # fa  ->  ं  + f
    (u'a', u'\u0902'),  # a  ->  ं
    (u'\xa1', u'\u0901'),  # ¡  ->  ँ
    (u'%', u':'),  # %  ->  :
    (u'W', u'\u0945'),  # W  ->  ॅ
    (u'\u2022', u'\u093d'),  # •  ->  ऽ
    (u'\xb7', u'\u093d'),  # ·  ->  ऽ
    (u'\u2219', u'\u093d'),  # ∙  ->  ऽ
    (u'\xb7', u'\u093d'),  # ·  ->  ऽ
    (u'~j', u'\u094d\u0930'),  # ~j  ->  ्र
    (u'~', u'\u094d'),  # ~  ->  ्
    (u'\\', u'?'),  # \  ->  ?
    (u'+', u'\u093c'),  # +  ->  ़
    (u'^', u'\u2018'),  # ^  ->  ‘
    (u'*', u'\u2019'),  # *  ->  ’
    (u'\xde', u'\u201c'),  # Þ  ->  “
    (u'\xdf', u'\u201d'),  # ß  ->  ”
    (u'(', u';'),  # (  ->  ;
    (u'\xbc', u'('),  # ¼  ->  (
    (u'\xbd', u')'),  # ½  ->  )
    (u'\xbf', u'{'),  # ¿  ->  {
    (u'\xc0', u'}'),  # À  ->  }
    (u'\xbe', u'='),  # ¾  ->  =
    (u'A', u'\u0964'),  # A  ->  ।
    (u'-', u'.'),  # -  ->  .
    (u'&', u'-'),  # &  ->  -
    (u'&', u'\xb5'),  # &  ->  µ
    (u'\u03bc', u'-'),  # μ  ->  -
    (u'\u0152', u'\u0970'),  # Œ  ->  ॰
    (u']', u','),  # ]  ->  ,
    (u'~ ', u'\u094d '),  # ~  ->  ्
    (u'@', u'/'),  # @  ->  /
    (u'\xae', u'\u0948\u0902'),  # ®  ->  ैं
    #   (u'%', u'\u0903'),  #  %  ->  ः
    #   (u' \u0903', u':'),  #   ः  ->  :
    #   (u'\xc7', u'\u093f\u0902'), #  Ç  ->  िं
    #   (u'\xca', u'\u0940Z'), #  Ê  ->  ीZ
    #   (u'Z', u'\u0930\u094d'), #  Z  ->  र्
    #   (u'f', u'\u093f'), #  f  ->  ि
    #   (u'\xb1', u'Z\u0902'), #  ±  ->  Zं
    #   (u'\xc6', u'\u0930\u094d\u093f'), #  Æ  ->  र्ि
    #   (u'\xc9', u'\u0930\u094d\u093f\u0902'),  #  É  ->  र्ि'
]

unicode_vowel_signs = [
    u'\u0905',  # अ
    u'\u0906',  # आ
    u'\u0907',  # इ
    u'\u0908',  # ई
    u'\u0909',  # उ
    u'\u090a',  # ऊ
    u'\u090f',  # ए
    u'\u0910',  # ऐ
    u'\u0913',  # ओ
    u'\u0914',  # औ
    u'\u093e',  # ा
    u'\u093f',  # ि
    u'\u0940',  # ी
    u'\u0941',  # ु
    u'\u0942',  # ू
    u'\u0943',  # ृ
    u'\u0947',  # े
    u'\u0948',  # ै
    u'\u094b',  # ो
    u'\u094c',  # ौ
    u'\u0902',  # ं
    u'\u0903',  # ः
    u'\u0901',  # ँ
    u'\u0945',  # ॅ
]

unicode_unattached_vowel_signs = [
    u'\u093e',  # ा
    u'\u093f',  # ि
    u'\u0940',  # ी
    u'\u0941',  # ु
    u'\u0942',  # ू
    u'\u0943',  # ृ
    u'\u0947',  # े
    u'\u0948',  # ै
    u'\u094b',  # ो
    u'\u094c',  # ौ
    u'\u0902',  # ं
    u'\u0903',  # ः
    u'\u0901',  # ँ
    u'\u0945',  # ॅ
]

unicode_consonants = [
    u'\u0915',  # क
    u'\u0916',  # ख
    u'\u0917',  # ग
    u'\u0918',  # घ
    u'\u0919',  # ङ
    u'\u091a',  # च
    u'\u091b',  # छ
    u'\u091c',  # ज
    u'\u091d',  # झ
    u'\u091e',  # ञ
    u'\u091f',  # ट
    u'\u0920',  # ठ
    u'\u0921',  # ड
    u'\u0922',  # ढ
    u'\u0923',  # ण
    u'\u0924',  # त
    u'\u0925',  # थ
    u'\u0926',  # द
    u'\u0927',  # ध
    u'\u0928',  # न
    u'\u0929',  # ऩ
    u'\u092a',  # प
    u'\u092b',  # फ
    u'\u092c',  # ब
    u'\u092d',  # भ
    u'\u092e',  # म
    u'\u092f',  # य
    u'\u0930',  # र
    u'\u0931',  # ऱ
    u'\u0932',  # ल
    u'\u0933',  # ळ
    u'\u0934',  # ऴ
    u'\u0935',  # व
    u'\u0936',  # श
    u'\u0937',  # ष
    u'\u0938',  # स
    u'\u0939',  # ह
    u'\u0958',  # क़
    u'\u0959',  # ख़
    u'\u095a',  # ग़
    u'\u095b',  # ज़
    u'\u095c',  # ड़
    u'\u095d',  # ढ़
    u'\u095e',  # फ़
    u'\u095f',  # य़
]

krutidev_consonants = [
    u'd',  # क
    u'[k',  # ख
    u'x',  # ग
    u'?k',  # घ
    u'\xb3',  # ङ
    u'p',  # च
    u'N',  # छ
    u't',  # ज
    u'>',  # झ
    u'\xa5',  # ञ
    u'V',  # ट
    u'B',  # ठ
    u'M',  # ड
    u'<',  # ढ
    u'.k',  # ण
    u'r',  # त
    u'Fk',  # थ
    u'n',  # द
    u'/k',  # ध
    u'u',  # न
    u'u',  # ऩ
    u'i',  # प
    u'Q',  # फ
    u'c',  # ब
    u'Hk',  # भ
    u'e',  # म
    u';',  # य
    u'j',  # र
    u'j',  # ऱ
    u'y',  # ल
    u'G',  # ळ
    u'\u0934',  # ऴ
    u'o',  # व
    u"'k",  # श
    u'"k',  # ष
    u'l',  # स
    u'g',  # ह
    u'd',  # क़
    u'[k',  # ख़
    u'x',  # ग़
    u't',  # ज़
    u'M+',  # ड़
    u'<+',  # ढ़
    u'Q',  # फ़
    u';',  # य़
    u'D',  # क्
    u'[',  # ख्
    u'X',  # ग्
    u'?',  # घ्
    u'\xb3~',  # ङ्
    u'P',  # च्
    u'N~',  # छ्
    u'T',  # ज्
    u'÷',  # झ्
    u'\xa5~',  # ञ्
    u'V~',  # ट्
    u'B~',  # ठ्
    u'M~',  # ड्
    u'<~',  # ढ्
    u'.',  # ण्
    u'R',  # त्
    u'F',  # थ्
    u'n~',  # द्
    u'/',  # ध्
    u'Ë',  # ध्
    u'è',  # ध्
    u'U',  # न्
    u'I',  # प्
    u'¶',  # फ्
    u'C',  # ब्
    u'H',  # भ्
    u'E',  # म्
    u'\xb8',  # य्
    u'Z',  # र्
    u'Y',  # ल्
    u'O',  # व्
    u"'",  # श्
    u"Ü",  # श्
    u'"',  # ष्
    u'L',  # स्
    u'\xba',  # ह्
]

krutidev_unattached_vowel_signs = [
    u'k',  # ा
    u'f',  # ि
    u'h',  # ी
    u'q',  # ु
    u'w',  # ू
    u'`',  # ृ
    u's',  # े
    u'S',  # ै
    u'ks',  # ो
    u'kS',  # ौ
    u'a',  # ं
    u'%',  # ः
    u'\xa1',  # ँ
    u'W',  # ॅ
]


def getUnicode(unk_txt):
    # Only decode if it's bytes:
    if isinstance(unk_txt, bytes):
        try:
            return unk_txt.decode('utf-8')
        except UnicodeDecodeError:
            return unk_txt.decode('unicode_escape')
    # Already str: no decoding needed
    return unk_txt


def kru2uni(kru_text):
    kru_text = getUnicode(kru_text)

    # space +  ्र  ->   ्र
    kru_text = kru_text.replace(u' \xaa', u'\xaa')
    kru_text = kru_text.replace(u' ~j', u'~j')
    kru_text = kru_text.replace(u' z', u'z')

    # – and — if not surrounded by krutidev consonants/matrās, change them to -
    misplaced = re.compile(r'[\u2014\u2013]')
    for m in misplaced.finditer(kru_text):
        index = m.start()
        if index < len(kru_text) - 1 and kru_text[
            m.start() + 1] not in krutidev_consonants + krutidev_unattached_vowel_signs:
            kru_text = kru_text[: index] + u'&' + kru_text[index + 1:]

    for mapping in k2u:
        kru_text = kru_text.replace(mapping[0], mapping[1])

    kru_text = kru_text.replace(u'\xb1', u'Z\u0902')  # ±  ->  Zं
    kru_text = kru_text.replace(u'\xc6', u'\u0930\u094df')  # Æ  ->  र्f

    #  f + ?  ->  ? + ि
    misplaced = re.search('f(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace('f' + misplaced, misplaced + u'\u093f')
        misplaced = re.search('f(.?)', kru_text)

    kru_text = kru_text.replace(u'\xc7', u'fa')  # Ç  ->  fa
    kru_text = kru_text.replace(u'\xaf', u'fa')  # ¯  ->  fa
    kru_text = kru_text.replace(u'\xc9', u'\u0930\u094dfa')  # É  ->  र्fa

    #  fa?  ->  ? + िं
    misplaced = re.search('fa(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace('fa' + misplaced, misplaced + u'\u093f\u0902')
        misplaced = re.search('fa(.?)', kru_text)

    kru_text = kru_text.replace(u'\xca', u'\u0940Z')  # Ê  ->  ीZ

    #  ि्  + ?  ->  ्  + ? + ि
    misplaced = re.search(u'\u093f\u094d(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace(u'\u093f\u094d' + misplaced, u'\u094d' + misplaced + u'\u093f')
        misplaced = re.search(u'\u093f\u094d(.?)', kru_text)

    kru_text = kru_text.replace(u'\u094dZ', u'Z')  # ्  + Z ->  Z

    # र +  ्  should be placed at the right place, before matrās
    misplaced = re.search('(.?)Z', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        index_r_halant = kru_text.index(misplaced + 'Z')
        while index_r_halant >= 0 and kru_text[index_r_halant] in unicode_vowel_signs:
            index_r_halant -= 1
            misplaced = kru_text[index_r_halant] + misplaced
        kru_text = kru_text.replace(misplaced + 'Z', u'\u0930\u094d' + misplaced)
        misplaced = re.search('(.?)Z', kru_text)

    # ' ', ',' and ्  are illegal characters just before a matrā
    for matra in unicode_unattached_vowel_signs:
        kru_text = kru_text.replace(' ' + matra, matra)
        kru_text = kru_text.replace(',' + matra, matra + ',')
        kru_text = kru_text.replace(u'\u094d' + matra, matra)

    kru_text = kru_text.replace(u'\u094d\u094d\u0930', u'\u094d\u0930')  # ्  + ्  + र ->  ्  + र
    kru_text = kru_text.replace(u'\u094d\u0930\u094d', u'\u0930\u094d')  # ्  + र + ्  ->  र + ्

    kru_text = kru_text.replace(u'\u094d\u094d', u'\u094d')  # ्  + ्  ->  ्

    # ्  at the ending of a consonant as the last character is illegal.
    # Uncomment, if input is Sanskrit
    kru_text = kru_text.replace(u'\u094d ', ' ')

    return kru_text.encode('utf-8')


def convert_kruti_excel(input_file, output_file, skip_columns):
    def infer_occupation_type(eng_value):
        if not eng_value or pd.isna(eng_value):
            return "none"

        val = eng_value.lower()

        if any(k in val for k in ["retired", "pensioner"]):
            return "retired"
        elif any(k in val for k in ["student", "studying"]):
            return "student"
        elif any(k in val for k in ["housewife"]):
            return "housewife"
        elif any(k in val for k in [
            "business", "shopkeeper", "dealer", "store", "transport", "restaurant",
            "marble", "property", "mining", "scrap", "stone", "millinery"
        ]):
            return "business"
        elif any(k in val for k in [
            "engineer", "doctor", "nurse", "lecturer", "teacher", "professor", "accountant",
            "job", "employee", "freelance", "artist", "developer", "advocate",
            "manager", "driver", "assistant", "bank", "government", "service", "police",
            "railway", "court", "contractor"
        ]):
            return "job"
        else:
            return "job"  # Default fallback
    # Read Excel file
    df = pd.read_excel(input_file, engine='openpyxl')

    # Convert column indices to column names
    skip_col_names = [df.columns[i] for i in skip_columns if i < len(df.columns)]

    for i in range(len(df)):
        for col in df.columns:
            if col in skip_col_names:
                continue  # Skip conversion for this column
            val = df.at[i, col]
            if pd.notna(val):
                try:
                    converted = kru2uni(str(val))
                    df.at[i, col] = converted.decode('utf-8')
                except Exception as e:
                    print(f"⚠️ Error at row {i + 2}, column '{col}': {val} → {e}")
                    df.at[i, col] = val  # Keep original if error

    new_columns = ['sr_no', 'family_id', 'name', 'gotra', 'father_name', 'family_head', 'relation_with_head',
                   'phone_number', 'whatsapp_no', 'dob', 'birth_place', 'birth_time', 'gender', 'marital_status',
                   'height', 'email', 'current_address', 'current_address_city', 'current_address_state',
                   'current_address_pincode', 'paitrik_nivas', 'paitrik_nivas_city', 'paitrik_nivas_state',
                   'paitrik_nivas_pincode', 'education_type', 'school_class', 'degree', 'occupation_type', 'occupation',
                   'location', 'company_name', 'job_description', 'business_description']
    df.columns = new_columns

    gotra_map = {
        "शांडिल्य": "shaandilya",
        "वत्स": "vatsa",
        "जोशी": "joshi",
        "वशिष्ठ": "vashishtha",
        "दवे": "dave",
        "वत्सत": "vatsat",
        "कवच्छस": "kavachhas",
        "वच्छस": "vachchhas",
        "सामरायण": "samarayan",
        "कवच्छ": "kavachh",
        "कश्यप": "kashyapa",
        "कौत्स": "kauts",
        "वच्छव": "vachchhav",
        "आस्तिक": "aastik",
        "कोत्सस": "kotsas",
        "वत्सस": "vatsas",
        "बनेडा": "baneda",
        "व्यास": "vyas",
        "वत्सक": "vatsak",
        "तिवाडी": "tiwadi",
        "त्रिवाडी": "trivadi",
        "भारद्वाज": "bharadwaja",
        "पाण्ड्या": "pandya",
    }
    marital_status_map = {
        'विवाहित': 'married',
        'अविवाहित': 'unmarried'
    }
    relation_map = {
        'स्वयं': 'self',
        'पत्नी': 'wife',
        'पुत्र': 'son',
        'पुत्रवधु': 'daughter-in-law',
        'पौत्र': 'grandson',
        'माता': 'mother',
        'बहिन': 'sister',
        'पुत्री': 'daughter',
        'सासु मां': 'mother-in-law',
        'पौत्री': 'granddaughter',
        'पिता': 'father',
        'भाई': 'brother',
        'भाईवधु': 'sister-in-law (brother’s wife)',
        'पौत्रवधु': 'grandson’s wife',
        'भाणेज': 'nephew (sister’s son)',
        'अनुजपत्नी': 'younger brother’s wife',
        'साुसजी': 'mother-in-law (alternate spelling)',
        'भतीजा': 'nephew (brother’s son)',
        'दोहिता': 'daughter’s daughter',
        'सासुजी': 'mother-in-law (respectful)',
        'पंत्रवधु': 'great-grandson’s wife',
        'प्रपौत्री': 'great-granddaughter',
        'प्रपौत्र': 'great-grandson',
        'भ्राता': 'brother',
        'भ्रातावधु': 'sister-in-law (brother’s wife)',
        'बडे भ्राता': 'elder brother',
        'बहन': 'sister',
        'दादीजी': 'paternal grandmother (respectful)',
        'अनुजभ्राता': 'younger brother',
        'अनुजवधु': 'younger brother’s wife',
        'पुत्रवधाु': 'daughter-in-law (misspelled)',
        'काकीसा': 'aunt (uncle’s wife)',
        'भुवा': 'father’s sister',
        'भ्रातावधाु': 'sister-in-law (brother’s wife, alternate)',
        'भतीजी': 'niece (brother’s daughter)',
        'दादी': 'paternal grandmother',
    }
    degree_map = {
        "बी. ए.": "ba",
        "बी.ए.": "ba",
        "बी. ए": "ba",
        "बीए": "ba",
        "बीए एमए": "ba, ma",
        "बीए. बीएड": "ba, bed",
        "बी.ए. बी.एड.": "ba, bed",
        "बीएबीएड": "ba, bed",
        "बीए, बी.एड.": "ba, bed",
        "बीए बीएड": "ba, bed",
        "बीए एमएस": "ba, ms",
        "बीए नर्सिंग": "ba, nursing",
        "बीए बीपीएड": "ba, bped",
        "बी.ए. एमएसडब्लू": "ba, msw",
        "बीएड": "bed",
        "बी.एड.": "bed",
        "बीएड एमबीए": "bed, mba",
        "बी.कॉम": "bcom",
        "बी.काॅम": "bcom",
        "बी. कॉम": "bcom",
        "बी.काॅम.": "bcom",
        "बी.काॅॅम.": "bcom",
        "बीकाॅम": "bcom",
        "बीकाॅम सीए": "bcom, ca",
        "बीएससी": "bsc",
        "बी.एससी.": "bsc",
        "बीएससी, बीएड": "bsc, bed",
        "बीएससी बीएड": "bsc, bed",
        "बीएससी एजी": "bsc, agri",
        "बीएससी पीजीडीसीए": "bsc, pgdca",
        "बीएसटीसी": "bstc",
        "बीबीए": "bba",
        "बीसीए": "bca",
        "बीसीए बीएड": "bca, bed",
        "बी.टेक": "btech",
        "बी.टेक.": "btech",
        "बी. टेक": "btech",
        "बीटेक": "btech",
        "बीई": "be",
        "बी0ई0": "be",
        "बीईर्रर्रर्रर्रर्रर्रर्रर्रर्रर्रर्रर्रर्रर्र": "be",
        "एम.ए.": "ma",
        "एमए": "ma",
        "एम ए": "ma",
        "एम. ए.": "ma",
        "एमए, बीएड": "ma, bed",
        "एमए, बी.एड": "ma, bed",
        "एमए पीएचडी": "ma, phd",
        "एमए डिप्लोमा": "ma, diploma",
        "एमए बीबीएम": "ma, bba",
        "एमए एमएड": "ma, med",
        "एमए बीएड": "ma, bed",
        "एमए एमएसडल्यू": "ma, msw",
        "एमएसी": "msc",
        "एमएससी": "msc",
        "एमएससी बीएड": "msc, bed",
        "एमएससी, बीएड": "msc, bed",
        "एमएसडब्लू": "msw",
        "एम.एससी.": "msc",
        "एम.कॉम": "mcom",
        "एम. कॉम": "mcom",
        "एमकॉम": "mcom",
        "एम.कॉम.": "mcom",
        "एम.काॅम.": "mcom",
        "एमकाॅम": "mcom",
        "एम.काॅम. बी.एड.": "mcom, bed",
        "एमकाॅम बीएड": "mcom, bed",
        "एमकाॅम, एमबीए": "mcom, mba",
        "एमबीए": "mba",
        "एमबीए पीजीडीसीए": "mba, pgdca",
        "इन्जि. एमबीए": "mba",
        "एमसीए": "mca",
        "एम. टेक": "mtech",
        "एमटेक": "mtech",
        "एलएलबी": "llb",
        "डीएलएलबी": "dllb",
        "एमफार्मा": "mpharma",
        "बी फार्मा": "bpharma",
        "बीफार्मा": "bpharma",
        "बीएएमएस": "ba, ms",
        "पीएचडी": "phd",
        "डाॅक्टर": "doctor",
        "शिशु विशेषज्ञ": "pediatrician",
        "डिप्लोमा": "diploma",
        "पोस्ट ग्रेज्यूएट": "postgraduate",
        "स्नातकोत्तर": "postgraduate",
        "स्नातक": "graduate",
        "यूजी": "ug",
        "पीयूसी": "puc",
        "एसटीसी": "stc",
        "एसएससी": "ssc",
        "एसएससी बीएड": "ssc, bed",
        "प्रथम वर्ष": "first year",
        "लाॅ.अ.": "llb",
        "नेट संस्कृत": "net (sanskrit)",
        "सीए": "ca",
        "सीएस एमकाॅम": "cs, mcom",
        "स्टेनाग्राफी": "stenography",
        "पाॅलोटेक्निक": "polytechnic",
        "पोलोटेक्निक": "polytechnic",
        "नर्सिंग": "nursing",
        "नर्सरी": "nursery",
        "अधययन": "study",
        "अधिास्नातक": "postgraduate",
        "अध्ययन": "study",
        "आईअीआई": "iti",
        "आईटीआई": "iti",
        "एनएम": "nm",
        "ग्रेजुएशन": "graduation",
        "बेए": "ba",
        "विधिास्नातक": "law graduate",
        "सैकण्ड्री": "secondary",
        "बीए, एमबीए": "ba, mba",
        "बीए एसटीसी": "ba, stc",
        "एमएबीएड": "ma, bed",
        "एम ए बीएड": "ma, bed",
        "एम.ए. बी.एड.": "ma, bed",
        "एमए, बीसीए": "ma, bca",
        "एमएसएमसीएच": "ms, mch",
        "एमबीबीएस": "mbbs",
        "शिक्षित": "educated",
        "अशिक्षित": "uneducated",
        "बीएससी दजी": "bsc"
    }
    occupation_map = {
        "स्वव्यसाय": "Self-employed",  # Business
        "समाजसेविका": "Social worker",  # Job
        "स्वव्यवसाय": "Self-business",  # Business
        "मेवाड ले0": "Mewar Ltd.",  # Job
        "डेल कं.": "Dell Company",  # Job
        "व्याख्याता": "Lecturer",  # Job
        "एबीपीएम": "ABPM (Assistance Branch Post Master)",  # Job
        "रा0नौकरी": "Government Job",  # Job
        "टंलरिंग": "Tailoring",  # Business
        "सर.नौकरी": "Government Job",  # Job
        "फ्रीलांस आर्टीस्ट": "Freelance Artist",  # Business
        "मैकेनिक": "Mechanic",  # Job
        "स्क्रेप व्यापार": "Scrap Business",  # Business
        "जोशी प्रिन्टर्स": "Joshi Printers",  # Business
        "एडवोकेट": "Advocate",  # Job
        "नौकरी": "Job",  # Job
        "प्रिन्ट प्रेस": "Print Press",  # Business
        "आकाउटेन्ट": "Accountant",  # Job
        "प्राध्यापक": "Professor",  # Job
        "रा.सेवा वि.": "Government Service - Education",  # Job
        "रा0 सेवा": "Government Service",  # Job
        "पेंशनर": "Pensioner",  # Retired
        "साॅ. इन्जि.": "Software Engineer",  # Job
        "हलवाई": "Cook",  # Business
        "आ.सहयेागिनी": "Health Worker Assistant",  # Job
        "राज0सेवा": "State Government Service",  # Job
        "व्यवसाय": "Business",  # Business
        "आ0 माईन्स": "Mining Sector",  # Business
        "श्रम न्यायालय": "Labour Court",  # Job
        "वकालात": "Lawyer",  # Job
        "ठेकेदार": "Contractor",  # Business
        "रा. सेवा.शि.": "Government Service - Education",  # Job
        "इन्जिनियर": "Engineer",  # Job
        "अधययन": "Studying",  # Student
        "अध्ययन": "Studying",  # Student
        "सरकारी क0": "Government Employee",  # Job
        "प्रा0 नौकरी": "Private Job",  # Job
        "डाॅक्यूमेन्ट असि0": "Document Assistant",  # Job
        "हि.जिंक": "Hindustan Zinc Ltd.",  # Job
        "अध्यापिक": "Teacher",  # Job
        "स0नौकरी": "Government Job",  # Job
        "नर्सिंग": "Nursing",  # Job
        "पं. सहायक": "Panchayat Assistant",  # Job
        "ट्रांसपोर्ट": "Transport Business",  # Business
        "अमूल डेयरी": "Amul Dairy",  # Business
        "अकाउंटेन्ट": "Accountant",  # Job
        "साॅ. डवलपर": "Software Developer",  # Job
        "सीए": "Chartered Accountant",  # Job
        "बि. उपकरण": "Business Equipment",  # Business
        "नौकरी टीसीसी": "TCC Job",  # Job
        "साॅफ्ट.इन्जि": "Software Engineer",  # Job
        "प्रो0 डिलर": "Product Dealer",  # Business
        "महाप्रबंधक": "General Manager",  # Job
        "मा.इन्जि": "Mechanical Engineer",  # Job
        "न्याय वि0": "Judicial Service",  # Job
        "बैंक सेवा": "Bank Service",  # Job
        "प्रा.नौकरी": "Private Job",  # Job
        "ग्राम सेवक": "Village Worker",  # Job
        "प्रा. नौकरी": "Private Job",  # Job
        "रा. सेवा": "Government Service",  # Job
        "रेस्टोरेन्ट": "Restaurant",  # Business
        "फि0 चेकर": "Fit Checker",  # Job
        "आंगूचा मा0": "Anganwadi Worker",  # Job
        "पंचायत रा.": "Panchayat Government Work",  # Job
        "मार्बल": "Marble Business",  # Business
        "ब्यूटी पार्लर": "Beauty Parlour",  # Business
        "अ.बाल.क.स.": "Integrated Child Development Worker",  # Job
        "मैनेजर रेमडस": "Manager at Remdes",  # Job
        "बैंक मैनेजर": "Bank Manager",  # Job
        "सेवानिवृत": "Retired",  # Retired
        "कनि.लेख.": "Junior Accountant",  # Job
        "कृषि": "Agriculture",  # Business
        "फीटर": "Fitter",  # Job
        "रा.पुलिस": "State Police",  # Job
        "राज. सेवा": "State Government Service",  # Job
        "बि0मे0सप्ला0": "BMSPL (Business Name Abbreviation)",  # Job
        "गृहिणी": "Housewife",  # Housewife
        "होमगार्ड": "Home Guard",  # Job
        "एसडीएम": "Sub-Divisional Magistrate (SDM)",  # Job
        "सॉफ्ट. इन्जि": "Software Engineer",  # Job
        "प्रोपर्टी": "Property Business",  # Business
        "प्रधानाध्यापिका": "Headmistress",  # Job
        "साफ्टवेयर डवलपर": "Software Developer",  # Job
        "आंगनवाड़ी": "Anganwadi Worker",  # Job
        "राज.सेवा": "State Government Service",  # Job
        "पण्डिताई": "Priesthood",  # Job
        "ज्योतिष": "Astrologer",  # Business
        "प्रो. स्टोर": "Provision Store",  # Business
        "आंगनवाडी": "Anganwadi Worker",  # Job
        "अध्यापक": "Teacher",  # Job
        "रा.सेवा": "Government Service",  # Job
        "कृषि व्यापार": "Agriculture Business",  # Business
        "खनन व्य0": "Mining Business",  # Business
        "जि.परिषद": "District Council",  # Job
        "व.सहा.": "Senior Assistant",  # Job
        "से0सि0इन": "SSC (Staff Selection Commission)",  # Job
        "मैलनर्स व्यापार": "Millinery Business",  # Business
        "व्यापार": "Business",  # Business
        "शाॅप": "Shopkeeper",  # Business
        "एमआर": "Medical Representative",  # Job
        "अध्यापिका": "Teacher",  # Job
        "ब्लाॅक मै.": "Block Manager",  # Job
        "स0डेयरी": "Dairy Business",  # Business
        "डाॅक्टर": "Doctor",  # Job
        "पैंशनर": "Pensioner",  # Retired
        "मैकनिक": "Mechanic",  # Job
        "मैके.इन्जि": "Mechanical Engineer",  # Job
        "ड्राईवर": "Driver",  # Job
        "पटवारी": "Land Record Officer (Patwari)",  # Job
        "व.सीमेन्ट": "Cement Worker",  # Job
        "आयुष नर्स": "Ayush Nurse",  # Job
        "रा0सेवा": "Government Service",  # Job
        "अधयापिका": "Teacher",  # Job
        "प. स्टोन": "Stone Business",  # Business
        "अधयापक": "Teacher",  # Job
        "सो.इन्जिनियर": "Software Engineer",  # Job
        "भा.रे.सेवा.": "Indian Railways Service",  # Job
        "कॉनट्रेक्टर": "Contractor",  # Business
        "ईले. इन्जि": "Electrical Engineer",  # Job
        "बैंक मैं.": "Bank Staff",  # Job
        "सीमेन्ट फ.": "Cement Factory",  # Business
        "रा0नौ": "Government Job"  # Job
    }
    occupation_type_map = {
        "स्वव्यसाय": "Business",
        "समाजसेविका": "Job",
        "स्वव्यवसाय": "Business",
        "मेवाड ले0": "Job",
        "डेल कं.": "Job",
        "व्याख्याता": "Job",
        "एबीपीएम": "Job",
        "रा0नौकरी": "Job",
        "टंलरिंग": "Business",
        "सर.नौकरी": "Job",
        "फ्रीलांस आर्टीस्ट": "Business",
        "मैकेनिक": "Job",
        "स्क्रेप व्यापार": "Business",
        "जोशी प्रिन्टर्स": "Business",
        "एडवोकेट": "Job",
        "नौकरी": "Job",
        "प्रिन्ट प्रेस": "Business",
        "आकाउटेन्ट": "Job",
        "प्राध्यापक": "Job",
        "रा.सेवा वि.": "Job",
        "रा0 सेवा": "Job",
        "पेंशनर": "Retired",
        "साॅ. इन्जि.": "Job",
        "हलवाई": "Business",
        "आ.सहयेागिनी": "Job",
        "राज0सेवा": "Job",
        "व्यवसाय": "Business",
        "आ0 माईन्स": "Business",
        "श्रम न्यायालय": "Job",
        "वकालात": "Job",
        "ठेकेदार": "Business",
        "रा. सेवा.शि.": "Job",
        "इन्जिनियर": "Job",
        "अधययन": "Student",
        "अध्ययन": "Student",
        "सरकारी क0": "Job",
        "प्रा0 नौकरी": "Job",
        "डाॅक्यूमेन्ट असि0": "Job",
        "हि.जिंक": "Job",
        "अध्यापिक": "Job",
        "स0नौकरी": "Job",
        "नर्सिंग": "Job",
        "पं. सहायक": "Job",
        "ट्रांसपोर्ट": "Business",
        "अमूल डेयरी": "Business",
        "अकाउंटेन्ट": "Job",
        "साॅ. डवलपर": "Job",
        "सीए": "Job",
        "बि. उपकरण": "Business",
        "नौकरी टीसीसी": "Job",
        "साॅफ्ट.इन्जि": "Job",
        "प्रो0 डिलर": "Business",
        "महाप्रबंधक": "Job",
        "मा.इन्जि": "Job",
        "न्याय वि0": "Job",
        "बैंक सेवा": "Job",
        "प्रा.नौकरी": "Job",
        "ग्राम सेवक": "Job",
        "प्रा. नौकरी": "Job",
        "रा. सेवा": "Job",
        "रेस्टोरेन्ट": "Business",
        "फि0 चेकर": "Job",
        "आंगूचा मा0": "Job",
        "पंचायत रा.": "Job",
        "मार्बल": "Business",
        "ब्यूटी पार्लर": "Business",
        "अ.बाल.क.स.": "Job",
        "मैनेजर रेमडस": "Job",
        "बैंक मैनेजर": "Job",
        "सेवानिवृत": "Retired",
        "कनि.लेख.": "Job",
        "कृषि": "Business",
        "फीटर": "Job",
        "रा.पुलिस": "Job",
        "राज. सेवा": "Job",
        "बि0मे0सप्ला0": "Job",
        "गृहिणी": "Housewife",
        "होमगार्ड": "Job",
        "एसडीएम": "Job",
        "सॉफ्ट. इन्जि": "Job",
        "प्रोपर्टी": "Business",
        "प्रधानाध्यापिका": "Job",
        "साफ्टवेयर डवलपर": "Job",
        "आंगनवाड़ी": "Job",
        "राज.सेवा": "Job",
        "पण्डिताई": "Job",
        "ज्योतिष": "Business",
        "प्रो. स्टोर": "Business",
        "आंगनवाडी": "Job",
        "अध्यापक": "Job",
        "रा.सेवा": "Job",
        "कृषि व्यापार": "Business",
        "खनन व्य0": "Business",
        "जि.परिषद": "Job",
        "व.सहा.": "Job",
        "से0सि0इन": "Job",
        "मैलनर्स व्यापार": "Business",
        "व्यापार": "Business",
        "शाॅप": "Business",
        "एमआर": "Job",
        "अध्यापिका": "Job",
        "ब्लाॅक मै.": "Job",
        "स0डेयरी": "Business",
        "डाॅक्टर": "Job",
        "पैंशनर": "Retired",
        "मैकनिक": "Job",
        "मैके.इन्जि": "Job",
        "ड्राईवर": "Job",
        "पटवारी": "Job",
        "व.सीमेन्ट": "Job",
        "आयुष नर्स": "Job",
        "रा0सेवा": "Job",
        "अधयापिका": "Job",
        "प. स्टोन": "Business",
        "अधयापक": "Job",
        "सो.इन्जिनियर": "Job",
        "भा.रे.सेवा.": "Job",
        "कॉनट्रेक्टर": "Business",
        "ईले. इन्जि": "Job",
        "बैंक मैं.": "Job",
        "सीमेन्ट फ.": "Business",
        "रा0नौ": "Job",
    }
    if 'gotra' in df.columns:
        df['gotra'] = df['gotra'].apply(lambda x: gotra_map.get(str(x).strip(), x))

    if 'marital_status' in df.columns:
        df['marital_status'] = df['marital_status'].apply(lambda x: marital_status_map.get(str(x).strip(), x))

    if 'relation_with_head' in df.columns:
        df['relation_with_head'] = df['relation_with_head'].apply(lambda x: relation_map.get(str(x).strip(), x))

    if 'degree' in df.columns:
        df['degree'] = df['degree'].apply(lambda x: degree_map.get(str(x).strip(), x))

    df['occupation'] = df['occupation_type'].apply(lambda x: occupation_map.get(str(x).strip(), x))
    df['occupation_type'] = df['occupation_type'].apply(lambda x: occupation_type_map.get(str(x).strip(), x))

    # Save converted DataFrame to a new Excel file
    df.to_excel(output_file, index=False)
    print(f"✅ Unicode Excel saved as: {output_file}")


if __name__ == '__main__':
    # Note: column starts from 0
    input_file_path = './paliwal_samaj_data.xlsx'
    output_file_path = './paliwal_samaj_data_unicode.xlsx'
    skip_columns = [0, 1, 5, 7, 8, 9, 11, 12, 14, 15, 19, 23, 24, 25]
    convert_kruti_excel(input_file_path, output_file_path, skip_columns)



# 0    -    sr_no                    -    Sr. No.
# 1    -    family_id                -    Family Id
# 2    -    name                     -    Name
# 3    -    gotra                    -    Gotra
# 4    -    father_name              -    Father Name
# 5    -    family_head              -    Family Head
# 6    -    relation_with_head       -    Relation with Head
# 7    -    phone_number             -    Phone Number
# 8    -    whatsApp_no              -    WhatsApp No
# 9    -    dob                      -    Date of Birth (dd/mm/yyyy)
# 10   -    birth_place              -    Birth Place
# 11   -    birth_time               -    Birth Time (24 Hr Format)
# 12   -    gender                   -    Gender (Male/Female)
# 13   -    marital_status           -    Marital Status (Unmarried / Married)
# 14   -    height                   -    Height (cm)
# 15   -    email                    -    Email
# 16   -    current_address          -    Current Address
# 17   -    current_address_city     -    Current Address (City)
# 18   -    current_address_state    -    Current Address (State)
# 19   -    current_address_pincode  -    Current Address (Pincode)
# 20   -    paitrik_nivas            -    Paitrik Nivas
# 21   -    paitrik_nivas_city       -    Paitrik Nivas (City)
# 22   -    paitrik_nivas_state      -    Paitrik Nivas (State)
# 23   -    paitrik_nivas_pincode    -    Paitrik Nivas (Pincode)
# 24   -    education_type           -    Education Type (School/College/Graduated)
# 25   -    school_class             -    Class (if School)
# 26   -    degree                   -    Degree (if College or Graduated)
# 27   -    occupation_type          -    Occupation Type (Student/Job/Business/Retired/Housewife)
# 28   -    occupation               -    Occupation
# 29   -    location                 -    Location
# 30   -    company_name             -    Company Name
# 31   -    job_description          -    Job Description (if Job)
# 32   -    business_description     -    Business Description (if Business)