from fake_useragent import UserAgent
from lxml import etree
from urllib import request


def get_translations(html_object):
    result_translations = []
    html_translation = html_object.xpath('//div[@class="qdef"]/ul/li/span')
    for i in range(0, len(html_translation), 2):
        translations = Translation(
            html_translation[i].text, html_translation[i + 1].xpath('span')[0].text)
        result_translations.append(translations)
    return result_translations


def get_phonetics(html_object):
    phonetic = []
    result_phonetics_usa = ""
    result_phonetics_uk = ""
    usa = html_object.xpath('//div[@class="hd_prUS b_primtxt"]/text()')
    for item in usa:
        result_phonetics_usa = item

    uk = html_object.xpath('//div[@class="hd_pr b_primtxt"]/text()')
    for item in uk:
        result_phonetics_uk = item
    phonetic.append(result_phonetics_usa)
    phonetic.append(result_phonetics_uk)
    return phonetic


def get_tenses(html_object):
    result_tense = []
    html_tenses = html_object.xpath(
        '//div[@class="hd_div1"]/div[@class="hd_if"]')
    for tense in html_tenses:
        for j in range(0, len(tense.xpath('span'))):
            # ten = Tense(tense.xpath('span')[j].text, tense.xpath('a')[j].text)
            ten = []
            ten.append(tense.xpath('span')[j].text)
            ten.append(tense.xpath('a')[j].text)
            result_tense.append(ten)
            # print(tense.xpath('span')[j].text+"||"+tense.xpath('a')[j].text)
    return result_tense


def get_Colls(html_object):
    result_coll = []
    colid = html_object.xpath('//div[@id="colid"]/div[@class="df_div2"]/div')
    for i in range(0, len(colid), 2):
        coll = []
        coll.append(colid[i].text)
        content = []
        for k in range(0, len(colid[i + 1].xpath('a/span'))):
            content.append(colid[i + 1].xpath('a/span')[k].text)
        result = '; '.join(content)
        coll.append(result)
        result_coll.append(coll)
    return result_coll


def get_synonym(html_object):
    result_synonym = []
    synonym = html_object.xpath(
        '//div[@id="synoid"]/div[@class="df_div2"]/div')
    for i in range(0, len(synonym), 2):
        syno = []
        syno.append(synonym[i].text)
        content = []
        for k in range(0, len(synonym[i + 1].xpath('a/span'))):
            content.append(synonym[i + 1].xpath('a/span')[k].text)
        result = '; '.join(content)
        syno.append(result)
        result_synonym.append((syno))
    return result_synonym


def get_antonym(html_object):
    result_antonym = []
    antonym = html_object.xpath(
        '//div[@id="antoid"]/div[@class="df_div2"]/div')
    for i in range(0, len(antonym), 2):
        an = []
        an.append(antonym[i].text)
        content = []
        for k in range(0, len(antonym[i + 1].xpath('a/span'))):
            content.append(antonym[i + 1].xpath('a/span')[k].text)
        result = '; '.join(content)
        an.append(result)
        result_antonym.append(an)
    return result_antonym


def get_ec(html_object):
    E_C_cixing = html_object.xpath(
        '//div[@id="crossid"]//div[@class="pos pos1"]')
    cixing = []
    for e_c in E_C_cixing:
        cixing.append(e_c.text)

    result_ec = []
    E_C_fanyiall = html_object.xpath(
        '//div[@id="crossid"]//div[@class="def_fl"]')
    for i in range(len(E_C_fanyiall)):
        fanyi = E_C_fanyiall[i].xpath('div/div[2]/span/text()')
        strfanyi = '|'.join(fanyi)
        ec = []
        ec.append(cixing[i])
        ec.append(strfanyi)
        result_ec.append(ec)
    return result_ec


def get_examples(html_object):
    result_examples = []
    examples_e = html_object.xpath('//div[@class="sen_en b_regtxt"]')
    examples_cn = html_object.xpath('//div[@class="sen_cn b_regtxt"]')
    if len(examples_e) == len(examples_cn):
        exam = []
        for i in examples_e:
            shuchu = i.xpath('*/text()')
            result = ''.join(shuchu)
            exam.append(result)
        exam2 = []
        for i in range(len(examples_cn)):
            ex = []
            shuchu = examples_cn[i].xpath('*/text()')
            result = ''.join(shuchu)
            ex.append(exam[i])
            ex.append(result)
            result_examples.append(ex)
    else:
        print("例句原文和翻译个数不对等。")
    return result_examples


def get_advanced_ec2(html_object):
    result_advanced_ec = []
    advanced_ecs = html_object.xpath(
        '//div[@class="se_lis"]//div[@class="def_pa"]')
    for advanced_ec in advanced_ecs:
        ecs = advanced_ec.xpath('*//text()')
        result = ''.join(ecs)
        result_advanced_ec.append(result)
        # print(result)
    return result_advanced_ec


def get_advanced_ec(html_object):
    get_liju_e = html_object.xpath(
        '//div[@class="li_pos"]//div[@class="val_ex"]')
    get_liju_cn = html_object.xpath(
        '//div[@class="li_pos"]//div[@class="bil_ex"]')
    get_len = len(get_liju_e)
    result_advanced_ec = []
    for i in range(get_len):
        liju = []
        liju.append(get_liju_e[i].text)
        liju.append(get_liju_cn[i].text)
        result_advanced_ec.append(liju)
    return result_advanced_ec


class Translation:
    def __init__(self, partOfSpeech, trans: str):
        self.partOfSpeech = partOfSpeech
        self.trans = trans


class Tense:
    def _init_(self, type, word):
        self.type = type
        self.word = word


class Phonetics:
    def _init_(self, usa, uk):
        self.usa = usa
        self.uk = uk


def main():
    words = ["fish"]
    for word in words:
        print('**********************************************\n' + word)
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'cookie': 'MUID=367B41EFF47062A605484E30F5E46391; MUIDB=367B41EFF47062A605484E30F5E46391; _EDGE_V=1; SRCHD=AF=S00028; SRCHUID=V=2&GUID=F7D0BC7B24F248BDB0FDBBC08BB9A85D&dmnchg=1; SRCHS=PC=U531; ABDEF=V=13&ABDV=11&MRNB=1613443243790&MRB=0; CortanaAppUID=B7FD295599AADF5C6B4CB8957BD7EB80; PPLState=1; SRCHUSR=DOB=20210215&T=1621748122000; BFBUSR=BAWAS=1&BAWFS=1; BFB=AhBsfeIP-sQLL7R_YTtocbOB-qyWjJfVrRuE7dOhroF1IFl1lt1TZe1NhYSZxMR51-c7X7ztxl0LvSC2adqjGdZIp95yS-LhGHF4KOT_yKgy0ZObbT-BH7G1iKFNuYAePR1KuxuwIp_NtbloYsZn8wYY1kivCxr7Z04Cd6raxkUbYg; OID=AhAhLAWVJDHCBbkoGrgHz-SSAdAaeXzOEsJNCGt9PrwWYGXEK_Pe3pwZ2G7N4Jjqf_NHBqeJGLNvf1O6XvDMAilM; OIDI=AhBpeGwcwZXUTmLswWlDo6qZugEjwbCkctbxBNenFEvoWg; ANON=A=B5F7C1CF13C4D4451E36A6CCFFFFFFFF&E=197d&W=3; WLS=C=16b020e3e0f0bd70&N=Tuck+Wai; CSRFCookie=07c01721-dff0-42bb-b779-1df79bc213d8; NAP=V=1.9&E=1951&C=ea5WFTd8EBQPJQ2D_oCx34P8iAS9qCFQK0D8QcR5dUfVr6cs5xGoqg&W=1; KievRPSSecAuth=FACSBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACJ+mZxiYKGWIUAREDk3g3l+YYkXV6Rzbo777k59QQrfBR/A7YiB6D+m/3A70bOdYufXMuBEIRVIvtJSIqXgarZNr/A8p8lsNRz/9xSEeaBt4TfrTeEkoruI69qBdEwSoQuGHFq3frMakm3+QPGGCmoRjZ79RS7lD6zrbQLNeTPRKRnM4T4kIrIqahzzDMN6fwb41NF2Qt/uf+0AZ/k/IsAbYyVhY4J30iH48WUum/+jfcUaCPXanYs8VB0CMeKwAxOxYpXJvnt3eaeVdy4o6KLt1pMmlST0HfvkadYcpmSNuWvd2M2YHlGo28wpxK2B+5jOUF5kTrZ7j44+KnfW/Gi8Z7960meoteLcEKIDPqUGvMPi98Wi73t9kbIg4VEZYB0NmvqR3z4Rj4uk66FzY0SArx/EskE4A6wlg5j8Xw0ZtuWaH69rUrl2xeLinSOf4dpYXsbr32Mz5friyLhMpU8oFPTrwnW3m/njhkXrZ3fWJmdP/3WAXoEkDhp2loOrwQEwkbDkhHZTRJZ7lwtAzpzVsursslFba5ZAVZbHxcHkh3mwuot/cHZlleSzV43ufO0f9M9+r3jKDa0dlrG/LpYg4IoH5DYOSVMU9faez8ewqyETCt6GtqGt26sZjNbsMTGlDe4XlRm5lKQqJwy8ObhZaPkAeY1EmTlEzNmCW6m82tw32hKZzFvTdqXNNj6JVYm4GqWnwuafSIKrfqxjHke9LuJ0xfEKAwuvWwm7lBfc/l5l0QTaPdnxzjA5oyv6OZBtAYthvjofVzVo+MxzlPV9pkrXqZQZCuzvivd2JNDgeLFmWbCtV+LGGqYvf/ty7NbuF70cPgv5cOkKtI8RDA/HYI/lBI7mSgQyS5dEXgO34tckfX+VHlhZyOMw9mPLAHpVlBwuxdbqhlJkvRhtyEp64TNPycCM3wQOGoQNev0pDJ2g9QMqkEVGtDyAOM4R7suqGDgOBgKCdICvYS5LvZqLFfAwmgayfSWqUiuNUsr6ly340SvaR5st7NJRbIbciYrvasmU2Z4xz4NpePBQh5kQT1c1mrf5tNm6WIXhFbIUwW17XP9nSRCXqR+KrpYJUIy74czoP9jev+j2U7PIjczKufa2ZmV/73da6zSJnY+uaSiQ1kj5rvGIy205nC1yOoz9c3V5g2m3RFH5nqIIFSPfIMZ1H9qqvBn28QDm2HHbaV8UpGuXddEbktz1nGfj7DCYpO3RJMrhk0Gb/AF7jQYdBTvtpU+YSyvoORDxf/PGgIzacO53IA4oFu7o5BeJ5jV78NRvgfbkqF7S413ERuLcJiEuRBcfHxDI2XjZrcHGZ+vDXKRD+++kZRONdSEFfF2kqt5i1v+NkSK9e/3mw9az2aCIDQQsFwiOa2iOgiqeECI//NB93puZzgh+k5HEOwTEEqek4JHn6jMdIWyOv+ew2VL1Tt3li3iVoW/2hoS7Qbgbo2YLh3WvOgvVauHsGpWuqLfdVoVy2g1gUAOT7/N/aB5CZSkikjtnbs3sSq2bz; imgv=flts=20210709; _RwBf=mtu=0&g=0&cid=&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2021-07-09T09:12:58.3502965+00:00&e=; _SS=SID=3BA403A969AD6D2C32A20C4968306CFB&PC=U531&R=35&RB=0&GB=0&RG=200&RP=30; _tarLang=default=zh-Hant; _TTSS_IN=hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=; _TTSS_OUT=hist=WyJlcyIsInl1ZSIsInpoLUhhbnQiXQ==; _EDGE_S=SID=2F53BD5B727B6AEE308FAD6F736B6BDE&mkt=zh-cn&ui=zh-hant; ipv6=hit=1626367532758&t=4; _U=1ahhv7FAiWFyy0Sp3xaplf-ieNsqlDGPuZWS3D0STT_nYsf1wFBtcVxwwLPSqp8o3-vT1eAl_BsS9lMyirujjSzORgnnV41YImf-CyKilyGCO7wxe4awCSTsfPm12VgUzQXedaKlKIU-kJd90iXrb2qEUc7JpJzOgrN7AAhN6Bg_37FjXGZfRnTyKtcdhkSXaAG_MBOPv4UPooOtwGrkPCg; SRCHHPGUSR=BRW=W&BRH=M&CW=1396&CH=716&DPR=1.375&UTC=480&DM=1&EXLTT=19&WTS=63748973785&HV=1626424519&SRCHLANGV2=en&PLTL=920&PLTA=1070&PLTN=3&THEME=1&SW=1397&SH=786&SRCHLANG=zh-Hant'
        }
        if True:
            url = 'http://cn.bing.com/dict/search?q=' + word
            req = request.Request(url, None, headers)
            data = ''
            with request.urlopen(req) as uf:
                while True:
                    data_temp = uf.read(1024)
                    if not data_temp:
                        break
                    data += data_temp.decode('utf-8', 'ignore')

            if data:
                # 转换为html对象，以便进行path查找
                html_object = etree.HTML(data)
                last_html_data = etree.tostring(html_object)    # 补全网页字符串
                # 再次转换为html对象，以便进行path查找
                html_object = etree.HTML(last_html_data)
                # -------------------------------音标---------------------------------------------------------------------
                phonetics_result = get_phonetics(html_object)
                print(phonetics_result)
                phonetics_result[0] = phonetics_result[0].replace('\'', '#')
                phonetics_result[0] = phonetics_result[0].replace('#', '\'\'')
                phonetics_result[1] = phonetics_result[1].replace('\'', '#')
                phonetics_result[1] = phonetics_result[1].replace('#', '\'\'')
                insert_phonetic = 'insert into phonetics (word, usa, uk) values (\'' + word + \
                    '\',' + '\'' + \
                    phonetics_result[0] + '\',' + '\'' + \
                    phonetics_result[1] + '\')'
                print(insert_phonetic)
                print("------------------------")
                # -------------------------------翻译---------------------------------------------------------------------
                translations_result = get_translations(html_object)
                for trans in translations_result:
                    print(trans.partOfSpeech, trans.trans)
                    # 这里knife单词有时可能会取到NoneType这种类型，所以进行类型转换。不知道是不是因为bing词典的缘故
                    trans.trans = str(trans.trans).replace('\'', '#')
                    trans.trans = trans.trans.replace('#', '\'\'')
                    insert_trans = 'insert into translations (word, partofspeech, trans) values (\'' + \
                        word + '\',' + '\'' + trans.partOfSpeech + '\',' + '\'' + trans.trans + '\')'
                    print(insert_trans)
                print("------------------------")
                # -------------------------------时态---------------------------------------------------------------------
                tenses_result = get_tenses(html_object)
                for tense in tenses_result:
                    print(tense)
                    tense[1] = tense[1].replace('\'', '#')
                    tense[1] = tense[1].replace('#', '\'\'')
                    insert_tense = 'insert into tenses (word, tensetype, tenseword) values (\'' + \
                        word + '\',' + '\'' + \
                        tense[0] + '\',' + '\'' + tense[1] + '\')'
                    print(insert_tense)
                print("------------------------")
                # -------------------------------Coll---------------------------------------------------------------------
                print("Coll.")
                Coll_result = get_Colls(html_object)
                for co in Coll_result:
                    print(co)
                    insert_coll = 'insert into coll (word, partofspeech, content) values (\'' + word + '\',' + '\'' + \
                        co[0] + '\',' + '\'' + co[1] + '\')'
                    print(insert_coll)
                print("------------------------")
                # -------------------------------近义词---------------------------------------------------------------------
                print("Synonym.")
                synonym_reslut = get_synonym(html_object)
                for sy in synonym_reslut:
                    print(sy)
                    sy[1] = sy[1].replace('\'', '#')
                    sy[1] = sy[1].replace('#', '\'\'')
                    insert_synonym = 'insert into synonym (word, partofspeech, content) values (\'' + word + '\',' + '\'' + \
                        sy[0] + '\',' + '\'' + sy[1] + '\')'
                    print(insert_synonym)
                print("------------------------")
                # -------------------------------反义词---------------------------------------------------------------------
                print("Antonym.")
                antonym_result = get_antonym(html_object)
                for ant in antonym_result:
                    print(ant)
                    insert_antonym = 'insert into antonym (word, partofspeech, content) values (\'' + word + '\',' + '\'' + \
                                     ant[0] + '\',' + '\'' + ant[1] + '\')'
                    print(insert_antonym)
                print("------------------------")
                # -------------------------------Advanced E-C---------------------------------------------------------------------
                # print("Advanced E-C")
                # advanced_ec_result = get_advanced_ec(html_object)
                # for adec in advanced_ec_result:
                #     print(adec)
                #     adec[0] = adec[0].replace('\'', '#')
                #     adec[0] = adec[0].replace('#', '\'\'')
                #     adec[1] = adec[1].replace('\'', '#')
                #     adec[1] = adec[1].replace('#', '\'\'')
                #     insert_advanced = 'insert into advancedec (word, en, cn) values (\'' + word + '\',' + '\'' + \
                #                      adec[0] + '\',' + '\'' + adec[1] + '\')'
                #     cursor.execute(insert_advanced)
                # print("------------------------")

                print("AdvancedEC")
                advanced_ec_result = get_advanced_ec2(html_object)
                for adec in advanced_ec_result:
                    print(adec)
                    adec = adec.replace('\'', '#')
                    adec = adec.replace('#', '\'\'')
                    insert_advanced = 'insert into advancedecs (word, en_cn) values (\'' + \
                        word + '\',' + '\'' + adec + '\')'
                    print(insert_advanced)
                print("------------------------")
                # -------------------------------E-C---------------------------------------------------------------------
                print("E-C")
                ec_result = get_ec(html_object)
                for ee in ec_result:
                    print(ee)
                    ee[1] = ee[1].replace('\'', '#')
                    ee[1] = ee[1].replace('#', '\'\'')
                    insert_ec = 'insert into ec (word, partofspeech, content) values (\'' + word + '\',' + '\'' + \
                        ee[0] + '\',' + '\'' + ee[1] + '\')'
                    print(insert_ec)
                print("------------------------")

                # -------------------------------Sample Examples---------------------------------------------------------------------
                print("例句")
                example_result = get_examples(html_object)
                for exam in example_result:
                    print(exam)
                    exam[0] = exam[0].replace('\'', '#')
                    exam[0] = exam[0].replace('#', '\'\'')
                    exam[1] = exam[1].replace('\'', '#')
                    exam[1] = exam[1].replace('#', '\'\'')
                    insert_example = 'insert into examples (word, en, cn) values (\'' + word + '\',' + '\'' + \
                        exam[0] + '\',' + '\'' + exam[1] + '\')'
                    print(insert_example)


if __name__ == '__main__':
    main()
